pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        IMAGE_NAME = 'aceest-fitness'
        PYTHON_BIN = 'python'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                    %PYTHON_BIN% -m venv .venv
                    call .venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint & Build Validation') {
            steps {
                bat '''
                    call .venv\\Scripts\\activate
                    python -m compileall app.py src tests
                    ruff check app.py src tests
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                bat '''
                    call .venv\\Scripts\\activate
                    pytest --junitxml=pytest-report.xml
                '''
            }
        }

        stage('Docker Build') {
            when {
                expression {
                    bat(script: 'where docker', returnStatus: true) == 0
                }
            }
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
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