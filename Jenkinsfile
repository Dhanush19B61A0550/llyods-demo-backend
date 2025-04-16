pipeline {
    agent any
    environment {
        RESOURCE_GROUP = credentials('RESOURCE_GROUP')
        WEB_APP_NAME = credentials('WEB_APP_NAME')
        AZURE_CREDENTIALS = credentials('AZURE_CREDENTIALS')
    }
    stages {
        stage('Build') {
            steps {
                bat 'mvn clean package'
            }
        }
        stage('Test') {
            steps {
                bat 'mvn test'
            }
        }
        stage('Deploy') {
            steps {
                withCredentials([file(credentialsId: 'AZURE_CREDENTIALS', variable: 'AZURE_AUTH_LOCATION')]) {
                    bat 'powershell -Command "az login --service-principal --username (Get-Content %AZURE_AUTH_LOCATION% | ConvertFrom-Json).clientId --password (Get-Content %AZURE_AUTH_LOCATION% | ConvertFrom-Json).clientSecret --tenant (Get-Content %AZURE_AUTH_LOCATION% | ConvertFrom-Json).tenantId"'
                    bat 'az webapp deploy --resource-group %RESOURCE_GROUP% --name %WEB_APP_NAME% --src-path target\\*.jar --type jar'
                }
            }
        }
    }
}
