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
      tty: true
      command:
        - dockerd-entrypoint.sh
      args:
        - --host=tcp://0.0.0.0:2375
        - --host=unix:///var/run/docker.sock
      env:
        - name: DOCKER_TLS_CERTDIR
          value: ""
      volumeMounts:
        - name: docker-graph-storage
          mountPath: /var/lib/docker
        - name: workspace-volume
          mountPath: /home/jenkins/agent
  volumes:
    - name: docker-graph-storage
      emptyDir: {}
    - name: workspace-volume
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
                container('docker') {
                    checkout scm
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    // Wait for Docker to be ready
                    sh '''
                    echo "Waiting for Docker daemon to be ready..."
                    for i in {1..15}; do
                        docker info > /dev/null 2>&1 && break
                        echo "Waiting... ($i)"
                        sleep 2
                    done
                    echo "Docker is ready!"

                    docker version
                    docker build -t $IMAGE_NAME:latest .
                    '''
                }
            }
        }

        stage('Authenticate and Push') {
            steps {
                container('docker') {
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
                container('docker') {
                    sh '''
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    '''
                }
            }
        }
    }
}
