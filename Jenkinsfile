// 代码仓库地址
env.GIT_URL = 'http://127.0.0.1:8081/root/gitlab_web_hook.git'
// 要构建的分支
env.BRANCHES = 'main'
// docker镜像仓库命名空间
env.Aliyun_Repo_Name_Space = 'develop_bigbigliu/'
// docker镜像仓库
env.Aliyun_Repo = 'registry.cn-zhangjiakou.aliyuncs.com/'
// gitlab 凭证id
env.CREDENTIALSID = 'gitlab_repo_hello_echo'
// 服务名
env.ServiceName = 'gitlab_web_hook'
// 镜像仓库凭证
env.Image_CREDENTIALSID = 'alibaba_repo'
// k8s master主机地址
env.K8S_MASTER_HOST = '127.0.0.1'
// k8s master 登录凭证
env.K8s_Master_CREDENTIALSID = 'k8s_master'
// k8s NameSpace
env.NAMESPACE = 'default'

node {
    environment {
        image_name = ""
    }

    stage('Source') {
        echo "start clone code"

        // 克隆代码
        git  branch: env.BRANCHES, credentialsId: env.CREDENTIALSID, url: env.GIT_URL
        
        echo "clone code end"
    }
    stage('Test') { 
        echo "test start"
        echo "test end"
    }
    stage('Build') {
        echo "build start"

        // 获取tag
        def git_tag = sh(script: 'git describe --always --tag', returnStdout: true).trim()

        container_full_name = env.ServiceName + ':' + git_tag
        println container_full_name

        repository = env.Aliyun_Repo + env.Aliyun_Repo_Name_Space + env.ServiceName + ':' + git_tag
        env.image_name = repository
        println repository

        // 登录镜像, 'ali_docker_registry'为jenkins 里配置hub仓库的全局凭证，用这个可以登录镜像仓库
        // docker.withRegistry(env.Aliyun_Repo, env.Image_CREDENTIALSID) {
        //     def customImage = docker.build(repository)
        //     customImage.push()
        // }
        
        // 使用jenkisn凭证里保存的账号密码
        withCredentials([usernamePassword(credentialsId: env.Image_CREDENTIALSID, usernameVariable: "username", passwordVariable: "password")]){
            sh 'pwd && ls -alh'
            sh 'printenv'
            sh "docker login --username=$username --password=$password registry.cn-zhangjiakou.aliyuncs.com"
            sh "docker build -t ${repository} ."
            sh "docker push ${repository}"
        }

        echo "build end"
    }
    stage('Deploy') { 
        echo "deploy start"

        withCredentials([usernamePassword(credentialsId: env.K8s_Master_CREDENTIALSID, usernameVariable: "username", passwordVariable: "password")]){
            def remote = [:]
            remote.name = 'root'
            remote.host = env.K8S_MASTER_HOST
            remote.user = username
            remote.password = password
            remote.allowAnyHosts = true

            test_commond = 'kubectl set image deployment/gitlabwebhook container-0=' + env.image_name
            sshCommand remote: remote, command: test_commond
        }

        echo "deploy end"
    }
    stage('Notification') {
        // http request 插件
         def requestBody = [
            "service_name": env.ServiceName,
            "jenkins_url": env.BUILD_URL,
            "image": env.image_name,
            "status": "Success",
         ]
         def response = httpRequest \
                    httpMode: "POST",
                    ignoreSslErrors: true,
                    contentType: 'APPLICATION_JSON',
                    requestBody: groovy.json.JsonOutput.toJson(requestBody),
                    url: "http://127.0.0.1:30003/webhook/jenkins"
        
        println response.content

        echo "Success"
    }
}
