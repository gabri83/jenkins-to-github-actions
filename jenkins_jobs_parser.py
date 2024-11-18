import os
import xml.etree.ElementTree as ET

USER = "YOUR_USERNAME"
APITOKEN = "YOUR_TOKEN"
output_dir = ".github/workflows/"

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def download_job_config(job_name, job_config_file):
    """
    Downloads the job config.xml and saves it to the specified file.
    Uses the correct base URL for Jenkins running on localhost.
    """
    job_url = f'http://localhost:8085/build/job/{job_name}/config.xml'
    command = f'curl -u {USER}:{APITOKEN} "{job_url}" -o {job_config_file}'

    print(f"Downloading config for job: {job_name} from {job_url}")
    response = os.system(command)
    
    if response != 0:
        print(f"Error downloading config for job: {job_name}")
    else:
        print(f"Successfully downloaded {job_config_file}")

def parse_all_jobs(jenkins_xml_file, output_dir):
    """
    Parses all jobs from the provided Jenkins XML file and saves their config files.
    """
    tree = ET.parse(jenkins_xml_file)
    root = tree.getroot()

    for job in root.findall('.//job'):
        job_name = job.find('name').text
        job_config_file = os.path.join(output_dir, f'{job_name}_config.xml')

        # Download the job config file
        download_job_config(job_name, job_config_file)

# Path to the Jenkins jobs XML
jenkins_xml_file = 'all_jobs.xml'

# Run the job parsing and downloading process
parse_all_jobs(jenkins_xml_file, output_dir)