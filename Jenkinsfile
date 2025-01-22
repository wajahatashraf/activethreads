import groovy.json.JsonSlurper

pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  environment {
    DOCKER_IMAGE = "flask-city-api" // Ensure this is in lowercase
    DOCKER_CONTAINER_NAME = "cityapi"
    REPO_URL = "https://github.com/wajahatashraf/activethreads.git"
  }

  stages {
    stage('Wait for Thread Completion') {
      steps {
        script {
          def isRunning = true
          while (isRunning) {
            try {
              // Run the curl command and capture only the response body
              def rawResponse = bat(
                script: '@curl -s http://localhost:3000/check_thread',
                returnStdout: true
              ).trim()

              // Debugging: Show the raw response
              echo "Raw response: ${rawResponse}"

              // Parse JSON response
              def jsonResponse = new JsonSlurper().parseText(rawResponse)

              // Check if the key 'is_thread_running' exists
              if (!jsonResponse.containsKey('is_thread_running')) {
                echo "Warning: The response does not contain the 'is_thread_running' key:\n${rawResponse}"
              } else {
                // Update the isRunning status
                isRunning = jsonResponse.is_thread_running
              }

              if (isRunning) {
                echo "Thread is still running. Retrying in 30 seconds..."
                sleep 30
              } else {
                echo "Thread has completed. Moving to the next stage."
              }
            } catch (Exception e) {
              echo "Error while checking thread status: ${e.message}. Retrying in 30 seconds..."
              sleep 30
            }
          }
        }
      }
    }

    stage('Stop Existing Container') {
      steps {
        script {
          def stopResult = bat(script: "docker stop ${DOCKER_CONTAINER_NAME}", returnStatus: true)
          if (stopResult != 0) {
            echo "No container to stop or an error occurred."
          }
        }
      }
    }

    stage('Remove Existing Container') {
      steps {
        script {
          def removeResult = bat(script: "docker rm ${DOCKER_CONTAINER_NAME}", returnStatus: true)
          if (removeResult != 0) {
            echo "No container to remove or an error occurred."
          }
        }
      }
    }

    stage('Delete Existing Image') {
      steps {
        script {
          def imageResult = bat(script: "docker image rm ${DOCKER_IMAGE} --force", returnStatus: true)
          if (imageResult != 0) {
            echo "No image to remove or an error occurred."
          }
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
