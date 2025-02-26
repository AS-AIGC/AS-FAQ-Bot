from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage, ShowLoadingAnimationRequest
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from pathlib import Path
import hashlib
import requests
import time, os, json
import google.generativeai as genai

# Function to extract pages from PDF files (currently, this function lacks implementation details for reading PDF content)
def extract_pdf_pages(pathname: str) -> list[str]:
    parts = [f"--- START OF PDF ${pathname} ---"]
    # TODO: Implement logic to read the PDF and extract pages into a list
    pages = []
    for index, page in enumerate(pages):
        parts.append(f"--- PAGE {index} ---")
        parts.append(page)
    return parts

# Function to extract data from a URL
def extract_from_URL(pathname: str) -> list[str]:
    response = requests.get(pathname)
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to retrieve {pathname}. Status code: {response.status_code}"

# Retrieve necessary environment variables
access_token = os.getenv('ChannelAccessToken')
secret = os.getenv('ChannelSecret')
genai.configure(api_key=os.getenv('GOOGLE_GEMINI_API_KEY'))

# Set up LINE Messaging API configuration
configuration = Configuration(access_token=access_token)
handler = WebhookHandler(secret)

# Default message for unsupported questions
SORRY_MESSAGE = os.getenv('Sorry_Message')

# Instructions for the generative AI model
system_instruction = os.getenv('System_Instruction')
pre_prompt = os.getenv('Pre_Prompt')


# List of URLs for data sources
DATABASE = [
      "https://raw.githubusercontent.com/AS-AIGC/AS-FAQ-Bot/main/data/AS-ALL.txt",
    ]

# Generation configuration for the AI model
generation_config = {
      "temperature": 0.8,
      "top_p": 0.95,
      "top_k": 0,
      "max_output_tokens": 8192,
    }

# Safety settings for handling harmful content
safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
    ]

# Main function to handle incoming requests from the LINE bot
def linebot(request):
    start_time = time.time()  # Track the start time for performance monitoring
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    user_id = json_data['events'][0]['source']['userId']
    msg_type = json_data['events'][0]['message']['type']
    tk = json_data['events'][0]['replyToken']

    try:
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)

        if msg_type == 'text':


            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                # Show a loading animation to the user
                line_bot_api.show_loading_animation(ShowLoadingAnimationRequest(chatId=user_id, loadingSeconds=60))
                


                # Initialize the AI model
                model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", generation_config=generation_config, system_instruction=system_instruction, safety_settings=safety_settings)
            
                # Prepare history from the DATABASE URLs
                hist = [{'role': 'user', 'parts': extract_from_URL(url)} for url in DATABASE]

                msg = json_data['events'][0]['message']['text']
                print(f"Q: {msg}\ntoken: {tk}")
                
                msg = pre_prompt + "\n\n\n" + msg

                # Start the conversation with the AI model
                convo = model.start_chat(history=hist)
                convo.send_message(msg)
                
                # Reply to the user with the AI-generated message
                line_bot_api.reply_message(ReplyMessageRequest(
                    reply_token=tk,
                    messages=[
                        TextMessage(text=convo.last.text),
                    ]))
                
                # Log the response for debugging
                response = convo.last.text.replace('\n', ' ').replace('\r', '')
                print(f"A: {response} \n Execution Time: %s" % (time.time() - start_time))
        else:
            # Handle non-text messages by informing the user
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.show_loading_animation(ShowLoadingAnimationRequest(chatId=user_id, loadingSeconds=60))
                line_bot_api.reply_message(ReplyMessageRequest(
                    reply_token=tk,
                    messages=[
                        TextMessage(text='感謝您的訊息！我們只支援文字喔！\nThank you for your message! We only support text.'),
                    ]))
                
                response = '感謝您的訊息！我們只支援文字喔！'
                print(f"A: {response} \n Execution Time: %s" % (time.time() - start_time))
    except Exception as e:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.show_loading_animation(ShowLoadingAnimationRequest(chatId=user_id, loadingSeconds=60))
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token=tk,
                messages=[
                    TextMessage(text=SORRY_MESSAGE),
                ]))
        print(SORRY_MESSAGE, "Error: ", e)

    return 'OK'
