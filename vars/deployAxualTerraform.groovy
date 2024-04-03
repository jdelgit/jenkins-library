def call(String cloud_credentials_id='') {
    pipeline {
        environment {
            ARM = credentials("${cloud_credentials_id}")
        }
        agent any
        stages {
            stage('Initialize') {
                steps {
                    sh 'git clone https://github.com/jdelgit/terraform-modules.git'
                    sh 'terraform -chdir=./test init --backend-config backend.conf'
                }
            }
            stage('Plan') {
                steps {
                    sh 'terraform -chdir=./test plan -out test.plan -destroy'
                }
            }
            stage('Apply plan') {
                    steps {
                        sh 'terraform -chdir=./test apply test.plan'
                    }
            }
        }
    }
}
