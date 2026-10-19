import docker

client = docker.from_env()

container = client.containers.run(
    "flask-apparmor",
    name="flask-apparmor-test",
    ports={"5000/tcp": 5002},
    detach=True
)

print(f"Container started: {container.short_id}")

try:
    # Test reading a sensitive file
    exit_code, output = container.exec_run(
        ["cat", "/etc/passwd"]
    )
    print(f"\nRead /etc/passwd: Exit code {exit_code}")
    print(output.decode())

    # Test executing a shell
    exit_code, output = container.exec_run(
        ["/bin/bash", "-c", "echo Shell executed"]
    )
    print(f"\nExecute /bin/bash: Exit code {exit_code}")
    print(output.decode())

finally:
    container.stop()
    container.remove()
    print("Container stopped and removed.")