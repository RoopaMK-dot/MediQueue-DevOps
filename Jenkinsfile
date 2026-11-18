
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'MediQueue source code checked out'
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                if exist requirements.txt (
                    bat python -m pip install -r requirements.txt
                ) else (
                    echo requirements.txt not found - skipping
                )
                '''
            }
        }

        stage('Validate Application') {
            steps {
                bat 'python -m compileall app'
            }
        }
    }

    post {
        success {
            echo 'MediQueue Pipeline Successful!'
        }
        failure {
            echo 'MediQueue Pipeline Failed!'
        }
    }
}
