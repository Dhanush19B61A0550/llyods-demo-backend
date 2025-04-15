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
<<<<<<< HEAD
                script {
                    def resourceGroup = credentials('RESOURCE_GROUP')
                    def webAppName = credentials('WEB_APP_NAME')
                    bat "az webapp deploy --resource-group ${resourceGroup} --name ${webAppName} --src-path target\\*.jar --type jar"
                }
=======
                bat "az webapp deploy --resource-group ${RESOURCE_GROUP} --name ${WEB_APP_NAME} --src-path target\\ems-backend-0.0.1-SNAPSHOT.jar --type jar"
>>>>>>> 2266ff67a876ac4d74b2656241b173401b749e98
            }
        }
    }
}
