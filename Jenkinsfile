pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                python setup.py sdist bdist_wheel
                echo 'Building'
            }
        }
        stage('Test') {
            steps {
                #!/bin/bash
                echo $PATH
                echo $HOME
                /Users/coltongarelli/anaconda3/bin/activate PlateMapper
                chmod ug+x /app/local/anaconda3/bin/activate
                pytest --junitxml results.xml test_one.py

            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying'
            }
        }
    }
    post {
        always {
            echo 'This will always run'
        }
        success {
            echo 'This will run only if successful'
        }
        failure {
            echo 'This will run only if failed'
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
        }
    }
}