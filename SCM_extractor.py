import xml.etree.ElementTree as ET
import os

def parse_jenkins_config(config_file):
    """
    Parse a Jenkins job's config.xml to extract relevant details for GitHub Actions.
    """
    tree = ET.parse(config_file)
    root = tree.getroot()

    # Extract job name (from the 'name' attribute of the root element)
    job_name = root.find(".//name")
    job_name = job_name.text if job_name is not None else os.path.basename(config_file).replace('_config.xml', '')

    # Extract SCM (Git) configuration
    scm = root.find(".//scm")
    git_url = None
    branch_names = []

    if scm is not None:
        # Check if the 'url' element exists
        url_elem = scm.find(".//url")
        if url_elem is not None:
            git_url = url_elem.text
        
        # Check for branch names
        branches = scm.findall(".//branches//name")
        branch_names = [branch.text for branch in branches if branch.text]

    # Extract build steps (shell commands)
    build_steps = []
    for builder in root.findall(".//builders//hudson.tasks.Shell"):
        command = builder.find("command").text
        build_steps.append(command)

    # Extract triggers (if any)
    triggers = []
    for trigger in root.findall(".//triggers//hudson.triggers.TimerTrigger"):
        schedule = trigger.find("spec").text
        triggers.append(schedule)

    # Extract post-build actions
    post_build_actions = []
    for publisher in root.findall(".//publishers"):
        for action in publisher:
            action_name = action.tag
            post_build_actions.append(action_name)

    # Return extracted information
    return {
        "job_name": job_name,
        "git_url": git_url,
        "branch_names": branch_names,
        "build_steps": build_steps,
        "triggers": triggers,
        "post_build_actions": post_build_actions,
    }

def generate_github_actions_yaml(job_data):
    """
    Generate GitHub Actions YAML configuration from the parsed Jenkins job data.
    """
    # Define GitHub Actions YAML template
    yaml_template = f"""
name: {job_data['job_name']}

on:
  push:
    branches:
      - {' '.join(job_data['branch_names'])}
  pull_request:
    branches:
      - {' '.join(job_data['branch_names'])}

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up JDK 11
      uses: actions/setup-java@v1
      with:
        java-version: '11'

    - name: Run build steps
      run: |
        {'\n        '.join(job_data['build_steps'])}
    """
    
    # Add triggers and post-build actions if needed
    if job_data['triggers']:
        yaml_template += f"""
    # Triggers:
    # {' '.join(job_data['triggers'])}
        """

    if job_data['post_build_actions']:
        yaml_template += f"""
    # Post-build actions:
    # {' '.join(job_data['post_build_actions'])}
        """
    
    return yaml_template

def parse_all_jobs(config_dir, output_dir):
    """
    Parse all Jenkins job config files and generate GitHub Actions YAML files.
    """
    # Process all XML files in the config directory
    for config_file_name in os.listdir(config_dir):
        if config_file_name.endswith("_config.xml"):
            config_file_path = os.path.join(config_dir, config_file_name)
            
            # Parse each Jenkins job config file
            job_data = parse_jenkins_config(config_file_path)

            # Generate GitHub Actions YAML
            github_actions_yaml = generate_github_actions_yaml(job_data)

            # Write the GitHub Actions YAML to the output directory
            output_file_name = os.path.join(output_dir, f"{config_file_name.replace('_config.xml', '.yml')}")
            with open(output_file_name, "w") as output_file:
                output_file.write(github_actions_yaml)

            print(f"Generated GitHub Actions YAML for job: {config_file_name.replace('_config.xml', '')}")

# Example usage:
config_dir = "./.github/workflows"
output_dir = "./generated_workflows"
os.makedirs(output_dir, exist_ok=True)
parse_all_jobs(config_dir, output_dir)