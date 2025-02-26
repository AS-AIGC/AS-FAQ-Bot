# AS-FAQ-Line-Chatbot

## 介紹 / Introduction

此專案透過 **Google Gemini** 提供的 large context window 進行推論，採用 **In-Context Learning** 的方法，並 **不使用 RAG** 技術。程式負責監聽 LINE Chatbot 傳入的訊息，並透過部署在雲端（例如 Google Cloud Functions）的 Webhook 回覆給使用者。

This project uses **Google Gemini** with a large context window, employing **In-Context Learning** and **not using RAG**. The code listens to messages from a LINE Chatbot and responds via a webhook installed on a cloud platform (such as Google Cloud Functions).

---

## 專案特色 / Key Features

1. **Loading 動畫**：在使用者傳送文字訊息後，系統會顯示「Loading」的動畫，讓使用者知道正在處理中。
2. **錯誤處理**：若發生錯誤（例如環境變數遺失或網路錯誤），系統會回覆預設的道歉訊息，提示使用者目前無法提供服務。
3. **非文字訊息處理**：若接收到圖片、貼圖或其他非文字訊息，機器人會回覆「僅支援文字訊息」的提示。

1. **Loading Animation**: After receiving a text message, the bot displays a “Loading” animation to inform the user that the system is processing their request.
2. **Error Handling**: If an error occurs (such as missing environment variables or a network issue), the bot sends a default apology message to let the user know the service is temporarily unavailable.
3. **Non-Text Input Handling**: If the bot receives images, stickers, or other non-text content, it replies with a message indicating that only text messages are supported.

---

## 環境變數 / Environment Variables

在部署此專案前，請先正確設定以下環境變數：

- `ChannelAccessToken`：LINE Messaging API 的存取金鑰
- `ChannelSecret`：LINE Messaging API 的密鑰
- `GOOGLE_GEMINI_API_KEY`：使用 Google Gemini 所需的 API 金鑰
- `Sorry_Message`：當系統發生錯誤時要回覆給使用者的預設訊息
- `System_Instruction`：傳遞給 AI 模型的系統指令（可指定角色或語氣）
- `Pre_Prompt`：在使用者輸入前先注入的提示（可引導對話內容）

Before deploying this project, configure the following environment variables:

- `ChannelAccessToken`: The access token for the LINE Messaging API
- `ChannelSecret`: The secret key for the LINE Messaging API
- `GOOGLE_GEMINI_API_KEY`: API key required for using Google Gemini
- `Sorry_Message`: Default error message to be sent to the user when the system encounters an error
- `System_Instruction`: System-level instructions passed to the AI model (e.g., specifying a role or tone)
- `Pre_Prompt`: A prompt text injected before the user's input (useful for guiding the conversation)

---

## 部署與使用流程 / Deployment and Usage

1. **下載或建立專案**下載專案，或直接在雲端平台（如 GCP）上建立。
2. **安裝依賴套件**使用 `pip install -r requirements.txt` 安裝所需套件。
3. **部署到雲端（以 Google Cloud Functions 為例）**
    - 建立新的 Google Cloud Function，選擇相容的 Python 執行環境（如 Python 3.9）。
    - 上傳專案程式碼或在雲端編輯。
    - 在「環境變數」欄位中，填寫前述所有環境變數。
    - 將函式的入口點 (Entry Point) 設為 `linebot`。
    - 部署並取得函式自動產生的 HTTPS URL。
4. **設定 LINE Chatbot Webhook**
    - 登入 LINE Developers 後台，進入您的 Channel 的 **Messaging API** 設定。
    - 將前一步取得的 HTTPS URL 填入 Webhook URL 欄位。
    - 驗證並啟用 Webhook。

1. **Obtain or Create the Project**Download the project or create it directly in a cloud platform (e.g., GCP).
2. **Install Dependencies**Run `pip install -r requirements.txt` to install all required packages.
3. **Deploy to Cloud Platform (e.g., Google Cloud Functions)**
    - Create a new Cloud Function in GCP with a compatible Python runtime (e.g., Python 3.9).
    - Upload the code or edit it in the cloud.
    - In the “Environment Variables” section, fill in all the variables mentioned above.
    - Set the function entry point to `linebot`.
    - Deploy and obtain the automatically generated HTTPS URL.
4. **Configure the LINE Chatbot Webhook**
    - Log into the LINE Developers console, then go to your Channel’s **Messaging API** settings.
    - Paste the HTTPS URL from the previous step into the Webhook URL field.
    - Verify and enable the Webhook.
4. **Configure the LINE Chatbot Webhook**
    - Log into the LINE Developers console, then go to your Channel’s **Messaging API** settings.
    - Paste the HTTPS URL from the previous step into the Webhook URL field.
    - Verify and enable the Webhook.
