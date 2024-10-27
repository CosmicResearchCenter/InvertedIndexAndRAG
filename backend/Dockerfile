# 使用 Python 3.12 作为基础镜像
FROM python:3.12

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 到工作目录
COPY requirements.txt .

# 安装依赖包
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将项目文件复制到容器中
COPY . .

# 将 .env 文件复制到容器的工作目录
COPY .env .env



# 运行 Alembic 迁移命令并启动应用程序
CMD ["sh", "-c", "alembic upgrade head && python main.py"]
