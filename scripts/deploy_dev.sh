#!/bin/bash

# 项目目录
frontend_dir="../web"
backend_dir="../backend"
# docker镜像名
image_name="chat2anything_dev_deploy"
# docker容器名
container_name="chat2anything_container_dev_deploy"

# 构建docker镜像
echo "开始构建docker镜像"
docker build -t $image_name .
echo "构建docker镜像完成"

# 停止并删除旧容器（如果存在）
if [ "$(docker ps -q -f name=$container_name)" ]; then
    echo "停止旧容器..."
    docker stop $container_name
    echo "删除旧容器..."
    docker rm $container_name
fi

# 启动容器
echo "启动容器"
docker run -d -p 12345:80 -p 9988:9988 --name $container_name $image_name
echo "启动容器完成"

echo "部署完成"

# 输出时间
echo "时间:$(date "+%Y-%m-%d %H:%M:%S")"

