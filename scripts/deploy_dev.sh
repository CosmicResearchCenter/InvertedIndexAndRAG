#!/bin/bash

# 项目目录
frontend_dir="./web"
backend_dir="./backend"

# docker镜像名
frontend_image_name="chat2anything_dev_frontend"
backend_image_name="chat2anything_dev_backend"

# docker容器名
container_names=("chat2anything_container_dev_frontend" "chat2anything_container_dev_backend")
frontend_container_name="${container_names[0]}"
backend_container_name="${container_names[1]}"

# 日志文件
log_file="deploy.log"

# 日志记录函数
log() {
    echo "$(date "+%Y-%m-%d %H:%M:%S") - $1" | tee -a $log_file
}

# 项目根目录
project_root=$(cd $(dirname $0)/.. && pwd)
cd "$project_root"

# 检查端口占用
check_port() {
    if lsof -i:$1 >/dev/null; then
        log "端口 $1 已被占用，无法启动容器"
        exit 1
    fi
}

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

# 停止并删除旧容器
# 停止并删除旧容器（处理所有状态的容器）
for container_name in "${container_names[@]}"; do
    # 检查容器是否存在（包括已停止的容器）
    if [ "$(docker ps -a -q -f name=$container_name)" ]; then
        log "发现旧容器 $container_name..."

        # 尝试停止旧容器
        log "停止旧容器 $container_name..."
        if docker stop $container_name >/dev/null 2>&1; then
            log "停止旧容器 $container_name 成功"
        else
            log "停止旧容器 $container_name 失败或未运行"
        fi

        # 尝试删除旧容器
        log "删除旧容器 $container_name..."
        if docker rm $container_name >/dev/null 2>&1; then
            log "删除旧容器 $container_name 成功"
        else
            log "删除旧容器 $container_name 失败"
            exit 1
        fi
    else
        log "未发现需要删除的容器 $container_name"
    fi
done

# 启动前检查端口占用
check_port 12345
check_port 9988

# 启动容器
log "启动前端容器"
if docker run -d -p 12345:80 --name $frontend_container_name $frontend_image_name; then
    log "启动 $frontend_container_name 容器完成"
else
    log "启动 $frontend_container_name 容器失败"
    exit 1
fi

log "启动后端容器"
if docker run -d -p 9988:9988 --name $backend_container_name $backend_image_name; then
    log "启动 $backend_container_name 容器完成"
else
    log "启动 $backend_container_name 容器失败"
    exit 1
fi

log "部署完成"