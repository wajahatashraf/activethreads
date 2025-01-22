pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  environment {
    DOCKER_IMAGE = "flask-city-api"  // Ensure this is in lowercase
    DOCKER_CONTAINER_NAME = "cityapi"
    REPO_URL = "https://github.com/wajahatashraf/flaskapi.git"
  }

  stages {
    stage('Stop Existing Container') {
      steps {
        bat "docker stop ${DOCKER_CONTAINER_NAME} || exit 0"
      }
    }
    stage('Remove Existing Container') {
      steps {
        bat "docker rm ${DOCKER_CONTAINER_NAME} || exit 0"
      }
    }
    stage('Delete Existing Image') {
      steps {
        bat "docker image rm ${DOCKER_IMAGE} || exit 0"
      }
    }
    stage('Build') {
      steps {
        bat "docker build -t ${DOCKER_IMAGE} ."
      }
    }
    stage('Deploy') {
      steps {
        // Run container with dynamic port assignment
        bat """
          docker run -d -p 3000:4000 --restart unless-stopped ^
          --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE}
        """

        // Get the dynamically assigned host port
        def dynamicPort = bat(script: "docker port ${DOCKER_CONTAINER_NAME} 5000 | awk -F: '{print \$2}'", returnStdout: true).trim()

        // Build the URL with the dynamic port
        def dockerUrl = "http://localhost:${dynamicPort}"

        // Print the URL to the console
        echo "Docker container is running at: ${dockerUrl}"
      }
    }
  }
}
