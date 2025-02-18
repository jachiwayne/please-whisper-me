pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'please-whisper-me/app'
    }

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run ${DOCKER_IMAGE} python -m pytest'  # Add tests later
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker run -d -p 5000:5000 ${DOCKER_IMAGE}'
            }
        }
    }
}
