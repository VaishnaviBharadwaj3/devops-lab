# Exercise 2: Deploy Flask Application on Kubernetes

## Objective

Deploy a Flask application on Kubernetes using Minikube and Docker, create a Kubernetes Deployment, expose the application using a NodePort Service, and access it through a web browser.

## Prerequisites

- Docker Desktop
- Minikube
- kubectl
- Python
- Flask

## Project Structure

```text
Exercise-2/
├── image/
│   └── Flask-app.png
├── app.py
├── Dockerfile
├── flask-deployment.yaml
├── flask-service.yaml
└── README.md