pipeline { 
    environment { 
        registry = "athirak1234/python_flask" 
        registryCredential = 'dockerhub_id' 
        dockerImage = '' 
    }
    agent any 
    stages { 
        stage('Cloning our Git') { 
            steps { 
                git branch:'main', url: 'https://github.com/athiboo/python_flask_app.git' 
            }
        }
        stage('flake8') { 
            steps { 
                sh 'docker run --user $(id -u):$(id -g) --rm -v $(pwd):/src alpine/flake8:3.5.0 app.py'
            }
        } 
        stage('Bandit') { 
            steps { 
                sh 'docker run --user $(id -u):$(id -g) -v $(pwd):/src --rm secfigo/bandit bandit -r /src -f json -o /src/bandit-output.json | exit 0'
            }
        }  
        stage('Git Secret using TruffleHog') {
            steps {
                echo 'Scan the git repo using Trufflehog'
                sh 'docker run --user $(id -u):$(id -g) --rm -v "$(pwd):/proj" dxa4481/trufflehog file:///proj --json | tee trufflehog-output.json'
            }
        } 
        stage('Dockerlint') {
                    steps {
                        echo 'Dockerlint Scaning'
                        sh 'docker run --user $(id -u):$(id -g) -it --rm -v "$PWD/Dockerfile":/Dockerfile:ro redcoolbeans/dockerlint | tee dockerlint-output.json'
                    }
                }
                stage('Hadolint') {
                    steps {
                        echo 'Hadolint Scaning'
                        sh 'docker run --user $(id -u):$(id -g) -it --rm -v "$PWD/Dockerfile":/Dockerfile:ro hadolint/hadolint hadolint Dockerfile | tee hadolint-output.json'
                    }
                }
        stage('Building our image') { 
            steps { 
                script { 
                    dockerImage = docker.build registry + ":$BUILD_NUMBER" 
                }
            }
        } 
        stage('Deploy our image') { 
            steps { 
                script { 
                    docker.withRegistry( '', registryCredential ) { 
                        dockerImage.push() 
                    }
                } 
            }
        }
        
        stage('Cleaning up') { 
            steps { 
                sh "docker rmi $registry:$BUILD_NUMBER" 
            }
        } 

        stage('Deploy to Kubernetes Dev Environment') {
            steps {
                echo 'Deploy the App using Kubectl'
                //sh "sed -i 's/BUILDNUMBER/$BUILD_NUMBER/g' python-flask-deployment.yml"
                sh "sed -i 's/DEPLOYMENTENVIRONMENT/development/g' python-flask-deployment.yml"
                sh "sed -i 's/TAG/$BUILD_NUMBER/g' python-flask-deployment.yml"
                sh "kubectl apply -f python-flask-deployment.yml"
            }
        }
        stage('Promote to Production') {
            steps {
                echo "Promote to production"
            }
            input {
                message "Do you want to Promote the Build to Production"
                ok "Ok"
                submitter "athkum@gmail.com"
                submitterParameter "whoIsSubmitter"
                
            }
        }
        stage('Deploy to Kubernetes Production Environment') {
            steps {
                echo 'Deploy the App using Kubectl'
                sh "sed -i 's/development/production/g' python-flask-deployment.yml"
                sh "sed -i 's/TAG/$BUILD_NUMBER/g' python-flask-deployment.yml"
                sh "kubectl apply -f python-flask-deployment.yml"
            }
        }
    }
    post{
        always{
            archiveArtifacts artifacts: 'bandit-output.json',onlyIfSuccessful: true
        }
    }
}