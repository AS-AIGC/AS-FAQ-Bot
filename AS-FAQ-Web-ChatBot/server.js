const express = require('express');
const rateLimit = require('express-rate-limit');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

const app = express();

// 提供靜態文件 (HTML, CSS)，tailwindcss
app.use(express.static(path.join(__dirname, 'src')));

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
    const apiUrl = process.env.API_URL;
    const response = await axios.post(apiUrl, { question });
    const answer = response.data.answer;

    res.json({ answer });
  } catch (error) {
    console.error('Error calling API:', error);
    res.status(500).json({ error: 'API 呼叫失敗' });
  }
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});