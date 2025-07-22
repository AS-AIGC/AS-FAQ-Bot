# AS-FAQ-RAG

---

## 介紹 | Introduction

### 繁體中文

本項目是 **AS-FAQ-RAG** 的後端 API。  
AS-FAQ-RAG是一個基於 RAG（Retrieval-Augmented Generation）技術的 FAQ 系統。它結合了前端網頁和後端 API，提供了一個解決方案來處理常見問題的自動回答。前端網頁 **AS-FAQ-Web-ChatBot** 提供了使用者友善的界面，而後端 API **AS-FAQ-RAG** 負責處理數據檢索和生成回答。

### English

This project is the back-end API for AS-FAQ-RAG.  
AS-FAQ-RAG is an FAQ system based on RAG (Retrieval-Augmented Generation) technology. It combines a front-end web interface and a back-end API to provide a solution for automatically answering frequently asked questions. The front-end web page, AS-FAQ-Web-ChatBot, offers a user-friendly interface, while the back-end API, AS-FAQ-RAG, handles data retrieval and generates responses.

---

## 安裝 | Installation

**繁體中文**  

1. 下載程式碼或複製專案  
2. 可以選擇使用 CLI 或是 Docker compose 的方式執行  

**English**  

1. Download or clone the repository  
2. You can choose to run it via CLI or Docker Compose  

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
    
    `REPO_URL` 為資料彙整程式 (`update_data.py`) 使用，如果沒有要用到資料彙整的功能可以不填。
    
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
> 若是正式環境請移除 `--reload` 標籤，以避免 CPU 占用過高。

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
    
    `REPO_URL` is used by the data aggregation script (`update_data.py`). If you do not need data aggregation functionality, you can leave them empty.
    
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
> For a production environment, remove the `--reload` flag to prevent high CPU usage.

7. On first startup, wait for `vector_database.bin` to be created.

---

### Docker compose 安裝 | Docker Compose Installation

### 繁體中文

1. 將 `.env.example` 檔案複製並重新命名為 `.env`，並編輯 `.env`：
    
    ```bash
    cp .env.example .env
    vim .env
    
    ```
    
    REPO_URL 為資料彙整程式 (`update_data.py`) 使用，如果沒有要用到資料彙整的功能可以不填。
    
2. 匯入 QA 資料
    
    參考 `combined_context_en.csv.example` 格式編輯 QA 資料，
    
    並另存為 `combined_context_en.csv`
    
    ```bash
    cp combined_context_en.csv.example combined_context_en.csv
    
    ```

3. 確保 start.sh 腳本有執行權限
    
    ```bash
    chmod +x start.sh
    ```
    
4. 啟動
    
    ```bash
    sudo docker compose up -d
    
    ```
    
5. 初次啟動需等待 `vector_database.bin` 建立。

### English

1. Copy `.env.example` to `.env` and edit the `.env` file:
    
    ```bash
    cp .env.example .env
    vim .env
    
    ```
    
    `REPO_URL` is used by the data aggregation script (`update_data.py`). If you do not need data aggregation functionality, you can leave them empty.
    
2. Import QA data
    
    Refer to `combined_context_en.csv.example` for the QA data format,

    then save your edited file as `combined_context_en.csv`:
    
    ```bash
    cp combined_context_en.csv.example combined_context_en.csv
    
    ```
    
3. Ensure the start.sh script has execution permissions
    
    ```bash
    chmod +x start.sh
    ```
    
4. Start the service:
    
    ```bash
    sudo docker compose up -d
    
    ```
    
5. On first startup, wait for `vector_database.bin` to be created.

---

### Docker compose 同時安裝 Web 及 API | Docker Compose to Install Both Web and API

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
            environment:
            - TZ=Asia/Taipei
            env_file:
            - ./AS-FAQ-RAG/.env
            volumes:
            - ./AS-FAQ-RAG:/app
            - ./hf_cache:/app/hf_cache
            working_dir: /app
            restart: always

        web:
            build: ./AS-FAQ-Web-ChatBot
            ports:
            - "3080:3000"
            environment:
            - TZ=Asia/Taipei
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
    
    REPO_URL 為資料彙整程式 (`update_data.py`) 使用，如果沒有要用到資料彙整的功能可以不填。
    
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
            environment:
            - TZ=Asia/Taipei
            env_file:
            - ./AS-FAQ-RAG/.env
            volumes:
            - ./AS-FAQ-RAG:/app
            - ./hf_cache:/app/hf_cache
            working_dir: /app
            restart: always

        web:
            build: ./AS-FAQ-Web-ChatBot
            ports:
            - "3080:3000"
            environment:
            - TZ=Asia/Taipei
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
    
    `REPO_URL` is used by the data aggregation script (`update_data.py`). If you do not need data aggregation functionality, you can leave them empty.
    
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

### 更新 Docker compose | Updating Docker Compose
### 繁體中文
1. 停止容器
    
    ```
    sudo docker compose down
    ```
    
2. 更新程式碼 (git)
    
    ```
    git pull
    ```
    
3. 建立新映像
    
    ```
    sudo docker compose build --no-cache
    ```
    
4. 啟動容器
    
    ```
    sudo docker compose up -d
    ```

### English
1. Stop the containers:
    
    ```
    sudo docker compose down
    ```
2. Update the code (git):
    
    ```
    git pull
    ```
3. Build new images:
    
    ```
    sudo docker compose build --no-cache
    ```
4. Start the containers:
    
    ```
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

## 啟用或停用自動更新 | Enable or Disable Auto Update

**繁體中文**  
本專案支援兩種方式控制自動更新功能：

1. **啟動參數**  
   - 啟用自動更新：  
     ```bash
     ./start.sh --auto-update
     ```

2. **環境變數**  
   - 在啟動前設定 `ENABLE_AUTO_UPDATE_ENV=1` 可啟用自動更新：  
     ```bash
     ENABLE_AUTO_UPDATE_ENV=1 ./start.sh
     ```
   - 若未設定參數且未設定環境變數，則預設不啟用自動更新。

> 註：若同時設定參數與環境變數，**以參數為主**。

### English
This project supports two ways to control the auto update feature:

1. **Command-line Argument**  
   - Enable auto update:  
     ```bash
     ./start.sh --auto-update
     ```

2. **Environment Variable**  
   - Set `ENABLE_AUTO_UPDATE_ENV=1` before starting to enable auto update:  
     ```bash
     ENABLE_AUTO_UPDATE_ENV=1 ./start.sh
     ```
   - If neither argument nor environment variable is set, auto update is disabled by default.

> Note: If both argument and environment variable are set, **the argument takes precedence**.

---

## 自訂埠號 | Custom Port

**繁體中文**  
您可以使用 `--port=<埠號>` 參數來自訂 API 服務的埠號：

```bash
# 使用自訂埠號 3000
./start.sh --port=3000

# 同時啟用自動更新和自訂埠號
./start.sh --auto-update --port=3000
```

**Windows 使用者**可以使用 `start.bat`：

```batch
REM 使用自訂埠號 3000
start.bat --port=3000

REM 同時啟用自動更新和自訂埠號
start.bat --auto-update --port=3000
```

### English
You can use the `--port=<port>` parameter to customize the API service port:

```bash
# Use custom port 3000
./start.sh --port=3000

# Enable auto update and custom port
./start.sh --auto-update --port=3000
```

**Windows users** can use `start.bat`:

```batch
REM Use custom port 3000
start.bat --port=3000

REM Enable auto update and custom port
start.bat --auto-update --port=3000
```
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

### 繁體中文

可於 `utils/respond.py` 設定 RAG 參數，包含搜尋文件數。

若要修改系統使用的提示詞，您可以編輯 `utils/prompts.yaml` 檔案。 這個檔案包含用於不同任務的提示詞，例如回答問題、翻譯文本和檢測語言。 此外，還提供了一個範例檔案 `utils/prompts.yaml.example`，其中包含簡化的提示詞，供測試使用。 您可以將此檔案複製到 `utils/prompts.yaml` 以使用範例提示詞。

請手動刪除 `utils/prompts.py` 和 `utils/prompts.py.example` 檔案。

### English

You can configure RAG parameters in `utils/respond.py`, including the number of documents to search.

To modify the prompts used by the system, you can edit the `utils/prompts.yaml` file. This file contains the prompts used for different tasks, such as answering questions, translating text, and detecting languages. An example file `utils/prompts.yaml.example` is also provided, which contains simplified prompts for testing purposes. You can copy this file to `utils/prompts.yaml` to use the example prompts.

Please manually delete `utils/prompts.py` and `utils/prompts.py.example` files.

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

---

## Acknowledgements

**繁體中文**  

本專案的原始版本為 [彭康軒](https://github.com/MKE0108) 先生於中央研究院資訊科學所擔任研究助理時完成撰寫 (2024/10)，特此致謝。

**English**  

The original version of this project was authored by Mr. [Kang-Syuan Peng](https://github.com/MKE0108) during his internship as a research assistant the Institute of Information Science, Academia Sinica (2024/10). We would like to express our gratitude.
