# AS-FAQ-Bot

本專案為一個基於 Generative AI 的聊天機器人程式，基於預先提供的中央研究院行政服務與規定資料庫，回答使用者線上提出的各式提問。

This project demonstrates how to create a Line bot that integrates with Google's Generative AI to provide intelligent responses to user queries. The bot extracts data from various sources, processes user messages, and uses AI to generate relevant responses. 

## Table of Contents

- [Features](notion://www.notion.so/cclljj/LJ-s-To-do-items-5dadcd69a98c42869adfe0b032601214?p=4c1f84d153dd455eb416cf87c834dac8&pm=s#features)
- [Prerequisites](notion://www.notion.so/cclljj/LJ-s-To-do-items-5dadcd69a98c42869adfe0b032601214?p=4c1f84d153dd455eb416cf87c834dac8&pm=s#prerequisites)
- [Installation](notion://www.notion.so/cclljj/LJ-s-To-do-items-5dadcd69a98c42869adfe0b032601214?p=4c1f84d153dd455eb416cf87c834dac8&pm=s#installation)
- [Configuration](notion://www.notion.so/cclljj/LJ-s-To-do-items-5dadcd69a98c42869adfe0b032601214?p=4c1f84d153dd455eb416cf87c834dac8&pm=s#configuration)
- [Usage](notion://www.notion.so/cclljj/LJ-s-To-do-items-5dadcd69a98c42869adfe0b032601214?p=4c1f84d153dd455eb416cf87c834dac8&pm=s#usage)
- [Contributing](notion://www.notion.so/cclljj/LJ-s-To-do-items-5dadcd69a98c42869adfe0b032601214?p=4c1f84d153dd455eb416cf87c834dac8&pm=s#contributing)
- [License](notion://www.notion.so/cclljj/LJ-s-To-do-items-5dadcd69a98c42869adfe0b032601214?p=4c1f84d153dd455eb416cf87c834dac8&pm=s#license)
- [Acknowledgements](notion://www.notion.so/cclljj/LJ-s-To-do-items-5dadcd69a98c42869adfe0b032601214?p=4c1f84d153dd455eb416cf87c834dac8&pm=s#acknowledgements)

## Features

- Handles messages from users on Line platform.
- Integrates with Google Generative AI for intelligent responses.
- Extracts data from URLs and PDFs.
- Logs input messages and responses for debugging.

## Prerequisites

- Python 3.7 or higher
- Line Developer Account
- Google Cloud Account with Generative AI API enabled

## Installation

1. **Clone the repository:**
    
    ```bash
    git clone https://github.com/AS-AIGC/AS-FAQ-Bot.git
    cd AS-FAQ-Bot
    
    ```
    
2. **Create and activate a virtual environment:**
    
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    
    ```
    
3. **Install the dependencies:**
    
    ```bash
    pip install -r requirements.txt
    
    ```
    

## Configuration

1. **Line Bot Configuration:**
    - Go to the Line Developers Console and create a new channel.
    - Note down your `Channel Secret` and `Channel Access Token`.
2. **Google Generative AI Configuration:**
    - Set up a project in the Google Cloud Console.
    - Enable the Generative AI API.
    - Note down your API key.
3. **Environment Variables:**
    - Create a file named `.env` in the root directory of the project.
    - Add the following environment variables:
        
        ```
        LINE_TOKEN=your_line_channel_access_token
        LINE_SECRET=your_line_channel_secret
        GOOGLE_KEY=your_google_api_key
        GEMINI_PROMPT=your_system_instruction
        DATABASE=your_database_url
        GENERATION_CONFIG=your_generation_config
        SAFETY_SETTINGS=your_safety_settings
        
        ```
        

## Usage

1. **Run the application:**
    
    ```bash
    python app.py
    ```
    
2. **Set up Webhook:**
    - Go to the Line Developers Console and set your webhook URL to point to your server where the bot is running.
3. **Interacting with the bot:**
    - Open Line and send a message to your bot. The bot will reply using the integrated Google Generative AI.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](notion://www.notion.so/cclljj/CONTRIBUTING.md) before submitting a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Line Bot SDK for Python](https://github.com/line/line-bot-sdk-python)
- Google Generative AI
