# demo_project + script_kit，从仓库根目录构建
# 使用方式：在仓库根目录执行 docker build -t script_kit_demo . && docker run -p 8000:8000 script_kit_demo
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# 使用仓库根目录的 requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY script_kit /app/script_kit
COPY demo_project /app/demo_project

WORKDIR /app/demo_project
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
