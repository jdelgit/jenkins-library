def call(String name = 'human') {
    pipeline {
        agent any
        stages {
            stage('Initial stage') {
                steps {
                    echo "Hello ${name}"
                }
            }
        }
    }
}
