#!/bin/bash

# 项目目录
frontend_dir="./web"
backend_dir="./backend"
# docker镜像名
frontend_image_name="chat2anything_dev_frontend"

backend_image_name="chat2anything_dev_backend"

# docker容器名
frontend_container_name="chat2anything_container_dev_frontend"
backend_container_name="chat2anything_container_dev_backend"

# 日志文件
log_file="deploy.log"

# 记录日志的函数
log() {
    echo "$(date "+%Y-%m-%d %H:%M:%S") - $1" | tee -a $log_file
}

# 退回到项目根目录
cd $(dirname $0)/..

# 构建docker镜像
log "开始构建前端docker镜像"
# 进入前端目录
cd $frontend_dir
if docker build -t $frontend_image_name .; then
    log "构建前端docker镜像完成"
else
    log "构建前端docker镜像失败"
    exit 1
fi

# 进入项目根目录
cd $(dirname $0)/..

# 进入后端目录
cd $backend_dir 

# 构建docker镜像
log "开始构建后端docker镜像"
if docker build -t $backend_image_name .; then
    log "构建后端docker镜像完成"
else
    log "构建后端docker镜像失败"
    exit 1
fi

# 停止并删除旧容器（如果存在）
for container_name in $frontend_container_name $backend_container_name; do
    if [ "$(docker ps -q -f name=$container_name)" ]; then
        log "停止旧容器 $container_name..."
        if docker stop $container_name; then
            log "停止旧容器 $container_name 成功"
        else
            log "停止旧容器 $container_name 失败"
            exit 1
        fi

        log "删除旧容器 $container_name..."
        if docker rm $container_name; then
            log "删除旧容器 $container_name 成功"
        else
            log "删除旧容器 $container_name 失败"
            exit 1
        fi
    fi
done

# 启动容器
log "启动容器"
if docker run -d -p 12345:80 --name $frontend_container_name $frontend_image_name; then
    log "启动 $frontend_container_name 容器完成"
else
    log "启动 $frontend_container_name 容器失败"
    exit 1
fi

if docker run -d -p 9988:9988 --name $backend_container_name $backend_image_name; then
    log "启动 $backend_container_name 容器完成"
else
    log "启动 $backend_container_name 容器失败"
    exit 1
fi


log "部署完成"

