# AS-FAQ-Web-ChatBot

---

## 介紹 / Introduction (AS-FAQ-Web-ChatBot)

**繁體中文**  

本項目 **AS-FAQ-Web-ChatBot** 是 **AS-FAQ-RAG** 的前端聊天介面，並包含呼叫後端 API 的功能。  
AS-FAQ-RAG 是一個基於 RAG（Retrieval-Augmented Generation）技術的 FAQ 系統。它結合了前端網頁和後端 API，提供了一個解決方案來自動回應常見問題。前端網頁 **AS-FAQ-Web-ChatBot** 提供了使用者友善的介面，而後端 API **AS-FAQ-RAG** 負責處理數據檢索和產生答案。

**English**  

This project (**AS-FAQ-Web-ChatBot**) is the front-end chat interface for **AS-FAQ-RAG** and includes the functionality to call the back-end API.  
AS-FAQ-RAG is an FAQ system based on RAG (Retrieval-Augmented Generation) technology. It combines a front-end web interface with a back-end API to provide automated responses to frequently asked questions. The front-end web interface, **AS-FAQ-Web-ChatBot**, offers a user-friendly interface, while the back-end API, **AS-FAQ-RAG**, handles data retrieval and answer generation.

---

## 安裝 / Installation

**繁體中文**  

以下提供兩種安裝方式：使用 CLI 或使用 Docker Compose。

**English**  

Below are two methods of installation: using the CLI or using Docker Compose.

---

### CLI 安裝 / CLI Installation

#### 環境需求 / Prerequisites

- **node** v20.18.0
- **npm** 8.15.0

**繁體中文**  

1. 進入專案目錄
    ```bash
    cd AS-FAQ-Web-ChatBot
    ```

2. 安裝前端套件
    ```bash
    npm install
    ```

3. 執行 tailwindcss (即時編譯前端 CSS)
    ```bash
    npm run watch
    ```

4. 編輯 `.env.example` 文件，根據需要修改
    ```bash
    cp .env.example .env
    vim .env
    ```

5. 啟動 node server
    ```bash
    node server.js
    ```

6. 開啟瀏覽器，並輸入網址：http://localhost:3000

**English**  

1. Enter the project directory:
    ```bash
    cd AS-FAQ-Web-ChatBot
    ```

2. Install front-end dependencies:
    ```bash
    npm install
    ```

3. Run tailwindcss for real-time CSS compilation:
    ```bash
    npm run watch
    ```

4. Copy and edit `.env.example` as needed:
    ```bash
    cp .env.example .env
    vim .env
    ```

5. Start the Node server:
    ```bash
    node server.js
    ```

6. Open your browser at: http://localhost:3000

---

### Docker compose 安裝 / Docker Compose Installation

**繁體中文**  

1. 進入專案目錄
    ```bash
    cd AS-FAQ-Web-ChatBot
    ```

2. 編輯 `.env.example` 文件，根據需要修改
    ```bash
    cp .env.example .env
    vim .env
    ```

3. 使用 Docker Compose 啟動服務
    ```bash
    docker compose up -d
    ```

4. 開啟瀏覽器，並輸入網址：http://localhost:3080

**English**  

1. Enter the project directory:
    ```bash
    cd AS-FAQ-Web-ChatBot
    ```

2. Copy and edit `.env.example` as needed:
    ```bash
    cp .env.example .env
    vim .env
    ```

3. Start the service with Docker Compose:
    ```bash
    docker compose up -d
    ```

4. Open your browser at: http://localhost:3080

---

### Docker compose 同時安裝 Web 及 API / Installing Web & API Together with Docker Compose

**繁體中文**  

假設您的目錄架構如下：

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
    yaml
    CopyEdit
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
    
2. 進入專案目錄，編輯 `.env.example` 文件，根據需要修改
    
    ```bash
    bash
    CopyEdit
    cp .env.example .env
    vim .env
    
    ```
    
3. 設定 **AS-FAQ-RAG** 的部分請參考相關專案
4. 使用 Docker Compose 啟動服務
    
    ```bash
    bash
    CopyEdit
    docker compose up -d
    
    ```
    
5. 開啟瀏覽器，並輸入網址：[http://localhost:3080](http://localhost:3080/)

**English**

Assume your directory structure is as follows:

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

1. Create a file named `docker-compose.yml` in the top-level directory:
    
    ```yaml
    yaml
    CopyEdit
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
    
2. Go into the project directory, copy and edit the `.env.example` file as needed:
    
    ```bash
    bash
    CopyEdit
    cp .env.example .env
    vim .env
    
    ```
    
3. Refer to the **AS-FAQ-RAG** project for its specific configuration.
4. Start the services using Docker Compose:
    
    ```bash
    bash
    CopyEdit
    docker compose up -d
    
    ```
    
5. Open your browser at: [http://localhost:3080](http://localhost:3080/)

---

## 編輯使用條款及個資政策網頁 / Editing Terms of Service & Privacy Policy Pages

**繁體中文**

將使用條款 (`tos.html`) 與個資政策 (`privacy.html`) 放在與 `index.html` 同一層目錄，

或在 `index.html` 中將其指向現有的網頁連結。

**English**

Place the Terms of Service (`tos.html`) and Privacy Policy (`privacy.html`) files in the same directory as `index.html`,

or modify the corresponding links in `index.html` to point to your existing pages.


---

## Acknowledgements

**繁體中文**  

本專案的原始版本為 [墜昆霖](https://github.com/jhuei0831) 先生於中央研究院資訊服務處服務時完成撰寫 (2025/01)，特此致謝。

**English**  

The original version of this project was authored by Mr. Kun-Ling Zui during his service at the Department of Information Technology Services of Academia Sinica (2025/01). We would like to express our gratitude.

