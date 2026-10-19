# Exercise 8: Creating a Hello World Jenkins Job

## Aim
To create a simple shell script, upload it to GitHub, and execute it using a Jenkins Freestyle project.

## Prerequisites
- Git and GitHub
- Docker
- Jenkins running at `http://localhost:8080`

## 1. Create the Shell Script
Create `hello-world.sh` with the following content:

```bash
#!/bin/bash
echo "Hello, Jenkins!"
```

## 2. Version Control Using Git
Initialize a Git repository, stage the script, and commit the changes.

## 3. Push to GitHub
Upload the script to the public GitHub repository `devops-sample-code`.

## 4. Configure the Jenkins Job
- Open Jenkins at `http://localhost:8080`.
- Create a new **Freestyle project** named `HelloWorld`.
- Under **Source Code Management**, select Git and provide the repository URL.
- Under **Build Steps**, select **Execute shell** and enter:

```bash
sh hello-world.sh
```

## 5. Execute and Verify
Click **Build Now**, then open the build's **Console Output**.

Expected output:

```text
Hello, Jenkins!
Finished: SUCCESS
```

## Result
Created a shell script, stored it in GitHub, and executed it through a Jenkins Freestyle project.
