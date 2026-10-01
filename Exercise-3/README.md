# Exercise 3: Scaling Flask App on a Single Node Using ReplicaSets

## Real-Life Tech Use Case: E-Commerce Flash Sale

During a flash sale on an e-commerce site such as Flipkart's Big Billion Days or Amazon Prime Day, a simple Flask service might normally handle around 100 requests per minute.

Suddenly, traffic can increase to thousands of requests per minute.

If the application is running in only one Pod, the Pod may become overloaded or crash under the increased load.

Using Kubernetes ReplicaSets, multiple identical Pods can be created to run the same application. For example, the application can be scaled from 1 Pod to 3, 5, 10, or more Pods.

Once the sale ends and traffic returns to normal, the number of Pods can be reduced to save resources.

---

## Objective

The objectives of this exercise are:

- Understand ReplicaSets and Pods
- Scale a Flask application using ReplicaSets
- Observe Pod creation and deletion
- Observe Pod distribution across a node
- Understand self-healing in Kubernetes
- Understand how Kubernetes maintains the desired number of replicas
- Understand how scaling can be used during high-traffic events

---

## Key Observations and Learnings

### 1. Pod Distribution

Each Pod acts like an identical worker running the same Flask application.

Scaling the ReplicaSet means creating additional copies of the application.

For example:

```text
1 Replica
    ↓
1 Pod

5 Replicas
    ↓
5 Pods
```

---

### 2. Resiliency

If one Pod fails or is deleted, the ReplicaSet automatically creates another Pod to maintain the desired number of replicas.

For example:

```text
Desired replicas = 5

5 Pods
   ↓
Delete 1 Pod
   ↓
4 Pods
   ↓
ReplicaSet detects the difference
   ↓
Creates a new Pod
   ↓
5 Pods again
```

---

### 3. Efficiency

Instead of running a large number of servers all the time, additional Pods can be created when demand increases.

After the traffic decreases, the number of Pods can be reduced.

---

### 4. Scalability in the Real World

The same basic scaling concept is useful for applications that need to handle large numbers of users and requests.

Examples include large-scale services such as Netflix, YouTube, and Swiggy.

---

# Application: Flash Sale Buy Orders

The Flask application simulates an e-commerce flash sale.

It provides three endpoints:

- `/` → Welcomes users to the Big Sale
- `/buy` → Simulates a flash-sale checkout
- `/health` → Provides a health status for Kubernetes probes

The application also displays the hostname of the Pod that served the request. This allows us to observe which Pod handled a request.

---

# Project Structure

```text
Exercise-3/
│
├── image/
│   ├── Flash sale.png
│   ├── Buy order.png
│   ├── Health check.png
│   └── Pod recreated.png
│
├── app.py
├── Dockerfile
├── flashsale-replicaset.yaml
└── README.md
```

---

# Step 1: Create the Flask Application

Create a file named:

```text
app.py
```

Use the following code:

```python
from flask import Flask, request
import socket
import time
import random

app = Flask(__name__)

@app.get("/")
def homepage():
    return {
        "message": "Welcome to Big Sale!",
        "pod": socket.gethostname(),
        "ts": time.time()
    }

@app.get("/buy")
def buy():
    item = random.choice([
        "Smartphone",
        "Shoes",
        "Headphones",
        "Laptop"
    ])

    user = request.args.get(
        "user",
        f"user{random.randint(1, 1000)}"
    )

    return {
        "status": "success",
        "item": item,
        "user": user,
        "served_by_pod": socket.gethostname(),
        "time": time.strftime("%H:%M:%S")
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "pod": socket.gethostname()
    }
```

---

# Application Details

## `/` Endpoint

The homepage welcomes users to the flash sale.

It also displays:

- Welcome message
- Pod hostname
- Timestamp

Example:

```json
{
    "message": "Welcome to Big Sale!",
    "pod": "flashsale-rs-pwhnd",
    "ts": 1790845764.38748
}
```

The Pod hostname allows us to identify which Pod served the request.

### Application Output

![Flash Sale Application](./image/Flash%20sale.png)

---

## `/buy` Endpoint

This endpoint simulates a flash-sale checkout.

The application randomly selects one of the following products:

```text
Smartphone
Shoes
Headphones
Laptop
```

A user can also be specified using a query parameter.

Example:

```text
/buy?user=123
```

Example response:

```json
{
    "status": "success",
    "item": "Shoes",
    "user": "123",
    "served_by_pod": "flashsale-rs-pwhnd",
    "time": "09:10:15"
}
```

### Buy Order Output

![Buy Order](./image/Buy%20order.png)

---

## `/health` Endpoint

The health endpoint returns:

```json
{
    "status": "healthy",
    "pod": "flashsale-rs-pwhnd"
}
```

This endpoint is used by Kubernetes for:

- Readiness probe
- Liveness probe

### Health Check Output

![Health Check](./image/Health%20check.png)

---

# Step 2: Create the Dockerfile

Create a file named:

```text
Dockerfile
```

Use:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir flask gunicorn

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "1", "--threads", "2"]
```

The Dockerfile:

1. Uses Python 3.11
2. Creates `/app` as the working directory
3. Copies `app.py` into the container
4. Installs Flask and Gunicorn
5. Starts the Flask application using Gunicorn
6. Runs the application on port `5000`

---

# Step 3: Build the Docker Image

Build the Docker image:

```powershell
docker build -t flashsale:1.0 .
```

Verify the image:

```powershell
docker images
```

The image should contain:

```text
flashsale    1.0
```

The Docker image created for this exercise was:

```text
flashsale:1.0
```

---

# Step 4: Push the Docker Image to Docker Hub

The image can also be pushed to Docker Hub.

Tag the image using your Docker Hub username:

```powershell
docker tag flashsale:1.0 <your-dockerhub-username>/flashsale:1.0
```

Log in to Docker Hub:

```powershell
docker login
```

Push the image:

```powershell
docker push <your-dockerhub-username>/flashsale:1.0
```

For this local Minikube implementation, the image was loaded directly into Minikube instead of relying on Docker Hub.

---

# Step 5: Clean Up Previous Minikube Cluster

If a previous Minikube cluster is already running, stop it:

```powershell
minikube stop
```

Delete the previous cluster:

```powershell
minikube delete
```

This provides a clean environment for the exercise.

---

# Step 6: Start Minikube with a Single Node

Start Minikube with one node:

```powershell
minikube start --nodes=1 --driver=docker
```

Verify the node:

```powershell
kubectl get nodes
```

Expected result:

```text
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   ...   ...
```

There should be one node in the cluster.

The single-node setup is important because this exercise focuses on running multiple Pods on one node.

---

# Step 7: Load the Docker Image into Minikube

The ReplicaSet uses the local image:

```text
flashsale:1.0
```

Load the image into Minikube:

```powershell
minikube image load flashsale:1.0
```

Verify available Minikube images if required:

```powershell
minikube image ls
```

The `flashsale:1.0` image should be available to the Minikube node.

---

# Step 8: Create the ReplicaSet Configuration

Create:

```text
flashsale-replicaset.yaml
```

Use the following configuration:

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: flashsale-rs
  labels:
    app: flashsale

spec:
  replicas: 3

  selector:
    matchLabels:
      app: flashsale

  template:
    metadata:
      labels:
        app: flashsale

    spec:
      containers:
        - name: flashsale-container
          image: flashsale:1.0
          imagePullPolicy: Never

          ports:
            - containerPort: 5000

          readinessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 2
            periodSeconds: 5

          livenessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 10
            periodSeconds: 10

          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"

            limits:
              cpu: "500m"
              memory: "256Mi"

---

apiVersion: v1
kind: Service
metadata:
  name: flashsale-svc

spec:
  selector:
    app: flashsale

  ports:
    - name: http
      port: 80
      targetPort: 5000

  type: ClusterIP
```

---

# ReplicaSet Configuration Explanation

## Replicas

```yaml
replicas: 3
```

This tells Kubernetes to maintain three Pods.

```text
ReplicaSet
    |
    ├── Pod 1
    ├── Pod 2
    └── Pod 3
```

---

## Selector

```yaml
selector:
  matchLabels:
    app: flashsale
```

The ReplicaSet manages Pods with:

```yaml
labels:
  app: flashsale
```

---

## Container Image

```yaml
image: flashsale:1.0
imagePullPolicy: Never
```

`imagePullPolicy: Never` tells Kubernetes to use the image already available on the Minikube node.

---

## Container Port

```yaml
containerPort: 5000
```

The Flask/Gunicorn application listens on port `5000`.

---

# Readiness Probe

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 2
  periodSeconds: 5
```

The readiness probe checks whether the Pod is ready to receive traffic.

Kubernetes sends requests to:

```text
/health
```

---

# Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 10
  periodSeconds: 10
```

The liveness probe checks whether the application is still running correctly.

---

# Resource Requests and Limits

Each Pod has the following resource configuration:

```yaml
requests:
  cpu: "100m"
  memory: "128Mi"

limits:
  cpu: "500m"
  memory: "256Mi"
```

This defines the requested and maximum CPU and memory resources.

---

# Service Configuration

The Service is named:

```text
flashsale-svc
```

It selects Pods using:

```yaml
selector:
  app: flashsale
```

The Service receives traffic on port:

```text
80
```

and forwards it to the Flask application on:

```text
5000
```

Therefore:

```text
Service Port 80
      ↓
Pod Port 5000
```

The Service type is:

```text
ClusterIP
```

---

# Step 9: Apply the ReplicaSet Configuration

Run:

```powershell
kubectl apply -f flashsale-replicaset.yaml
```

Expected output:

```text
replicaset.apps/flashsale-rs created
service/flashsale-svc created
```

This creates:

- ReplicaSet
- Service

---

# Step 10: Verify the ReplicaSet

Run:

```powershell
kubectl get rs
```

Expected result:

```text
NAME           DESIRED   CURRENT   READY
flashsale-rs   3         3         3
```

The important values are:

```text
DESIRED = 3
CURRENT = 3
READY   = 3
```

This means Kubernetes has successfully created and started three replicas.

---

# Step 11: Verify the Pods

Run:

```powershell
kubectl get pods -l app=flashsale
```

Expected result:

```text
NAME                 READY   STATUS    RESTARTS   AGE
flashsale-rs-xxxxx   1/1     Running   0          ...
flashsale-rs-yyyyy   1/1     Running   0          ...
flashsale-rs-zzzzz   1/1     Running   0          ...
```

There should be three Flash Sale Pods.

Each Pod should eventually show:

```text
1/1   Running
```

---

# Step 12: Verify Pod Distribution

Run:

```powershell
kubectl get pods -l app=flashsale -o wide
```

This displays:

- Pod IP
- Node
- Status
- Pod age

Example:

```text
NAME                 READY   STATUS    IP            NODE
flashsale-rs-xxxxx   1/1     Running   10.244.0.11   minikube
flashsale-rs-yyyyy   1/1     Running   10.244.0.12   minikube
flashsale-rs-zzzzz   1/1     Running   10.244.0.13   minikube
```

Since the cluster contains one node, all Pods run on:

```text
minikube
```

---

# Step 13: Access the Flask Application

The Service is a `ClusterIP` Service.

For local Minikube development, run:

```powershell
minikube service flashsale-svc --url
```

Minikube provides a local URL such as:

```text
http://127.0.0.1:xxxxx
```

Keep the terminal running while using the generated URL.

Open the URL in a browser.

The `/` endpoint should return:

```json
{
  "message": "Welcome to Big Sale!",
  "pod": "flashsale-rs-pwhnd",
  "ts": 1790845764.38748
}
```

This confirms that the Flask application is running inside Kubernetes.

---

# Step 14: Test the `/buy` Endpoint

Open:

```text
/buy
```

or:

```text
/buy?user=123
```

Example:

```text
http://127.0.0.1:xxxxx/buy?user=123
```

Example response:

```json
{
  "status": "success",
  "item": "Shoes",
  "user": "123",
  "served_by_pod": "flashsale-rs-pwhnd",
  "time": "09:10:15"
}
```

The item is randomly selected.

The `served_by_pod` field shows which Pod served the request.

This demonstrates the Flash Sale checkout functionality.

---

# Step 15: Test the `/health` Endpoint

Open:

```text
/health
```

Example:

```text
http://127.0.0.1:xxxxx/health
```

Expected response:

```json
{
  "status": "healthy",
  "pod": "flashsale-rs-pwhnd"
}
```

This confirms that the health endpoint is working correctly.

The same endpoint is used by the readiness and liveness probes.

---

# Step 16: Scale the ReplicaSet to 5 Replicas

Initially, the ReplicaSet contains:

```text
3 replicas
```

Scale it to five:

```powershell
kubectl scale rs flashsale-rs --replicas=5
```

Expected output:

```text
replicaset.apps/flashsale-rs scaled
```

Kubernetes creates two additional Pods.

The number of Pods changes from:

```text
3 → 5
```

---

# Step 17: Verify the Updated ReplicaSet

Run:

```powershell
kubectl get rs
```

Expected result:

```text
NAME           DESIRED   CURRENT   READY
flashsale-rs   5         5         5
```

This confirms that the ReplicaSet has been successfully scaled to five replicas.

---

# Step 18: Verify the Five Pods

Run:

```powershell
kubectl get pods -l app=flashsale
```

The output should contain five Pods.

Example:

```text
NAME                 READY   STATUS    RESTARTS   AGE
flashsale-rs-xxxxx   1/1     Running   0          ...
flashsale-rs-yyyyy   1/1     Running   0          ...
flashsale-rs-zzzzz   1/1     Running   0          ...
flashsale-rs-aaaaa   1/1     Running   0          ...
flashsale-rs-bbbbb   1/1     Running   0          ...
```

All five Pods should eventually be:

```text
1/1   Running
```

---

# Step 19: Delete One Pod

Choose one of the five running Pods.

First list them:

```powershell
kubectl get pods -l app=flashsale
```

Then delete one:

```powershell
kubectl delete pod <pod-name>
```

For example:

```powershell
kubectl delete pod flashsale-rs-pwhnd
```

Expected output:

```text
pod "flashsale-rs-pwhnd" deleted
```

---

# Step 20: Verify ReplicaSet Self-Healing

Run:

```powershell
kubectl get pods -l app=flashsale
```

After one Pod is deleted, the ReplicaSet detects that the current number of Pods is lower than the desired number.

It automatically creates a replacement Pod.

The final state returns to:

```text
Desired Pods = 5
Current Pods = 5
Ready Pods   = 5
```

This demonstrates the self-healing capability of a ReplicaSet.

### Pod Replacement Output

![Pod Recreated](./image/Pod%20recreated.png)

The newer Pod ages compared with the older Pods demonstrate that replacement Pods were created after the deletion.

---

# Step 21: View Pod Distribution Across the Node

Run:

```powershell
kubectl get pods -l app=flashsale -o wide
```

Example:

```text
NAME                 READY   STATUS    IP            NODE
flashsale-rs-aaaaa   1/1     Running   10.244.0.9    minikube
flashsale-rs-bbbbb   1/1     Running   10.244.0.10   minikube
flashsale-rs-ccccc   1/1     Running   10.244.0.11   minikube
flashsale-rs-ddddd   1/1     Running   10.244.0.12   minikube
flashsale-rs-eeeee   1/1     Running   10.244.0.13   minikube
```

Because this exercise uses one node:

```text
Node 1: minikube

├── Pod 1
├── Pod 2
├── Pod 3
├── Pod 4
└── Pod 5
```

All five Pods are running on the same node.

---

# Step 22: Observe Which Pod Serves Requests

The Flask application returns the hostname of the Pod that handles each request.

For example:

```json
{
  "status": "success",
  "item": "Shoes",
  "user": "123",
  "served_by_pod": "flashsale-rs-pwhnd",
  "time": "09:10:15"
}
```

The `served_by_pod` field helps identify which Pod handled the request.

Multiple requests can be made to observe the Pods serving application traffic.

---

# Step 23: Inspect the ReplicaSet

Run:

```powershell
kubectl describe rs flashsale-rs
```

This displays information such as:

- ReplicaSet name
- Namespace
- Desired replicas
- Current replicas
- Ready replicas
- Selector
- Pod template
- Container image
- Resource requests and limits
- Readiness probe
- Liveness probe
- Events

The Events section also shows Pods being successfully created by the ReplicaSet controller.

---

# Step 24: Inspect a Pod

First list the Pods:

```powershell
kubectl get pods -l app=flashsale
```

Then describe a Pod:

```powershell
kubectl describe pod <pod-name>
```

Replace `<pod-name>` with the actual Pod name.

This can be used to inspect:

- Container information
- Pod IP
- Node
- Readiness probe
- Liveness probe
- Events
- Resource configuration

---

# Step 25: View Pod Logs

Run:

```powershell
kubectl logs <pod-name>
```

The logs show the Gunicorn application starting.

Example:

```text
Starting gunicorn
Listening at: http://0.0.0.0:5000
Using worker: gthread
Booting worker
```

This confirms that the application is listening on port `5000`.

---

# Step 26: Access a Pod's Container

The exercise also demonstrates accessing the container directly.

Run:

```powershell
kubectl exec -it <pod-name> -- /bin/sh
```

Inside the container, check the files:

```sh
ls
```

The application file should be present:

```text
app.py
```

Check the working directory:

```sh
pwd
```

Expected:

```text
/app
```

Exit the container using:

```sh
exit
```

---

# Scaling Demonstration

The complete scaling and self-healing process is:

```text
Initial ReplicaSet
       |
       | replicas = 3
       ↓
   3 Pods
       |
       | kubectl scale --replicas=5
       ↓
   5 Pods
       |
       | Delete 1 Pod
       ↓
   4 Pods temporarily
       |
       | ReplicaSet detects difference
       ↓
Replacement Pod created
       |
       ↓
   5 Pods again
```

This demonstrates:

- Scaling
- Self-healing
- Desired state
- Replica management

---

# Questions and Answers

## Q1. What is the initial number of replicas in the ReplicaSet?

**Answer:**

The initial number of replicas is:

```text
3
```

This is defined using:

```yaml
replicas: 3
```

---

## Q2. How many Pods are running after applying the ReplicaSet configuration?

**Answer:**

Three Pods are created.

```text
3 replicas = 3 Pods
```

---

## Q3. What happens when you scale the ReplicaSet to 5 replicas?

**Answer:**

Kubernetes creates two additional Pods to meet the desired number of replicas.

```text
3 Pods → 5 Pods
```

The ReplicaSet now maintains five Pods.

---

## Q4. What happens when you delete one Pod?

**Answer:**

Kubernetes automatically creates a new Pod to replace the deleted Pod.

For example:

```text
5 Pods
   ↓
Delete 1 Pod
   ↓
4 Pods temporarily
   ↓
ReplicaSet creates replacement
   ↓
5 Pods
```

The desired number of replicas remains five.

---

## Q5. How does Kubernetes maintain the desired number of replicas?

**Answer:**

Kubernetes continuously monitors the actual number of Pods and compares it with the desired number of replicas defined in the ReplicaSet.

If there is a discrepancy, the ReplicaSet controller creates or deletes Pods to reach the desired state.

For example:

```text
Desired = 5
Current = 4

Difference = 1

ReplicaSet creates 1 Pod.
```

The final state becomes:

```text
Desired = 5
Current = 5
```

---

## Q6. How many nodes are running?

**Answer:**

One node is running.

```text
Node count = 1
```

The cluster was started using:

```powershell
minikube start --nodes=1 --driver=docker
```

---

## Q7. Where are the Pods running with respect to nodes?

**Answer:**

All five Pods are running on the single Minikube node.

```text
Node 1: minikube

├── Pod 1
├── Pod 2
├── Pod 3
├── Pod 4
└── Pod 5
```

This can be verified using:

```powershell
kubectl get pods -l app=flashsale -o wide
```

The `NODE` column shows:

```text
minikube
```

for all five Pods.

---

# Additional Challenges

## Challenge 1: Use a Different Image

Update the image in:

```text
flashsale-replicaset.yaml
```

For example:

```yaml
image: <your-dockerhub-username>/flashsale:1.0
```

Then apply the updated configuration:

```powershell
kubectl apply -f flashsale-replicaset.yaml
```

---

## Challenge 2: Create a Deployment Instead of a ReplicaSet

Create a Kubernetes Deployment that manages the Flash Sale application.

A Deployment can be used to manage ReplicaSets and provides additional deployment functionality.

---

## Challenge 3: Inspect the ReplicaSet

Run:

```powershell
kubectl describe rs flashsale-rs
```

Observe:

- Desired replicas
- Current replicas
- Ready replicas
- Selector
- Pod template
- Events

---

## Challenge 4: Inspect Pods

Run:

```powershell
kubectl describe pod <pod-name>
```

Observe:

- Container information
- IP address
- Node
- Readiness probe
- Liveness probe
- Events

---

# Useful Commands

## Check Minikube Status

```powershell
minikube status
```

## Start Minikube

```powershell
minikube start --nodes=1 --driver=docker
```

## Stop Minikube

```powershell
minikube stop
```

## Delete Minikube

```powershell
minikube delete
```

## Check Nodes

```powershell
kubectl get nodes
```

## Check Flash Sale Pods

```powershell
kubectl get pods -l app=flashsale
```

## Check Pods with Node Information

```powershell
kubectl get pods -l app=flashsale -o wide
```

## Check ReplicaSets

```powershell
kubectl get rs
```

## Describe ReplicaSet

```powershell
kubectl describe rs flashsale-rs
```

## Scale ReplicaSet

```powershell
kubectl scale rs flashsale-rs --replicas=5
```

## Delete a Pod

```powershell
kubectl delete pod <pod-name>
```

## View Pod Logs

```powershell
kubectl logs <pod-name>
```

## Execute a Command Inside a Pod

```powershell
kubectl exec -it <pod-name> -- /bin/sh
```

## Check Services

```powershell
kubectl get svc
```

## Check Flash Sale Service

```powershell
kubectl get svc flashsale-svc
```

## Access Flash Sale Service

```powershell
minikube service flashsale-svc --url
```

---

# Technologies Used

- Python
- Flask
- Gunicorn
- Docker
- Kubernetes
- Minikube
- kubectl
- ReplicaSets
- Kubernetes Services

---

# Architecture

```text
                         User
                           |
                           ↓
                   flashsale-svc
                     ClusterIP
                      Port 80
                           |
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
       Pod 1             Pod 2            Pod 3
          |                |                |
          ↓                ↓                ↓
       Flask             Flask            Flask
        App               App              App
          |                |                |
          └────────────────┼────────────────┘
                           |
                           ↓
                     ReplicaSet
                           |
                           ↓
                  Maintains desired
                   number of Pods
```

After scaling to five replicas:

```text
                    flashsale-svc
                          |
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
        Pod 1           Pod 2           Pod 3
          ↓               ↓               ↓
        Flask           Flask           Flask
          |
          ├───────────────────────┐
          ↓                       ↓
        Pod 4                   Pod 5
          |                       |
        Flask                   Flask

                 All Pods
                     |
                     ↓
              Minikube Node
```

---

# Flash Sale Scaling Scenario

### Normal Traffic

```text
Normal Traffic
      ↓
3 Pods
```

### Traffic Spike

```text
Flash Sale
     ↓
High Traffic
     ↓
Scale ReplicaSet
     ↓
5 Pods
```

### Pod Failure

```text
5 Pods
  ↓
1 Pod deleted
  ↓
4 Pods temporarily
  ↓
ReplicaSet detects difference
  ↓
Replacement Pod created
  ↓
5 Pods restored
```

This demonstrates how ReplicaSets maintain the desired application state.

---

# Final Learning Outcomes

After completing this exercise, the following concepts were demonstrated:

- Creating a Flask application for a simulated flash sale
- Containerizing the application using Docker
- Building the `flashsale:1.0` Docker image
- Loading the image into Minikube
- Creating a Kubernetes ReplicaSet
- Running multiple replicas of the same Flask application
- Creating a Kubernetes Service
- Scaling a ReplicaSet from 3 to 5 replicas
- Using readiness probes
- Using liveness probes
- Observing Pods using `kubectl get pods`
- Observing node placement using `kubectl get pods -o wide`
- Deleting a Pod manually
- Observing ReplicaSet self-healing
- Inspecting ReplicaSet configuration using `kubectl describe`
- Viewing Pod logs
- Accessing a Pod's container using `kubectl exec`
- Testing the `/` endpoint
- Testing the `/buy` endpoint
- Testing the `/health` endpoint
- Understanding how replicas can help handle increased application demand

---

# Conclusion

This exercise demonstrated how Kubernetes ReplicaSets can be used to run multiple instances of a Flask application on a single-node Minikube cluster.

The application was initially deployed with three replicas and then scaled to five replicas.

When one Pod was deleted, the ReplicaSet automatically created a replacement Pod to maintain the desired number of replicas.

The Flash Sale application also demonstrated:

```text
Multiple Pods
      +
Scaling
      +
Self-Healing
      +
Health Checks
      +
Service Access
```

Therefore, the exercise demonstrated the basic principles of Kubernetes replica-based scalability and resiliency in a practical e-commerce flash-sale scenario.