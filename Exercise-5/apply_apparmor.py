import docker

# Connect to Docker Desktop
client = docker.from_env()

# Build the Docker image
print("Building Flask image...")
client.images.build(path=".", tag="flask-apparmor")

print("Starting Flask container...")
container = client.containers.run(
    "flask-apparmor",
    name="flask-apparmor-sdk",
    ports={"5000/tcp": 5002},
    detach=True
)

print(f"Container started: {container.short_id}")

# Verify container configuration
container_info = client.api.inspect_container(container.id)
print("Container status:", container_info["State"]["Status"])
print("Port configuration:", container_info["HostConfig"]["PortBindings"])

# Stop and remove the test container
container.stop()
container.remove()

print("Container stopped and removed.")