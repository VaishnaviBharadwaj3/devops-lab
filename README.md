# Exercise 5: Docker Security Using AppArmor

## Overview

This exercise demonstrates how to improve Docker container security using AppArmor on Ubuntu. A custom AppArmor profile is created and applied to a Flask application running inside a Docker container.

The profile restricts access to sensitive files and demonstrates how mandatory access control can limit the actions a containerized application can perform.

## Objectives

- Build a Flask application and package it into a Docker image.
- Create a custom AppArmor security profile.
- Load and enforce the AppArmor profile.
- Run a Docker container with the custom profile attached.
- Verify that restricted file access is denied.
- Inspect the container's security configuration.

## Technologies Used

- Ubuntu Linux
- Docker
- AppArmor
- Python 3.8
- Flask
- Nano text editor

## Project Structure

```text
apparmor-flask/
├── app.py
├── Dockerfile
├── requirements.txt
├── image/
│   ├── apparmor-desktop.png
│   ├── apparmor-flask.png
│   └── AppArmor-Verification.png
└── README.md
