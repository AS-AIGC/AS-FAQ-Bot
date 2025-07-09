const express = require('express');
const rateLimit = require('express-rate-limit');
const path = require('path');
const axios = require('axios');
const helmet = require('helmet'); // 引入 helmet
require('dotenv').config();

const app = express();

// 根據環境決定是否使用 helmet 和 HSTS
if (process.env.NODE_ENV === 'production') {
  // 在生產環境中使用完整的 helmet 配置
  app.use(
    helmet({
      strictTransportSecurity: {
        maxAge: 31536000, // 設定 HSTS max-age 為一年 (單位為秒)
        includeSubDomains: true, // 套用到所有子網域
        preload: true // 允許預載入 HSTS 清單
      }
    })
  );
}

// 提供靜態文件 (HTML, CSS)，tailwindcss
app.use(express.static(path.join(__dirname, 'src')));
// 移除 Express 預設的 X-Powered-By 標頭
app.disable('x-powered-by');

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'src', 'index.html'));
});

// 建立一個 limiter 實例
const limiter = rateLimit({
  windowMs: process.env.RATE_LIMIT_MINUTE * 60 * 1000, // 1 分鐘的時間窗口
  max: process.env.RATE_LIMIT_MAX_REQUEST, // 每個 IP 最多允許 100 次請求
  message: '請求過多，請稍後再試。' // 超出限制時返回的訊息
});

// 解析 JSON 請求體的中介軟體
app.use(express.json());
// 只對 api 路由套用速率限制
app.use('/eip/askbot', limiter);
app.use('/askbot', limiter);

app.post(['/eip/askbot', '/askbot'], async (req, res) => { // "/eip/askbot" for webui dev, "/askbot" for local pc dev
  const { question } = req.body;

  if (!question) {
      return res.status(400).json({ error: '請提供問題' });
  }
  // 呼叫 API 取得答案
  try {
    const apiUrl = `${process.env.BACKEND_URL}/ask`;
    const response = await axios.post(apiUrl, { question });
    const answer = response.data.answer;

    res.json({ answer });
  } catch (error) {
    console.error('Error calling API:', error);
    res.status(500).json({ error: 'API 呼叫失敗' });
  }
});

// 獲取嵌入模型資訊的 endpoint
app.get(['/api/rag/embedding-info'], async (req, res) => {
  try {
    const apiUrl = `${process.env.BACKEND_URL}/api/rag/embedding-info`;
    const response = await axios.get(apiUrl);
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching embedding info:', error);
    res.status(500).json({ error: '無法獲取嵌入模型資訊' });
  }
});

// 獲取 LLM 模型資訊的 endpoint
app.get(['/api/rag/llm-info'], async (req, res) => {
  try {
    const apiUrl = `${process.env.BACKEND_URL}/api/rag/llm-info`;
    const response = await axios.get(apiUrl);
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching LLM info:', error);
    res.status(500).json({ error: '無法獲取 LLM 模型資訊' });
  }
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});