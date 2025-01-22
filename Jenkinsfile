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
            script: '@curl -s --max-time 10 http://localhost:3000/check_thread',
            returnStdout: true
          )?.trim()

          // Log the raw response
          echo "Raw response: ${rawResponse}"

          // Parse JSON response directly
          def jsonResponse = new JsonSlurper().parseText(rawResponse)

          // Update the isRunning status based on the parsed response
          isRunning = jsonResponse.is_thread_running ?: false

          if (isRunning) {
            echo "Thread is still running. Retrying in 30 seconds..."
            sleep(30)
          }
        } catch (Exception e) {
          // Retry silently if any error occurs
          echo "Error occurred while checking thread status: Retrying in 30 seconds..."
          sleep(30)
        }
      }
      echo "Thread has completed. Moving to the next stage."
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
