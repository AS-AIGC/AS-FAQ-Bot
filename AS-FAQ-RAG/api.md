# API 說明文件

本文件為現有 API 端點提供說明。

## 端點

### 1. 提出問題

- **端點:** `POST /ask`
- **說明:** 此端點接收使用者的問題，並以串流方式回傳答案及相關來源。
- **請求主體 (Request Body):**
  ```json
  {
    "question": "你的問題"
  }
  ```
- **回應 (Responses):**
  - `200 OK`: 以串流方式回傳 JSON 回應。串流將產生 JSON 物件。
    - **成功物件:**
      ```json
      {"answer": "問題的答案。", "sources": ["source1", "source2"]}
      ```
    - **錯誤物件:**
      ```json
      {"error": "發生內部錯誤！"}
      ```
  - `400 Bad Request`: 如果請求主體中未提供問題。
    ```json
    {"error": "Question not provided"}
    ```
  - `500 Internal Server Error`: 如果伺服器發生錯誤。

### 2. 獲取嵌入模型資訊

- **端點:** `GET /api/rag/embedding-info`
- **說明:** 獲取當前使用的嵌入模型名稱。
- **回應 (Responses):**
  - `200 OK`:
    ```json
    {
      "embedding_model": "model-name"
    }
    ```

### 3. 獲取大型語言模型 (LLM) 供應商資訊

- **端點:** `GET /api/rag/llm-info`
- **說明:** 獲取當前使用的大型語言模型 (LLM) 供應商名稱。
- **回應 (Responses):**
  - `200 OK`:
    ```json
    {
      "llm_provider": "provider-name"
    }
    ``` 