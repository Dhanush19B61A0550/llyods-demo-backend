pipeline {
    agent any
    
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
            environment {
                RESOURCE_GROUP = credentials('RESOURCE_GROUP')
                WEB_APP_NAME = credentials('WEB_APP_NAME')
            }
            steps {
                bat "az webapp deploy --resource-group ${RESOURCE_GROUP} --name ${WEB_APP_NAME} --src-path target/*.jar --type jar"
            }
        }
    }
}
