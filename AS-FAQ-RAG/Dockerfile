# 使用官方的 Python 基礎映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案檔案
COPY . .

# 暴露應用程式埠
EXPOSE 8000

# 啟動 FastAPI 應用程式
# dev
# ENTRYPOINT ["uvicorn", "api:app", "--reload", "--reload-exclude", ".venv", "--reload-exclude", ".git", "--host", "0.0.0.0", "--port", "8000"]
# prod
ENTRYPOINT ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]