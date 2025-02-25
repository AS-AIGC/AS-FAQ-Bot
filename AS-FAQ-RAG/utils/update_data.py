import os
import asyncio
import pandas as pd
import requests
import logging
from openai import OpenAI
from groq import Groq
from googletrans import Translator

# 設定資料來源目錄與輸出檔案名稱
DATA_DIR = './FAQ-data'
OUTPUT_FILE = './combined_context_en.csv'

# 設定 logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 下載github repo
def download_github_repo():
    # 從 github 下載原始資料
    repo_url = os.getenv("REPO_URL")
    if not os.path.exists(DATA_DIR):
        logging.info(f"資料夾 {DATA_DIR} 不存在，正在建立")
        os.makedirs(DATA_DIR)

    # 如果資料夾為空，則 clone repo
    if not os.listdir(DATA_DIR):
        os.system(f"git clone {repo_url} {DATA_DIR}")
    else:
        # 檢查git status 如果有變更，則嘗試更新 repo
        logging.info(f"資料夾 {DATA_DIR} 已存在，檢查是否有更新...")
        os.system(f"cd {DATA_DIR} && git fetch")
        git_status = os.popen(f"git status").read()
        if "Your branch is up to date" not in git_status:
            logging.info(f"資料夾 {DATA_DIR} 已存在且有更新，嘗試更新 repo。")
            os.system(f"git reset --hard origin/main")
        else:
            logging.info(f"資料夾 {DATA_DIR} 已存在且無更新。")

# LLM 翻譯
def llm_translate_text(text) -> str:
    
    translate_api = os.getenv("TRANSLATE_API", "OLLAMA")  # Default to ollama if not specified

    prompt = f"""
            Task: Translate the following Chinese text to English.
            Maintain the original meaning and context while ensuring natural English expression.
            Only reply with the translated English text.
            
            Chinese text: {text}
            
            Translated English text:
        """
    
    try:
        if translate_api == "OLLAMA":
            # 使用 OLLAMA API
            ollama_base_url = os.getenv("OLLAMA_BASE_URL")
            response = requests.post(
                f"{ollama_base_url}/api/generate",
                json={
                    "model": os.getenv("OLLAMA_MODEL"),
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_ctx": 8192
                    }
                }
            )
        elif translate_api == "WEBUI" or translate_api == "OPENAI":
            # 使用 WebUI 或 OpenAI API
            openai_base_url = os.getenv("OPENAI_BASE_URL")
            client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=openai_base_url
            )
            completion = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL"),
                messages=[
                    {"role": "system", "content": prompt}
                ],
            )
            response = completion.choices[0].message.content
        elif translate_api == "GROQ":
            # 使用 GROQ API
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            completion = client.chat.completions.create(
                model=os.getenv("GROQ_MODEL"),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            response = completion.choices[0].message.content
        else:
            logging.error("無效的翻譯選擇")
            return ""
        
        # DEBUG
        if translate_api == "OLLAMA":
            response.raise_for_status()
            logging.info("---------------------\n翻譯結果: %s\n---------------------\n", response.json()["response"])
        else:
            logging.info("---------------------\n翻譯結果: %s\n---------------------\n", response)

        if translate_api == "OLLAMA":
            response.raise_for_status()
            return response.json()["response"]
        else:
            return response
        
    except requests.RequestException as e:
        logging.error("翻譯錯誤:", e)
        return ""

# check text length
def check_text_length(text, max_char=15000) -> int:
    if not isinstance(text, str):
        return 0
    text_length = len(text)
    if text_length > max_char:
        return -1
    return text_length

# Google 翻譯
async def google_translate_text(text, src='zh-tw',dest='en'):
    """以google翻譯將text翻譯為目標語言

    :param text: 要翻譯的字串，接受UTF-8編碼。
    :param dest: 要翻譯的目標語言，參閱googletrans.LANGCODES語言列表。
    """
    # check text length
    max_char = 10000 # https://github.com/ssut/py-googletrans 限制為 15000 字，這裡設定為 10000 字
    if check_text_length(text, max_char) <= 0:
        logging.warning("字串長度超過 %s 字或不是字串: %s", max_char, text)
        return f"<Error: Text length exceeds {max_char} characters or is not a string.>"

    async with Translator() as translator:
        result = await translator.translate(text, dest=dest, src=src)
        logging.info("---------------------\n翻譯結果: %s\n---------------------\n", result.text)
        return result.text

# 處理單一 CSV 檔案
def process_csv_file(file_path):
    df = pd.read_csv(file_path)
    if os.getenv("TRANSLATE_API") == "GOOGLE":
        # 假設原有欄位包含: contact, context, category, url, title
        # 新增翻譯結果欄位
        df['en_title'] = df['title'].apply(lambda x: asyncio.run(google_translate_text(x)))
        df['en_context'] = df['context'].apply(lambda x: asyncio.run(google_translate_text(x)))
    else:
        df['en_title'] = df['title'].apply(lambda x: llm_translate_text(x))
        df['en_context'] = df['context'].apply(lambda x: llm_translate_text(x))
    return df

# 合併所有 CSV 檔案並輸出結果
def combine_csv_files():
    SOURCE_DIR = DATA_DIR + '/data/source'
    combined_df = pd.DataFrame()
    for file_name in os.listdir(SOURCE_DIR):
        if file_name.endswith('.csv'):
            file_path = os.path.join(SOURCE_DIR, file_name)
            logging.info("處理檔案: %s", file_path)
            df = process_csv_file(file_path)
            combined_df = pd.concat([combined_df, df], ignore_index=True)
    # 調整欄位順序
    columns_order = ['contact', 'context', 'category', 'url', 'title', 'en_title', 'en_context']
    combined_df = combined_df[columns_order]
    combined_df.to_csv(OUTPUT_FILE, index=False)
    logging.info("合併後的 CSV 已輸出: %s", OUTPUT_FILE)

if __name__ == "__main__":
    # 下載資料
    download_github_repo()
    # 合併 CSV 檔案
    combine_csv_files()
