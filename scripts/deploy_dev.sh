#!/bin/bash

# 项目目录
frontend_dir="../web"
backend_dir="../backend"
# docker镜像名
image_name="chat2anything_dev_deploy"
# docker容器名
container_name="chat2anything_container_dev_deploy"

# 日志文件
log_file="deploy.log"

# 记录日志的函数
log() {
    echo "$(date "+%Y-%m-%d %H:%M:%S") - $1" | tee -a $log_file
}

# 构建docker镜像
log "开始构建docker镜像"
if docker build -t $image_name .; then
    log "构建docker镜像完成"
else
    log "构建docker镜像失败"
    exit 1
fi

# 停止并删除旧容器（如果存在）
if [ "$(docker ps -q -f name=$container_name)" ]; then
    log "停止旧容器..."
    if docker stop $container_name; then
        log "停止旧容器成功"
    else
        log "停止旧容器失败"
        exit 1
    fi

    log "删除旧容器..."
    if docker rm $container_name; then
        log "删除旧容器成功"
    else
        log "删除旧容器失败"
        exit 1
    fi
fi

# 启动容器
log "启动容器"
if docker run -d -p 12345:80 -p 9988:9988 --name $container_name $image_name; then
    log "启动容器完成"
else
    log "启动容器失败"
    exit 1
fi

log "部署完成"

