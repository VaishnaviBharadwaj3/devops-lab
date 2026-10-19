# Exercise 9: Jenkins Multi-Stage Pipeline for a Python Flask Application

## Aim
To create and execute a Jenkins Pipeline that builds, tests, and deploys a Python Flask application.

## Technologies Used
- Python
- Flask
- Jenkins
- Git and GitHub

## Project Files
- `app.py` — Flask web application.
- `requirements.txt` — Python dependency specification.
- `test_app.py` — Automated unit test.
- `Jenkinsfile` — Defines the CI/CD pipeline stages.

## Pipeline Stages

### 1. Build
Creates a Python virtual environment and installs the dependencies listed in `requirements.txt`.

### 2. Test
Runs automated unit tests using Python's `unittest` framework.

### 3. Deploy
Copies the application files into the `python-app-deploy` directory in the Jenkins workspace.

### 4. Run Application
Starts the Flask application as a background process.

### 5. Test Application
Runs the unit tests again to verify the application after deployment.

## Expected Output
The unit test should pass and display:

`Hello, Jenkins Multi-Stage Pipeline!`

The Jenkins pipeline should finish with:

`Pipeline completed successfully!`

## Result
Implemented a multi-stage Jenkins pipeline for building, testing, and deploying a sample Python Flask application.
