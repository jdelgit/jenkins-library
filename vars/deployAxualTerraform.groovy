def call(String cloudCredentialsID='') {
    pipeline {
        environment {
            ARM = credentials("${cloudCredentialsID}")
        }
        agent any
        stages {
            stage('Validate & Deploy: Ontw') {
                steps {
                    python3 .'./resources/example/validation.py' 'test'
                }
            }

            // stage('Initialize') {
            //     steps {
                    // echo 'Check out Axual module'
            //         sh 'git clone https://github.com/jdelgit/terraform-modules.git'
            //         sh 'terraform -chdir=./test init --backend-config backend.conf'
            //     }
            // }
            // stage('Plan') {
            //     steps {
            //         sh 'terraform -chdir=./test plan -out test.plan'
            //     }
            // }
            // stage('Deploy approval') {
            //     steps {
            //         input 'Deploy to environment?'
            //     }
            // }
            // stage('Apply plan') {
            //         steps {
            //             sh 'terraform -chdir=./test apply test.plan'
            //         }
            // }
        }
    }
}
