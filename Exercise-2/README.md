# Exercise 2: Deploy a Flask App on Minikube Using kubectl and YAML

## Objective

Learn Kubernetes basics using Minikube to set up a single-node Kubernetes cluster and deploy a Python Flask application.

This exercise demonstrates how to:

- Create a Flask application
- Containerize the application using Docker
- Build a Docker image
- Deploy the application using a Kubernetes Deployment
- Verify the Deployment and Pod
- View application logs
- Create a Kubernetes NodePort Service
- Access the Flask application through Minikube

---

# Prerequisites

The following tools are required:

- Docker
- Minikube
- kubectl
- Python
- Flask

Minikube was used to create the local Kubernetes cluster.

---

# Minikube Cheat Sheet

## 1. Starting and Stopping Minikube

```bash
minikube start
minikube stop
minikube delete
```

For this exercise, Minikube was started using Docker:

```bash
minikube start --driver=docker
```

---

## 2. Checking Minikube Status

```bash
minikube status
```

Check Kubernetes cluster information:

```bash
kubectl cluster-info
```

Check Kubernetes nodes:

```bash
kubectl get nodes
```

---

## 3. Accessing Services

Open a Kubernetes Service in the browser:

```bash
minikube service <service-name>
```

List available Minikube services:

```bash
minikube service list
```

---

## 4. Docker with Minikube

Display Minikube Docker environment information:

```bash
minikube docker-env
```

Load an existing local Docker image into Minikube:

```bash
minikube image load <image-name>
```

---

## 5. Debugging and Logs

View Minikube logs:

```bash
minikube logs
```

Open the Kubernetes dashboard:

```bash
minikube dashboard
```

View application logs:

```bash
kubectl logs <pod-name>
```

---

# Step 1: Start Minikube

Start the Minikube cluster using Docker:

```bash
minikube start --driver=docker
```

Check the Minikube status:

```bash
minikube status
```

Check the Kubernetes node:

```bash
kubectl get nodes
```

Expected result:

```text
NAME       STATUS   ROLES           VERSION
minikube   Ready    control-plane   ...
```

The Minikube cluster should be in the `Running` state and the node should be `Ready`.

---

# Step 2: Create a Flask Application

Create a file named:

```text
app.py
```

Add the following code:

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello from Flask on Kubernetes!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)
```

The Flask application provides a single route:

```text
/
```

When the route is accessed, it returns:

```text
Hello from Flask on Kubernetes!
```

The application runs on port:

```text
15000
```

The application listens on:

```text
0.0.0.0
```

This allows the application to accept connections from outside the container.

---

# Step 3: Create a Dockerfile

Create a file named:

```text
Dockerfile
```

Add:

```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install flask

CMD ["python", "app.py"]
```

### Explanation

```text
FROM python:3.8-slim
```

Uses Python 3.8 slim as the base image.

```text
WORKDIR /app
```

Sets `/app` as the working directory inside the container.

```text
COPY . /app
```

Copies the application files into the container.

```text
RUN pip install flask
```

Installs Flask inside the container.

```text
CMD ["python", "app.py"]
```

Starts the Flask application.

---

# Step 4: Build the Docker Image

Build the Docker image:

```bash
docker build -t flask-app .
```

The image is created with the name:

```text
flask-app:latest
```

Verify the image:

```bash
docker images
```

Expected result:

```text
REPOSITORY    TAG       IMAGE ID       CREATED       SIZE
flask-app     latest    ...            ...           ...
```

---

# Step 5: Load the Docker Image into Minikube

The Flask image needs to be available inside the Minikube environment.

Load the image:

```bash
minikube image load flask-app:latest
```

The Kubernetes Deployment uses:

```yaml
imagePullPolicy: Never
```

This means Kubernetes will use the locally available image instead of trying to pull the image from an external registry.

### Kubernetes Image Pull Policies

Kubernetes provides three common image pull policies:

```text
Always
IfNotPresent
Never
```

### Always

```text
Always
```

Kubernetes always pulls the image from a container registry.

### IfNotPresent

```text
IfNotPresent
```

Kubernetes pulls the image only if it is not already available locally.

### Never

```text
Never
```

Kubernetes never pulls the image and only uses the image available locally.

For this exercise:

```yaml
imagePullPolicy: Never
```

is used.

---

# Step 6: Create the Kubernetes Deployment YAML

Create a file named:

```text
flask-deployment.yaml
```

Add:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-app
          image: flask-app:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 15000
```

### Deployment Explanation

The Deployment is named:

```text
flask-app
```

It creates:

```text
1 replica
```

The container uses:

```text
flask-app:latest
```

The container listens on:

```text
15000
```

The image pull policy is:

```text
Never
```

---

# Step 7: Deploy the Application

Apply the Deployment:

```bash
kubectl apply -f flask-deployment.yaml
```

Expected output:

```text
deployment.apps/flask-app created
```

---

# Step 8: Check Deployment Status

Check the Deployment:

```bash
kubectl get deployments
```

Expected output:

```text
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
flask-app   1/1     1            1           ...
```

The Deployment should show:

```text
READY: 1/1
UP-TO-DATE: 1
AVAILABLE: 1
```

This indicates that one replica is running and available.

---

# Step 9: Verify the Pod

Check the Pods created by the Deployment:

```bash
kubectl get pods
```

You can also specifically check Flask Pods:

```bash
kubectl get pods -l app=flask-app
```

Expected output:

```text
NAME                          READY   STATUS    RESTARTS   AGE
flask-app-xxxxxxxxxx-xxxxx    1/1     Running   0          ...
```

The Flask Pod should have:

```text
READY: 1/1
STATUS: Running
```

---

# Troubleshooting: ErrImageNeverPull

During deployment, the Flask Pod may show:

```text
ErrImageNeverPull
```

This means Kubernetes cannot find the `flask-app:latest` image inside Minikube.

Load the image again:

```bash
minikube image load flask-app:latest
```

Delete the failed Pod:

```bash
kubectl delete pod -l app=flask-app
```

Because the Pod is managed by a Deployment, Kubernetes automatically creates a replacement Pod.

Check the Pods again:

```bash
kubectl get pods
```

The replacement Pod should eventually show:

```text
1/1     Running
```

---

# Step 10: Describe the Deployment

Get detailed information about the Deployment:

```bash
kubectl describe deployment flask-app
```

This command provides information about:

- Deployment name
- Namespace
- Replicas
- Pod template
- Container image
- Container port
- Deployment conditions
- ReplicaSet
- Events

The Deployment should show one available replica.

---

# Step 11: View Deployment Logs

First find the Flask Pod:

```bash
kubectl get pods
```

Then view its logs:

```bash
kubectl logs <pod-name>
```

Example:

```bash
kubectl logs flask-app-xxxxxxxxxx-xxxxx
```

Typical Flask output:

```text
* Serving Flask app 'app'
* Debug mode: off
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:15000
```

These logs confirm that Flask is running and listening on port `15000`.

---

# Step 12: Check Kubernetes Services

Check the available Kubernetes Services:

```bash
kubectl get services
```

Initially, the Flask application is running inside the Kubernetes Pod but is not externally accessible.

The application is listening internally on:

```text
15000
```

A Kubernetes Service is therefore required to expose the application.

---

# Step 13: Create the Kubernetes Service

Create a file named:

```text
flask-service.yaml
```

Add:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  type: NodePort
  selector:
    app: flask-app
  ports:
    - protocol: TCP
      port: 15000
      targetPort: 15000
```

### Service Explanation

The Service is named:

```text
flask-service
```

The Service type is:

```text
NodePort
```

The Service listens on:

```text
15000
```

The Service forwards traffic to:

```text
targetPort: 15000
```

The Service selects the Flask Pod using:

```yaml
selector:
  app: flask-app
```

The selector matches the Pod label:

```yaml
labels:
  app: flask-app
```

---

# Step 14: Apply the Service

Create the Service:

```bash
kubectl apply -f flask-service.yaml
```

Expected output:

```text
service/flask-service created
```

---

# Step 15: Check the Service

Verify the Service:

```bash
kubectl get services
```

Example:

```text
NAME            TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)
flask-service   NodePort   10.96.156.42    <none>        15000:31453/TCP
```

The Service exposes:

```text
Service Port: 15000
Target Port: 15000
NodePort: 31453
```

The exact NodePort can vary because Kubernetes assigns the NodePort dynamically.

---

# Step 16: Access the Flask Application

Use Minikube to open the Service:

```bash
minikube service flask-service
```

Minikube opens the application in the browser.

The browser should display:

```text
Hello from Flask on Kubernetes!
```

This confirms that the Flask application is successfully running inside Kubernetes and exposed through a NodePort Service.

---

# Application Output

The Flask application was successfully deployed and accessed through the Kubernetes NodePort Service.

![Flask Application](./image/Flask-app.png)

---

# Kubernetes Architecture

```text
                         Minikube
                            |
                            v
                    Kubernetes Cluster
                            |
                            v
                     Deployment
                      flask-app
                            |
                            v
                         Pod
                            |
                            v
                   Flask Container
                     Port 15000
                            |
                            v
                    Kubernetes Service
                     flask-service
                       NodePort
                            |
                            v
                         Browser
```

---

# Port Mapping

The application uses the following port mapping:

```text
Browser
   |
   v
NodePort
   |
   v
Service Port: 15000
   |
   v
Target Port: 15000
   |
   v
Flask Container
   |
   v
Flask Application
```

---

# Useful Commands

## Minikube

```bash
minikube start --driver=docker
minikube status
minikube stop
minikube delete
minikube image load flask-app:latest
minikube service flask-service
```

## Docker

```bash
docker build -t flask-app .
docker images
```

## Kubernetes

```bash
kubectl get nodes
kubectl get pods
kubectl get deployments
kubectl get services
kubectl describe deployment flask-app
kubectl logs <pod-name>
kubectl apply -f flask-deployment.yaml
kubectl apply -f flask-service.yaml
```

---

# Technologies Used

- Python
- Flask
- Docker
- Kubernetes
- Minikube
- kubectl
- YAML

---

# Key Kubernetes Concepts Practiced

- Kubernetes Cluster
- Minikube
- Nodes
- Pods
- Deployments
- Replica management
- Container images
- `imagePullPolicy`
- Kubernetes Services
- NodePort
- Ports and targetPorts
- Labels and selectors
- `kubectl`
- Application logs
- Troubleshooting
- Service exposure

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