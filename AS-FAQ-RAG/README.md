# AS-FAQ-RAG

AS-FAQ-RAG是一個基於RAG（Retrieval-Augmented Generation）技術的FAQ系統。它結合了前端網頁和後端API，提供了一個解決方案來處理常見問題的自動回答。前端網頁AS-FAQ-Web-ChatBot提供了用戶友好的界面，而後端API AS-FAQ-RAG負責處理數據檢索和生成回答。


## 介紹
本項目是AS-FAQ-RAG的後端API

## 安裝
1. 下載程式碼或複製專案
2. 可以選擇使用CLI或是Docker compose的方式執行

### CLI 安裝
1. 進入專案目錄
   ```bash
   cd AS-FAQ-RAG
   ```

2. 建立虛擬環境
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. 安裝套件
   ```bash
   pip install -r requirements.txt
   ```

4. 將 `.env.example` 檔案複製並重新命名為 `.env`，並編輯 `.env`：
   ```bash
   cp .env.example .env
   vim .env
   ``` 
   REPO_URL、TRANSLATE_API 為資料彙整程式 (update_data.py) 使用，如果沒有要用到資料彙整的功能可以不填。

5. 匯入QA資料
   參考 `combined_context_en.csv.example` 格式編輯 QA 資料，
   並另存為 `combined_context_en.csv`
   ```bash
   cp combined_context_en.csv.example combined_context_en.csv
   ``` 

6. 啟動AS-FAQ-RAG API，請使用以下命令：
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```
   (port 8000 可自行修改為其他埠)
   > [!TIP] 
   > 若是正式環境請移除 `reload` 標籤，避免 CPU 占用過高。

7. 初次啟動需等待 `vector_database.bin` 建立

### Docker compose 安裝
1. 將 `.env.example` 檔案複製並重新命名為 `.env`，並編輯 `.env`：
   ```bash
   cp .env.example .env
   vim .env
   ``` 
   REPO_URL、TRANSLATE_API 為資料彙整程式 (`update_data.py`) 使用，如果沒有要用到資料彙整的功能可以不填。 

2. 匯入QA資料
   參考 `combined_context_en.csv.example` 格式編輯 QA 資料，
   並另存為 `combined_context_en.csv`
   ```bash
   cp combined_context_en.csv.example combined_context_en.csv
   ``` 

3. 啟動
   ```bash
   sudo docker compose up -d
   ``` 

4. 初次啟動需等待 `vector_database.bin` 建立

### Docker compose 同時安裝 Web 及 API
目錄架構
```plain text
YOUR-DIR/
├── docker-compose.yml
├── AS-FAQ-RAG/
│   ├── Dockerfile
│   ├── .env
│   └── ...（其他檔案）
└── AS-FAQ-Web-ChatBot/
    ├── Dockerfile
    ├── .env
    └── ...（其他檔案）
```
1. 在第一層目錄建立 `docker-compose.yml`
    ```yaml
    services:
      api:
        build: ./AS-FAQ-RAG
        ports:
        - "4000:8000"
        env_file:
        - ./AS-FAQ-RAG/.env
        volumes:
        - ./AS-FAQ-RAG:/app
        working_dir: /app
        restart: always

      web:
        build: ./AS-FAQ-Web-ChatBot
        tty: true
        stdin_open: true
        ports:
        - "3080:3000"
        working_dir: /app
        env_file:
        - ./AS-FAQ-Web-ChatBot/.env
        restart: always
    ```

2. 移動至 `AS-FAQ-RAG/` 將 `.env.example` 檔案複製並重新命名為 `.env`，並編輯 `.env`：
   ```bash
   cd AS-FAQ-RAG
   ``` 
   ```bash
   cp .env.example .env
   vim .env
   ``` 
   REPO_URL、TRANSLATE_API 為資料彙整程式 (`update_data.py`) 使用，如果沒有要用到資料彙整的功能可以不填。 

2. 匯入QA資料
   參考 `combined_context_en.csv.example` 格式編輯 QA 資料，
   並另存為 `combined_context_en.csv`
   ```bash
   cp combined_context_en.csv.example combined_context_en.csv
   ``` 

3. 設定 `AS-FAQ-Web-ChatBot` 方式請參考另一個專案

4. 兩個專案都設定好後回到第一層啟動容器
   ```bash
   cd ..
   sudo docker compose up -d
   ``` 

## 匯入QA資料
參考 `combined_context_en.csv.example` 格式編輯 QA 資料
必須含有：
- `title`: 標題
- `context`: 中文內容
- `url`: 來源 URL
- `en_title`: 英文標題
- `en_context`: 英文內容

### 資料彙整程式
單獨執行 `update_data.py` 可以將個別CSV翻譯並合併為 combined_context_en.csv，
```bash
cd utils
python update_data.py
```
個別CSV格式參考：[AS-FAQ-Bot](https://github.com/AS-AIGC/AS-FAQ-Bot/tree/main/data/source)  
> [!WARNING]
> `combined_context_en.csv.example` 的英文翻譯為機器翻譯，不保證正確性

## 更新資料庫
1. 關閉程式或容器
2. 刪除 `vector_database.bin`
3. 更新 `combined_context_en.csv`
4. 啟動 API 程式

## RAG 設定
可於 `utils/respond.py` 設定 RAG 參數，包含搜尋文件數及提示詞。

## 使用
透過 Postman 或 curl 等開發工具連線到 API：
```bash
curl --location 'http://127.0.0.1:8000/ask' \
--data '{
   "question": "請問如何申請VPN?"
}'
```
### 預設 port
- CLI 安裝：8000
- Docker compose：4000