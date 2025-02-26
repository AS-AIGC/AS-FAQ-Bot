# AS-FAQ-Bot

[![Academia Sinica](https://img.shields.io/badge/Academia%20Sinica-%23006E99.svg?style=for-the-badge)](https://www.sinica.edu.tw)
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)


AS-FAQ-Bot 是一個多功能的 FAQ Chatbot 解決方案，提供兩種技術方案：基於 RAG（Retrieval-Augmented Generation）的問答系統，以及基於 in-context learning 的 Line Chatbot。這個專案包含四個主要部分：**AS-FAQ-RAG** 提供 RAG 方案的後端資料檢索與生成回答，**AS-FAQ-Web-ChatBot** 提供 RAG 方案的前端網頁使用者介面，**AS-FAQ-Line-Chatbot** 提供基於 in-context learning 的 Line Chatbot webhook，而 **data** 則包含 FAQ 的原始資料。

This project demonstrates how to create versatile FAQ chatbots using two approaches: a Retrieval-Augmented Generation (RAG) system and an in-context learning-based Line Chatbot. It integrates a powerful backend with a user-friendly web interface for the RAG solution, alongside a Line Chatbot implementation, efficiently handling frequently asked questions across different platforms.

## Features

- **中文 / Chinese**
  - 支援中文及英文，適用於更廣泛的使用者群體
  - 提供 RAG 技術與 in-context learning 兩種方案，滿足不同應用場景
  - 前後端分離架構（RAG 方案）與獨立 webhook（Line Chatbot），提升靈活性和適應性
  - 可接入多種 AI 服務，提供更多樣化的回答
  - 使用者友善的介面設計（網頁與 Line），提升使用體驗

- **English**
  - Supports both Chinese and English, catering to a wider range of users
  - Offers two solutions: RAG technology and in-context learning, addressing diverse use cases
  - Frontend-backend separation architecture (RAG) and standalone webhook (Line Chatbot), enhancing flexibility and adaptability
  - Integrates with various AI services, providing diverse responses
  - User-friendly interface design (web and Line), improving user experience

## Installation

請參考目錄中的 README.md：
- [AS-FAQ-RAG](AS-FAQ-RAG/README.md)  
- [AS-FAQ-Web-ChatBot](AS-FAQ-Web-ChatBot/README.md)  
- [AS-FAQ-Line-Chatbot](AS-FAQ-Line-Chatbot/README.md)  
- [data](data)  

Please refer to the README.md in the directory:  
- [AS-FAQ-RAG](AS-FAQ-RAG/README.md)  
- [AS-FAQ-Web-ChatBot](AS-FAQ-Web-ChatBot/README.md)  
- [AS-FAQ-Line-Chatbot](AS-FAQ-Line-Chatbot/README.md)  
- [data](data)  

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
