#!/bin/bash

# 项目目录
frontend_dir="./web"
backend_dir="./backend"

# docker镜像名
frontend_image_name="chat2anything_frontend"
backend_image_name="chat2anything_backend"

# 日志文件
log_file="deploy.log"

# 日志记录函数
log() {
    echo "$(date "+%Y-%m-%d %H:%M:%S") - $1" | tee -a $log_file
}

# 项目根目录
project_root=$(cd $(dirname $0)/.. && pwd)
cd "$project_root"

# 构建前端 Docker 镜像
log "开始构建前端 Docker 镜像"
cd "$frontend_dir"
if docker build -t $frontend_image_name .; then
    log "构建前端 Docker 镜像完成"
else
    log "构建前端 Docker 镜像失败"
    exit 1
fi

# 构建后端 Docker 镜像
cd "$project_root/$backend_dir"
log "开始构建后端 Docker 镜像"
if docker build -t $backend_image_name .; then
    log "构建后端 Docker 镜像完成"
else
    log "构建后端 Docker 镜像失败"
    exit 1
fi

cd "$project_root"
cd "docker"
# 用 docker-compose 启动容器
log "开始启动容器"
if docker-compose up -d; then
    log "启动容器成功"
else
    log "启动容器失败"
    exit 1
fi

log "部署完成"