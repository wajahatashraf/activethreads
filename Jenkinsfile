import groovy.json.JsonSlurper

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
    stage('Wait for Thread Completion') {
      steps {
        script {
          def isRunning = true
          while (isRunning) {
            // Check the status of the thread
            def response = bat(script: "curl -s http://localhost:5000/check_thread", returnStdout: true).trim()
            def jsonResponse = new JsonSlurper().parseText(response)
            isRunning = jsonResponse.is_thread_running
            if (isRunning) {
              echo "Thread is still running. Waiting..."
              sleep 30 // Wait for 30 seconds before checking again
            }
          }
          echo "Thread has completed."
        }
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