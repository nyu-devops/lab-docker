# Minikube Kubernetes Demo

From: [Hello Minikube | Kubernetes](https://kubernetes.io/docs/tutorials/stateless-application/hello-minikube/)

## Install Minikube

"Offical" installation instructions here: [minikube](https://github.com/kubernetes/minikube)

### macOS
```shell
brew cask install minikube
```
or
```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64 && \
  chmod +x minikube && \
  sudo mv minikube /usr/local/bin/
```
### Linux
```shell
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```

### Windows
Download the [minikube-windows-amd64.exe](https://storage.googleapis.com/minikube/releases/latest/minikube-windows-amd64.exe) file, rename it to `minikube.exe` and add it to your path.


## Install Kubectl

### macOS
```
brew install kubectl
```
or
```shell
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/darwin/amd64/kubectl && \
chmod +x ./kubectl && \
sudo mv ./kubectl /usr/local/bin/kubectl
```

### Linux
```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && \
chmod +x ./kubectl && \
sudo mv ./kubectl /usr/local/bin/kubectl
```

### Windows
Download the latest release v1.8.0 from this [link](https://storage.googleapis.com/kubernetes-release/release/v1.8.0/bin/windows/amd64/kubectl.exe).

Or if you have curl installed, use this command:
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.8.0/bin/windows/amd64/kubectl.exe
```

Windows users should add the location of `kubectl.exe` to their path.

## Start minikube
```
minikube start
```

## Create a Python Flask application
Create a simple Python Flask application and name is `app.py` with a `requirements.txt` file that installs `Flask`:

### app.py
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello Service</h1>", 200

if __name__ == '__main__':
    app.run()
```

### requirements.txt
```
Flask
```

## Create a Dockerfile
We need a `Dockerfile` to specify how to build our images

### Dockerfile
```
FROM python:2-alpine
EXPOSE 5000
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD python app.py
```

## Point to Minikube Docker Registry
This next step is extremely import so that the docker images you build are inside of the minikube vm
```
eval $(minikube docker-env)
```

Note: undo with `eval $(minikube docker-env -u)`

## Build the Docker Image
```
docker build -t hello-service:v1 .
```

## Create a Deployment
```
kubectl run hello-service --image=hello-service:v1 --port=5000
```

## Create a Service
```
kubectl expose deployment hello-service --type=LoadBalancer
```

Get the service in a  browser with:
```
minikube service hello-service
```

## Update your app
Edit your app.py file to return a new message:
```python
return "<h1>Hello New Improved Service</h1>", 200
```

Build a new version of your image:
```
docker build -t hello-service:v2 .
```

Update the image of your Deployment:
```
kubectl set image deployment/hello-service hello-service=hello-service:v2
```

Run your app again to view the new message:
```
minikube service hello-service
```

## Clean up
Now you can clean up the resources you created in your cluster:
```
kubectl delete service hello-service
kubectl delete deployment hello-service
```

Optionally, stop Minikube:
```
minikube stop
```
