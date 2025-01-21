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
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                }
            }
        }
        stage('Stop Existing Container') {
            steps {
                script {
                    def containerExists = bat(script: "docker ps -a -q -f name=${DOCKER_CONTAINER_NAME}", returnStdout: true).trim()
                    if (containerExists) {
                        bat "docker stop ${DOCKER_CONTAINER_NAME}"
                    } else {
                        echo "No container named ${DOCKER_CONTAINER_NAME} exists."
                    }
                }
            }
        }
        stage('Remove Existing Container') {
            steps {
                script {
                    def containerExists = bat(script: "docker ps -a -q -f name=${DOCKER_CONTAINER_NAME}", returnStdout: true).trim()
                    if (containerExists) {
                        bat "docker rm ${DOCKER_CONTAINER_NAME}"
                    } else {
                        echo "No container named ${DOCKER_CONTAINER_NAME} exists."
                    }
                }
            }
        }
        stage('Delete Existing Image') {
            steps {
                script {
                    def imageExists = bat(script: "docker images -q ${DOCKER_IMAGE}", returnStdout: true).trim()
                    if (imageExists) {
                        bat "docker image rm ${DOCKER_IMAGE}"
                    } else {
                        echo "No image named ${DOCKER_IMAGE} exists."
                    }
                }
            }
        }
        stage('Wait for Thread Completion') {
            steps {
                script {
                    def isRunning = true
                    while (isRunning) {
                        def response = bat(script: "curl -s http://localhost:5000/check_thread", returnStdout: true).trim()
                        echo "Response from Flask: ${response}"
                        def jsonResponse = new groovy.json.JsonSlurper().parseText(response)
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
    post {
        always {
            echo 'Pipeline completed.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}