pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: docker-builder
spec:
  containers:
    - name: docker
      image: docker:24.0.2-dind
      securityContext:
        privileged: true
      volumeMounts:
        - name: docker-graph-storage
          mountPath: /var/lib/docker
    - name: builder
      image: docker:24.0.2-cli
      command:
        - cat
      tty: true
      env:
        - name: DOCKER_HOST
          value: tcp://localhost:2375
  volumes:
    - name: docker-graph-storage
      emptyDir: {}
"""
        }
    }

    environment {
        IMAGE_NAME = 'balakancharla79/flask-k3s-app'
        DOCKER_CREDENTIALS_ID = 'BalaDockerTKN'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                container('builder') {
                    sh '''
                    docker version
                    docker build -t $IMAGE_NAME:latest .
                    '''
                }
            }
        }

        stage('Authenticate and Push') {
            steps {
                container('builder') {
                    withCredentials([usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS_ID}",
                        usernameVariable: 'U',
                        passwordVariable: 'P'
                    )]) {
                        sh '''
                        echo "$P" | docker login -u "$U" --password-stdin
                        docker push $IMAGE_NAME:latest
                        '''
                    }
                }
            }
        }
        stage('Deploy to K3s') {
            steps {
                container('builder') {
                    sh '''
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    '''
                }
            }
        }
    }
}
