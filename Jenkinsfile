
pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  environment {
    DOCKER_IMAGE = "flask-city-api" // Ensure this is in lowercase
    DOCKER_CONTAINER_NAME = "cityapi"
    THREAD_CHECK_URL = "http://localhost:3000/check_thread"
  }

  stages {
  stage('Wait for Thread Completion') {
    steps {
      script {
        def isRunning = true
        def retries = 2  // Number of retries if URL does not respond

        while (isRunning) {
          def attempts = 0
          def rawResponse = ""

          while (attempts < retries) {
            try {
              // Run the curl command and capture the response body as plain text
              rawResponse = bat(
                script: "@curl -s --max-time 10 ${env.THREAD_CHECK_URL}",
                returnStdout: true
              )?.trim()

              // Log the raw response
              echo "Raw response: ${rawResponse}"

              // Check if the response indicates the thread is running
              if (rawResponse == "is_thread_running=True") {
                isRunning = true
                echo "Thread is still running. Retrying in 30 seconds..."
                sleep(30)
                break  // Break the inner loop and retry after the delay
              } else if (rawResponse == "is_thread_running=False") {
                isRunning = false
                echo "Thread has completed. Moving to the next stage."
                break  // Exit the loop since the thread has completed
              } else {
                // Handle any unexpected response
                echo "Unexpected response: ${rawResponse}. Retrying in 30 seconds..."
                attempts++
                sleep(30)  // Wait for 30 seconds before retrying
              }
            } catch (Exception e) {
              // Retry silently if any error occurs
              echo "Error occurred while checking thread status: ${e.message}. Retrying in 30 seconds..."
              attempts++
              sleep(30)  // Wait for 30 seconds before retrying
            }
          }

          // If the URL failed to respond after the retries, exit the loop
          if (attempts >= retries) {
            echo "URL did not respond after ${retries} attempts. Moving to the next stage."
            isRunning = false
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
