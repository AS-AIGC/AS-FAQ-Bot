# AS-FAQ-RAG

## 繁體中文
AS-FAQ-RAG是一個基於 RAG（Retrieval-Augmented Generation）技術的 FAQ 系統。它結合了前端網頁和後端 API，提供了一個解決方案來處理常見問題的自動回答。前端網頁 AS-FAQ-Web-ChatBot 提供了用戶友好的界面，而後端 API AS-FAQ-RAG 負責處理數據檢索和生成回答。

## English
AS-FAQ-RAG is an FAQ system based on RAG (Retrieval-Augmented Generation) technology. It combines a front-end web interface and a back-end API to provide a solution for automatically answering frequently asked questions. The front-end web page, AS-FAQ-Web-ChatBot, offers a user-friendly interface, while the back-end API, AS-FAQ-RAG, handles data retrieval and generates responses.

---

## 介紹 | Introduction

### 繁體中文
本項目是 AS-FAQ-RAG 的後端 API。

### English
This project is the back-end API for AS-FAQ-RAG.

---

## 安裝 | Installation

> **繁體中文**  
> 1. 下載程式碼或複製專案  
> 2. 可以選擇使用 CLI 或是 Docker compose 的方式執行  

> **English**  
> 1. Download or clone the repository  
> 2. You can choose to run it via CLI or Docker Compose  

---

### CLI 安裝 | CLI Installation

#### 繁體中文
1. 進入專案目錄
   ```bash
   cd AS-FAQ-RAG

2. 建立虛擬環境
    
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Windows 使用 `venv\Scripts\activate`
    
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
    
    REPO_URL、TRANSLATE_API 為資料彙整程式 (`update_data.py`) 使用，如果沒有要用到資料彙整的功能可以不填。
    
5. 匯入 QA 資料
    
    參考 `combined_context_en.csv.example` 格式編輯 QA 資料，
    
    並另存為 `combined_context_en.csv`
    
    ```bash
    cp combined_context_en.csv.example combined_context_en.csv
    
    ```
    
6. 啟動 AS-FAQ-RAG API，請使用以下命令：
    
    ```bash
    uvicorn api:app --reload --host 0.0.0.0 --port 8000
    
    ```
    
    （port 8000 可自行修改為其他埠）
    
    > [!TIP]
    > 
    > 
    > 若是正式環境請移除 `--reload` 標籤，以避免 CPU 占用過高。
    > 
7. **初次啟動**需等待 `vector_database.bin` 建立。

### English

1. Navigate to the project directory:
    
    ```bash
    cd AS-FAQ-RAG
    
    ```
    
2. Create a virtual environment:
    
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    
    ```
    
3. Install the required packages:
    
    ```bash
    pip install -r requirements.txt
    
    ```
    
4. Copy the `.env.example` file, rename it to `.env`, and edit the `.env` file:
    
    ```bash
    cp .env.example .env
    vim .env
    
    ```
    
    `REPO_URL` and `TRANSLATE_API` are used by the data aggregation script (`update_data.py`). If you do not need data aggregation functionality, you can leave them empty.
    
5. Import QA data
    
    Refer to `combined_context_en.csv.example` for the QA data format,
    
    then save your edited file as `combined_context_en.csv`:
    
    ```bash
    cp combined_context_en.csv.example combined_context_en.csv
    
    ```
    
6. Start the AS-FAQ-RAG API using the following command:
    
    ```bash
    uvicorn api:app --reload --host 0.0.0.0 --port 8000
    
    ```
    
    (You can modify port 8000 to another port if needed.)
    
    > [!TIP]
    > 
    > 
    > For a production environment, remove the `--reload` flag to prevent high CPU usage.
    > 
7. **On first startup**, wait for `vector_database.bin` to be created.

---

### Docker compose 安裝 | Docker Compose Installation

### 繁體中文

1. 將 `.env.example` 檔案複製並重新命名為 `.env`，並編輯 `.env`：
    
    ```bash
    cp .env.example .env
    vim .env
    
    ```
    
    REPO_URL、TRANSLATE_API 為資料彙整程式 (`update_data.py`) 使用，如果沒有要用到資料彙整的功能可以不填。
    
2. 匯入 QA 資料
    
    參考 `combined_context_en.csv.example` 格式編輯 QA 資料，
    
    並另存為 `combined_context_en.csv`
    
    ```bash
    cp combined_context_en.csv.example combined_context_en.csv
    
    ```
    
3. 啟動
    
    ```bash
    sudo docker compose up -d
    
    ```
    
4. 初次啟動需等待 `vector_database.bin` 建立。

### English

1. Copy `.env.example` to `.env` and edit the `.env` file:
    
    ```bash
    cp .env.example .env
    vim .env
    
    ```
    
    `REPO_URL` and `TRANSLATE_API` are used by the data aggregation script (`update_data.py`). If you do not need data aggregation functionality, you can leave them empty.
    
2. Import QA data
    
    Refer to `combined_context_en.csv.example` for the QA data format,
    
    then save your edited file as `combined_context_en.csv`:
    
    ```bash
    cp combined_context_en.csv.example combined_context_en.csv
    
    ```
    
3. Start the service:
    
    ```bash
    sudo docker compose up -d
    
    ```
    
4. On first startup, wait for `vector_database.bin` to be created.

---

### Docker compose 同時安裝 Web 及 API

### Docker Compose to Install Both Web and API

### 繁體中文

目錄架構：

```
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
    cp .env.example .env
    vim .env
    
    ```
    
    REPO_URL、TRANSLATE_API 為資料彙整程式 (`update_data.py`) 使用，如果沒有要用到資料彙整的功能可以不填。
    
3. 匯入 QA 資料
    
    參考 `combined_context_en.csv.example` 格式編輯 QA 資料，
    
    並另存為 `combined_context_en.csv`
    
    ```bash
    cp combined_context_en.csv.example combined_context_en.csv
    
    ```
    
4. 設定 `AS-FAQ-Web-ChatBot` 的方式請參考另一個專案。
5. 兩個專案都設定好後，回到第一層啟動容器：
    
    ```bash
    cd ..
    sudo docker compose up -d
    
    ```
    

### English

Directory structure:

```
YOUR-DIR/
├── docker-compose.yml
├── AS-FAQ-RAG/
│   ├── Dockerfile
│   ├── .env
│   └── ... (other files)
└── AS-FAQ-Web-ChatBot/
    ├── Dockerfile
    ├── .env
    └── ... (other files)

```

1. Create a `docker-compose.yml` file in the top-level directory:
    
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
    
2. Go to `AS-FAQ-RAG/`, copy `.env.example` to `.env`, and edit the file:
    
    ```bash
    cd AS-FAQ-RAG
    cp .env.example .env
    vim .env
    
    ```
    
    `REPO_URL` and `TRANSLATE_API` are used by the data aggregation script (`update_data.py`). If you do not need data aggregation functionality, you can leave them empty.
    
3. Import QA data
    
    Refer to `combined_context_en.csv.example` for the QA data format,
    
    then save your edited file as `combined_context_en.csv`:
    
    ```bash
    cp combined_context_en.csv.example combined_context_en.csv
    
    ```
    
4. For instructions on setting up `AS-FAQ-Web-ChatBot`, please refer to its own repository.
5. Once both projects are configured, go back to the top-level directory and start the containers:
    
    ```bash
    cd ..
    sudo docker compose up -d
    
    ```
    

---

## 匯入 QA 資料 | Importing QA Data

### 繁體中文

參考 `combined_context_en.csv.example` 格式編輯 QA 資料，

必須包含：

- `title`: 標題
- `context`: 中文內容
- `url`: 來源 URL
- `en_title`: 英文標題
- `en_context`: 英文內容

### 資料彙整程式

單獨執行 `update_data.py` 可以將個別 CSV 翻譯並合併為 `combined_context_en.csv`：

```bash
cd utils
python update_data.py

```

個別 CSV 格式參考：[AS-FAQ-Bot](https://github.com/AS-AIGC/AS-FAQ-Bot/tree/main/data/source)

> [!WARNING]
> 
> 
> `combined_context_en.csv.example` 的英文翻譯為機器翻譯，不保證正確性。
> 

### English

Refer to `combined_context_en.csv.example` for the QA data format. It must contain:

- `title`: Title
- `context`: Content in Chinese
- `url`: Source URL
- `en_title`: Title in English
- `en_context`: Content in English

### Data Aggregation Script

You can run `update_data.py` separately to translate and merge individual CSV files into `combined_context_en.csv`:

```bash
cd utils
python update_data.py

```

For individual CSV format, please refer to [AS-FAQ-Bot](https://github.com/AS-AIGC/AS-FAQ-Bot/tree/main/data/source).

> [!WARNING]
> 
> 
> The English translations in `combined_context_en.csv.example` are machine-translated and are not guaranteed to be accurate.
> 

---

## 更新資料庫 | Updating the Database

### 繁體中文

1. 關閉程式或容器
2. 刪除 `vector_database.bin`
3. 更新 `combined_context_en.csv`
4. 再次啟動 API 程式

### English

1. Stop the program or container
2. Delete `vector_database.bin`
3. Update `combined_context_en.csv`
4. Restart the API program

---

## RAG 設定 | RAG Configuration

### 繁體中文

可於 `utils/respond.py` 設定 RAG 參數，包含搜尋文件數及提示詞。

### English

You can configure RAG parameters in `utils/respond.py`, including the number of documents to search and prompt settings.

---

## 使用 | Usage

### 繁體中文

可以透過 Postman 或 curl 等開發工具連線到 API：

```bash
curl --location 'http://127.0.0.1:8000/ask' \
--data '{
   "question": "請問如何申請VPN?"
}'

```

### English

You can use Postman, curl, or similar tools to connect to the API:

```bash
curl --location 'http://127.0.0.1:8000/ask' \
--data '{
   "question": "How do I apply for a VPN?"
}'

```

---

## 預設 Port | Default Port

- **CLI 安裝 | CLI installation**: 8000
- **Docker compose**: 4000
