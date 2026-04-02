pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        IMAGE_NAME = 'aceest-fitness'
        PYTHON_BIN = 'python3'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    ${PYTHON_BIN} -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint & Build Validation') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m compileall app.py src tests
                    ruff check app.py src tests
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --junitxml=pytest-report.xml
                '''
            }
        }

        stage('Docker Build') {
            when {
                expression {
                    sh(script: 'command -v docker >/dev/null 2>&1', returnStatus: true) == 0
                }
            }
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'pytest-report.xml', skipPublishingChecks: true
            cleanWs deleteDirs: true, disableDeferredWipeout: true
        }
        success {
            githubNotify context: 'Jenkins CI',
                         description: 'All stages passed',
                         status: 'SUCCESS',
                         credentialsId: 'github-token'
        }
        failure {
            githubNotify context: 'Jenkins CI',
                         description: 'Build failed',
                         status: 'FAILURE',
                         credentialsId: 'github-token'
        }
    }
}