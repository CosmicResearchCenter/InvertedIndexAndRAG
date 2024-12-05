# 使用多阶段构建
# 第一阶段：构建前端
FROM node:18 AS frontend-builder

# 设置工作目录
WORKDIR /app/web

# 将前端代码复制到容器
COPY web/ .

# 安装依赖并构建
RUN npm install --registry https://registry.npmmirror.com && npm run build

# 第二阶段：构建后端
FROM python:3.12 AS backend-builder

# 设置工作目录
WORKDIR /app/backend

# 将后端代码复制到容器
COPY backend/ .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将.env文件复制到镜像中
COPY backend/.env /app/backend/.env

# 第三阶段：生产镜像
FROM nginx:1.23

# 设置Nginx工作目录
WORKDIR /usr/share/nginx/html

# 从前端构建阶段复制构建的静态文件
COPY --from=frontend-builder /app/web/dist/ .

# 配置Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# 设置后端运行目录
WORKDIR /app/backend

# 从后端构建阶段复制后端代码
COPY --from=backend-builder /app/backend/ .

EXPOSE 80 9988


# 设置运行后端服务的命令
CMD ["sh", "-c", "nginx -g 'daemon off;' & alembic upgrade head && python main.py"]
