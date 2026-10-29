
pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                bat 'py -3 --version'
                bat 'py -3 -m venv .venv-ci'
                bat '.venv-ci\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '.venv-ci\\Scripts\\python.exe -m pip install -r requirements.txt'
                bat '.venv-ci\\Scripts\\python.exe -m pip install pytest'
            }
        }

        stage('Run tests') {
            steps {
                bat '.venv-ci\\Scripts\\python.exe -m pytest -q'
            }
        }

        stage('Build Docker image') {
            steps {
                bat 'docker build -t employee-leave-app:%BUILD_NUMBER% .'
            }
        }
    }
}
