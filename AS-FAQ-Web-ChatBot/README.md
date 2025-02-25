# AS-FAQ-RAG

AS-FAQ-RAG是一個基於RAG（Retrieval-Augmented Generation）技術的FAQ系統。它結合了前端網頁和後端API，提供了一個解決方案來處理常見問題的自動回答。前端網頁AS-FAQ-Web-ChatBot提供了用戶友好的界面，而後端API AS-FAQ-RAG負責處理數據檢索和生成回答。


## 介紹 (AS-FAQ-Web-ChatBot)
本項目 (AS-FAQ-Web-ChatBot) 是 AS-FAQ-RAG 的前端聊天介面及呼叫後端API的部分

## 安裝
1. 下載程式碼或複製專案
2. 可以選擇使用CLI或是Docker compose的方式執行

### CLI 安裝
#### 環境
- node v20.18.0
- npm 8.15.0

1. 進入專案目錄
    ```bash
    cd AS-FAQ-Web-ChatBot
    ```

2. 安裝前端套件
    ```bash
    npm install
    ```
3. 執行 tailwindcss (即時編譯前端CSS)
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

6. 開啟瀏覽器，http://localhost:3000

### Docker compose 安裝
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
4. 開啟瀏覽器，http://localhost:3080

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
2. 進入專案目錄編輯 `.env.example` 文件，根據需要修改
    ```bash
    cp .env.example .env
    vim .env
    ```
3. 設定 `AS-FAQ-RAG` 方式請參考另一個專案

3. 使用 Docker Compose 啟動服務
    ```bash
    docker compose up -d
    ```
4. 開啟瀏覽器，http://localhost:3080

## 編輯使用條款及個資政策網頁
將使用條款(`tos.html`)及個資政策(`privacy.html`)放入`index.html`同一層目錄中，  
或修改`index.html`中對應的網址到現有的網頁。

## TODO


## Credits
原程式由昆霖撰寫 2025/01