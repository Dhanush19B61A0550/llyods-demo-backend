pipeline {
    agent any 
    environment {
        RESOURCE_GROUP = credentials('RESOURCE_GROUP')
        WEB_APP_NAME = credentials('WEB_APP_NAME')
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
                withCredentials([ 
                    string(credentialsId: 'AZURE_CLIENT_ID', variable: 'CLIENT_ID'), 
                    string(credentialsId: 'AZURE_CLIENT_SECRET', variable: 'CLIENT_SECRET'), 
                    string(credentialsId: 'AZURE_TENANT_ID', variable: 'TENANT_ID') 
                ]) {
                    bat 'az login --service-principal --username %CLIENT_ID% --password %CLIENT_SECRET% --tenant %TENANT_ID%'
                    bat 'az webapp deploy --resource-group %RESOURCE_GROUP% --name %WEB_APP_NAME% --src-path target\\*.jar --type jar'
                }
            }
        }
    }
}
