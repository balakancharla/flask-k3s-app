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
      command:
        - dockerd-entrypoint.sh
      args:
        - --host=tcp://0.0.0.0:2375
        - --host=unix:///var/run/docker.sock
      securityContext:
        privileged: true
      tty: true
      env:
        - name: DOCKER_TLS_CERTDIR
          value: ""
      volumeMounts:
        - name: docker-graph-storage
          mountPath: /var/lib/docker
        - name: workspace-volume
          mountPath: /home/jenkins/agent
    - name: kubectl
      image: lachlanevenson/k8s-kubectl:latest
      command:
        - cat
      tty: true
      volumeMounts:
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
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    sh '''
                    echo "Waiting for Docker daemon to be ready..."
                    export DOCKER_HOST=tcp://127.0.0.1:2375

                    i=0
                    while ! docker info > /dev/null 2>&1; do
                      i=$((i+1))
                      if [ "$i" -gt 15 ]; then
                        echo "Docker daemon not ready after waiting, exiting..."
                        exit 1
                      fi
                      echo "Waiting for Docker... ($i)"
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
                        export DOCKER_HOST=tcp://127.0.0.1:2375
                        echo "$P" | docker login -u "$U" --password-stdin
                        docker push $IMAGE_NAME:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to K3s') {
            steps {
                container('kubectl') {
                    sh '''
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    '''
                }
            }
        }
    }
}
