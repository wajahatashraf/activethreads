pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  environment {
    DOCKER_IMAGE = "flask-city-api" // Ensure this is in lowercase
    DOCKER_CONTAINER_NAME = "cityapi"
    REPO_URL = "https://github.com/wajahatashraf/flaskapi.git"
  }

  stages {
    stage('Stop Existing Container') {
      steps {
        script {
          // Check if the container is running
          def existingPort = sh(script: "docker port ${DOCKER_CONTAINER_NAME} 5000 | awk -F: '{print \$2}'", returnStdout: true).trim()

          // If the container is running, print the port
          if (existingPort) {
            echo "The existing container is running on port: ${existingPort}"
          } else {
            echo "The container is not running."
          }
        }
      }
    }
    stage('Remove Existing Container') {
      steps {
        bat "docker stop ${DOCKER_CONTAINER_NAME} || exit 0"
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
        bat """
          docker run -d -p 3000:5000 --restart unless-stopped ^
          --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE}
        """
      }
    }
  }
}
