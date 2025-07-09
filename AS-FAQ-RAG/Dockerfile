# 使用官方的 Python 基礎映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝CPU版本的 PyTorch(節省image大小)
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安裝 Git (用於從 GitHub 下載資料)
RUN apt-get update && apt-get install -y git && apt-get clean

# 複製專案檔案
COPY . .

# 建立臨時目錄
RUN mkdir -p /app/temp

# 設置啟動腳本的執行權限
RUN chmod +x /app/start.sh

# 暴露應用程式埠
EXPOSE 8000

# 使用啟動腳本同時啟動 API 和自動更新服務
ENTRYPOINT ["/app/start.sh"]