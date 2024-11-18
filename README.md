
# Jenkins to GitHub Actions Converter

This project automates the conversion of Jenkins job configurations into GitHub Actions YAML workflows. It parses Jenkins `config.xml` files, extracts relevant details such as SCM configuration, build steps, and triggers, and generates corresponding GitHub Actions workflows.

## Features
- **Download Jenkins Job Configurations:** Fetches `config.xml` files for Jenkins jobs from a Jenkins server.
- **Parse Jenkins Job Details:** Extracts SCM (e.g., Git URLs and branches), build steps, triggers, and post-build actions from Jenkins job configurations.
- **Generate GitHub Actions YAML:** Converts the parsed information into GitHub Actions YAML workflows.
- **Batch Processing:** Handles multiple jobs automatically.

## Requirements
- Python 3.6 or higher
- `curl` command-line tool for downloading Jenkins configurations
- Jenkins server running locally (or accessible with proper credentials)

## Setup

### Clone the Repository
```bash
git clone https://github.com/gabri83/jenkins-to-github-actions.git
cd jenkins-to-github-actions
```

### Install Dependencies
Ensure Python is installed. No external dependencies are required since the code relies on Python's standard library.

### Configure Environment
1. Replace the following placeholders in the `main.py` file with your own values:
   - **User:** Replace `USER` with your Jenkins username.
   - **API Token:** Replace `APITOKEN` with your Jenkins API token.
   - **Output Directory:** Adjust `output_dir` if necessary.

   **Note:** Do not commit sensitive information like usernames or API tokens to version control.

### Prepare Input Data
- Place your `all_jobs.xml` (exported Jenkins job list) in the project root directory.
- Ensure all required permissions for downloading job configurations are set.

## Usage

### Step 1: Download Jenkins Configurations
Run the script to fetch `config.xml` files for all Jenkins jobs listed in `all_jobs.xml`:
```bash
python main.py
```
This will save the `config.xml` files to the `.github/workflows` directory.

### Step 2: Generate GitHub Actions Workflows
Parse the downloaded configurations and generate YAML workflows:
```bash
python generate_workflows.py
```
Generated workflows will be saved in the `generated_workflows` directory.

### Step 3: Review and Commit Workflows
Review the generated YAML files for correctness, then commit them to your GitHub repository:
```bash
git add generated_workflows/
git commit -m "Add GitHub Actions workflows converted from Jenkins jobs"
git push origin main
```

## Example Workflow Output

A typical generated GitHub Actions workflow will look like this:
```yaml
name: example-job-name

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

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
        ./gradlew clean build
```

## Contributing
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request. Ensure sensitive information is never included in commits.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
