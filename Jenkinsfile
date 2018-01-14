node {

    checkout scm

    env.DOCKER_API_VERSION="1.23"

    sh "git rev-parse --short HEAD > commit-id"

    tag = readFile('commit-id').replace("\n", "").replace("\r", "")
    appName = "hello-service"
    registryHost = "127.0.0.1:30400/"
    imageName = "${registryHost}${appName}:${tag}"
    env.BUILDIMG=imageName

    stage "Build"

        sh "docker build -t ${imageName} -f kubernetes/Dockerfile kubernetes/"

    stage "Push"

        sh "docker push ${imageName}"

    stage "Deploy"

        sh "kubectl apply -f kubernetes/service.yaml"
        sh "sed 's#hello-service:v1#'$BUILDIMG'#' kubernetes/deployment.yaml | kubectl apply -f -"
        sh "kubectl rollout status deployment/hello-service"
}
