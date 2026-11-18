pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Automated tests') {
            steps {
                sh '. .venv/bin/activate && pytest -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Application validation') {
            steps {
                sh '. .venv/bin/activate && python -m compileall -q app'
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'requirements.txt,Dockerfile,kubernetes/*.yaml', fingerprint: true
        }
    }
}
