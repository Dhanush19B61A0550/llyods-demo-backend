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
            steps {
                script {
                    def resourceGroup = credentials('RESOURCE_GROUP')
                    def webAppName = credentials('WEB_APP_NAME')
                    bat "az webapp deploy --resource-group ${resourceGroup} --name ${webAppName} --src-path target\\*.jar --type jar"
                }
            }
        }
    }
}
