?variant="document" title="Updated Jenkinsfile" id="58321"}
pipeline {
    agent any

    environment {
        PYTHON = 'C:/Users/ROOPA/AppData/Local/Programs/Python/Python312/python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'MediQueue source code checked out successfully'
            }
        }

        stage('Check Python') {
            steps {
                bat '"%PYTHON%" --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install --upgrade pip'
                bat '"%PYTHON%" -m pip install -r requirements.txt'
                bat '"%PYTHON%" -m pip install pytest'
            }
        }

        stage('Validate Application') {
            steps {
                bat '"%PYTHON%" -m compileall app'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"%PYTHON%" -m pytest -v'
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