pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                bat '''
                    "C:\\Users\\POTHAGALLA VAMSHI\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" --version
                    "C:\\Users\\POTHAGALLA VAMSHI\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m venv .venv-ci
                    ".venv-ci\\Scripts\\python.exe" -m pip install --upgrade pip
                    ".venv-ci\\Scripts\\python.exe" -m pip install -r requirements.txt
                    ".venv-ci\\Scripts\\python.exe" -m pip install pytest
                '''
            }
        }

        stage('Run tests') {
            steps {
                bat '".venv-ci\\Scripts\\python.exe" -m pytest -q'
            }
        }

        stage('Build Docker image') {
            steps {
                bat 'docker build -t employee-leave-app:%BUILD_NUMBER% .'
            }
        }
    }
}
