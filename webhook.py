import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from pathlib import Path
import hashlib
import requests
import time
import google.generativeai as genai

# Function to extract pages from PDF files
def extract_pdf_pages(pathname: str) -> list[str]:
  parts = [f"--- START OF PDF ${pathname} ---"]
  # Add logic to read the PDF and return a list of pages here.
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

# Main function to handle Line bot requests
def linebot(request):
  try:
    start_time = time.time()

    access_token = config.LINE_TOKEN
    secret = config.LINE_SECRET

    genai.configure(api_key=config.GOOGLE_KEY)
    system_instruction = config.GEMINI_PROMPT
    DATABASE = config.DATABASE
    generation_config = config.GENERATION_CONFIG
    safety_settings = config.SAFETY_SETTINGS
    
    # Parse the request body and signature
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    line_bot_api = LineBotApi(access_token)
    handler = WebhookHandler(secret)
    signature = request.headers['X-Line-Signature']
    
    # Handle the incoming messages and generate responses
    handler.handle(body, signature)
    msg = json_data['events'][0]['message']['text']
    tk = json_data['events'][0]['replyToken']
    
    # Log the input message for debugging
    print(f"Q: {msg}")

    # Configure and start the AI chat model
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro",generation_config=generation_config,system_instruction=system_instruction,safety_settings=safety_settings)
    hist = [{'role': 'user', 'parts': extract_from_URL(url)} for url in DATABASE] 

    convo = model.start_chat(history=hist)
    convo.send_message(msg)
    line_bot_api.reply_message(tk,TextSendMessage(convo.last.text))
    
    # Log the response for debugging
    response = convo.last.text.replace('\n', ' ').replace('\r', '')
    print(f"A: {response}")
    print(f"Execution Time: %s" % (time.time() - start_time))

  except Exception as e:
    # Handle exceptions and provide user feedback
    print("Error: ", e)

  return 'OK'
