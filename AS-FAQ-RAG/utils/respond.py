"""
Search and QA System
This module implements a vector search-based QA system using FAISS for similarity search,
combined with multiple LLM providers for text generation and translation.
"""

import yaml

try:
    with open("config/prompts/prompts.yaml", 'r', encoding='utf-8') as f:
        prompts = yaml.safe_load(f)
    SYSTEM_PROMPT = prompts["SYSTEM_PROMPT"]
    TRANSLATION_PROMPT = prompts["TRANSLATION_PROMPT"]
    LANGUAGE_DETECTION_PROMPT = prompts["LANGUAGE_DETECTION_PROMPT"]
    QA_PROMPT = prompts["QA_PROMPT"]
    QA_PROMPT_EN = prompts["QA_PROMPT_EN"]
except Exception as e:
    print(f"Error loading prompts from YAML: {e}")
    SYSTEM_PROMPT = "You are a helpful assistant."
    TRANSLATION_PROMPT = "Translate to English: {text}"
    LANGUAGE_DETECTION_PROMPT = "Task: Detect the language of the following text: {query} If the text is Chinese, reply '台灣繁體中文'. If the text is in any other language, reply 'english'. Only reply with the language code."
    QA_PROMPT = "對話歷史：{previous_chat} 這是和這個問題可能相關的背景知識: {context} 使用者的問題: {query}，以 {lang} 回覆"
    QA_PROMPT_EN = "Conversation History: {previous_chat} Background Knowledge: {context} USER's QUESTION: {query} , response in {lang}"

import os
from dotenv import load_dotenv
import csv
import logging
import time
from typing import List, Dict, Tuple, Optional, Literal
from enum import Enum
import json
import google.generativeai as genai
import openai
from groq import Groq
import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import asyncio
import threading

MAX_HISTORY_ROUND = 1 # 最多要傳入最近幾輪的對話歷史紀錄到 Prompt

# Global Configuration
class LLMProvider(Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    OLLAMA = "ollama"
    GROQ = "groq"
    WEBUI = "webui"

# 從字串轉換成 LLMProvider 枚舉的函數
def get_llm_provider(provider_str: str) -> LLMProvider:
    """
    根據環境變數中的字串值轉換成 LLMProvider 枚舉
    
    Args:
        provider_str: 提供者名稱字串
        
    Returns:
        LLMProvider 枚舉值
    """
    provider_map = {
        "gemini": LLMProvider.GEMINI,
        "openai": LLMProvider.OPENAI,
        "ollama": LLMProvider.OLLAMA,
        "groq": LLMProvider.GROQ,
        "webui": LLMProvider.WEBUI,
    }
    
    return provider_map.get(provider_str.lower(), LLMProvider.OLLAMA)

# Global Variables
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
CONFIG = {
    # File Paths
    "CSV_PATH": "combined_context_en.csv",
    "VECTOR_DB_PATH": "vector_database.bin",
    
    # Default Provider - 從環境變數讀取，預設為 Ollama
    "DEFAULT_LLM_PROVIDER": get_llm_provider(os.getenv("DEFAULT_LLM_PROVIDER", "ollama")),
    
    # API Keys and Endpoints
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", ""),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
    "WEBUI_API_KEY": os.getenv("WEBUI_API_KEY", ""),
    "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    "WEBUI_BASE_URL": os.getenv("WEBUI_BASE_URL", "http://localhost:8000"),
    
    # Model Configuration
    "GEMINI_MODEL": os.getenv("GEMINI_MODEL", "gemini-2.0-flash-001"),
    "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
    "GROQ_MODEL": os.getenv("GROQ_MODEL","mixtral-8x7b-32768"),
    "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL", "llama3.2-vision:latest"),
    "WEBUI_MODEL": os.getenv("WEBUI_MODEL", "llama3.2-vision:latest"),
    
    # Vector Search Configuration
    "VECTOR_MODEL": os.getenv("VECTOR_MODEL", "multi-qa-mpnet-base-dot-v1"),
    "TOP_K_RESULTS": 10,
    
    # Debug Mode
    "DEBUG_MODE": os.getenv("DEBUG_MODE", "false").lower() == "true",
    
    
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 全域 embedding model 及 lock
_GLOBAL_ST_MODEL = None
_GLOBAL_ST_MODEL_LOCK = threading.Lock()

class LLMService:
    """Service class for handling different LLM providers"""
    
    def __init__(self, provider: LLMProvider):
        """
        Initialize LLM service with specified provider
        
        Args:
            provider: The LLM provider to use
        """
        self.provider = provider
        self._setup_provider()
    
    def _setup_provider(self):
        """Setup the selected LLM provider"""
        if self.provider == LLMProvider.GEMINI:
            if not CONFIG["GOOGLE_API_KEY"]:
                raise ValueError("GOOGLE_API_KEY not set")
            genai.configure(api_key=CONFIG["GOOGLE_API_KEY"])
            
        elif self.provider == LLMProvider.OPENAI:
            if not CONFIG["OPENAI_API_KEY"]:
                raise ValueError("OPENAI_API_KEY not set")
            self.client = openai.OpenAI(api_key=CONFIG["OPENAI_API_KEY"])
            
        elif self.provider == LLMProvider.GROQ:
            if not CONFIG["GROQ_API_KEY"]:
                raise ValueError("GROQ_API_KEY not set")
            self.client = Groq(api_key=CONFIG["GROQ_API_KEY"])
    
    async def generate_response(self, prompt: str) -> str:
        """
        Generate response using the selected LLM provider
        
        Args:
            prompt: The input prompt
            
        Returns:
            Generated response text
        """
        try:
            if self.provider == LLMProvider.GEMINI:
                model = genai.GenerativeModel(
                    model_name=CONFIG["GEMINI_MODEL"],
                    system_instruction= SYSTEM_PROMPT
                )
                response = model.generate_content(prompt)
                return response.text
                
            elif self.provider == LLMProvider.OPENAI:
                # 未加入system prompt
                response = self.client.chat.completions.create(
                    model=CONFIG["OPENAI_MODEL"],
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
                
            elif self.provider == LLMProvider.OLLAMA:
                # 未加入system prompt
                response = await asyncio.to_thread(
                    requests.post,
                    f"{CONFIG['OLLAMA_BASE_URL']}/api/generate",
                    json={
                        "model": CONFIG["OLLAMA_MODEL"],
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "num_ctx": 30000
                        }
                    }
                )
                return response.json()["response"]
                
            elif self.provider == LLMProvider.WEBUI:
                openai_payload = {
                    "model": CONFIG["WEBUI_MODEL"],
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {
                        "num_ctx": 30000
                    }
                }
                response = await asyncio.to_thread(
                    requests.post,
                    f"{CONFIG['WEBUI_BASE_URL']}/api/chat/completions",
                    headers={"Authorization": f"Bearer {CONFIG['WEBUI_API_KEY']}"},
                    json=openai_payload
                )
                print(response.json())
                return response.json()["choices"][0]["message"]["content"]
                
            elif self.provider == LLMProvider.GROQ:
                # 未加入system prompt
                response = self.client.chat.completions.create(
                    model=CONFIG["GROQ_MODEL"],
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"Error generating response with {self.provider}: {str(e)}")
            # Include "429 Resource has been exhausted (e.g. check quota)" return error message
            if "429" in str(e):
                return "🔄 系統目前請求過多，暫時無法回應。請稍後重試，感謝您的耐心等待！"
            raise

class SearchQASystem:
    """Main class for the Search and QA System"""
    
    def __init__(
            self,
            csv_path: str = CONFIG["CSV_PATH"],
            vector_db_path: str = CONFIG["VECTOR_DB_PATH"],
            llm_provider: LLMProvider = CONFIG["DEFAULT_LLM_PROVIDER"],
            debug: bool = CONFIG["DEBUG_MODE"]
        ):
        """
        Initialize the Search and QA System
        
        Args:
            csv_path: Path to the CSV file containing QA data
            vector_db_path: Path for storing FAISS vector database
            llm_provider: The LLM provider to use
            debug: Whether to enable debug mode
        """
        self.csv_path = csv_path
        self.vector_db_path = vector_db_path
        self.debug = debug
        self.data = []
        self.index = None
        self.st_model = None
        self.llm_service = LLMService(llm_provider)
        self.last_db_modified_time = 0
        self.is_initialized = False

        init_thread = threading.Thread(target=self._initialize_system)
        init_thread.daemon = True
        init_thread.start()

    def _initialize_system(self) -> None:
        """Initialize system components"""
        try:
            self._load_data()
            self._initialize_models()
            self._setup_vector_database()
            self.is_initialized = True
            logger.info("System initialization complete.")
        except Exception as e:
            logger.error(f"System initialization failed: {str(e)}")

    def _load_data(self) -> None:
        """Load data from CSV file"""
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                self.data = [{key: row[key] for key in row.keys()} for row in csv_reader]
            logger.info(f"Successfully loaded {len(self.data)} records")
        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def _initialize_models(self) -> None:
        """Initialize required models (singleton)"""
        global _GLOBAL_ST_MODEL
        if _GLOBAL_ST_MODEL is not None:
            self.st_model = _GLOBAL_ST_MODEL
            logger.info("Reusing global Sentence Transformer model")
            return
        with _GLOBAL_ST_MODEL_LOCK:
            if _GLOBAL_ST_MODEL is None:
                try:
                    _GLOBAL_ST_MODEL = SentenceTransformer(CONFIG["VECTOR_MODEL"])
                    logger.info("Successfully initialized global Sentence Transformer model")
                except Exception as e:
                    logger.error(f"Error initializing models: {str(e)}")
                    raise
            self.st_model = _GLOBAL_ST_MODEL

    def _setup_vector_database(self) -> None:
        """Set up or load vector database"""
        # 檢查向量資料庫是否存在
        if os.path.exists(self.vector_db_path):
            try:
                # 載入現有的向量資料庫
                self.index = faiss.read_index(self.vector_db_path)
                # 記錄當前資料庫的修改時間
                self.last_db_modified_time = os.path.getmtime(self.vector_db_path)
                logger.info(f"載入現有向量資料庫: {self.vector_db_path}")
            except Exception as e:
                logger.error(f"載入向量資料庫失敗，將重新建立: {str(e)}")
                self._create_vector_database()
        else:
            # 建立新的向量資料庫
            logger.info("向量資料庫不存在，將建立新的資料庫")
            self._create_vector_database()

    def _create_vector_database(self) -> None:
        """Create new vector database"""
        # 確保模型已初始化
        if self.st_model is None:
            logger.info("模型尚未初始化，正在初始化模型...")
            self._initialize_models()

        texts = [f"{d['title']}\n{d['context']}" for d in self.data]
        embeddings = self.st_model.encode(texts)
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        faiss.write_index(self.index, self.vector_db_path)
        logger.info("Successfully created and saved new vector database")

    def _update_vector_database(self) -> None:
        """
        從 CSV 重新產生向量資料庫，並更新索引
        """
        try:
            logger.info("定時重建向量資料庫任務啟動")
            # 確保模型已初始化
            if self.st_model is None:
                logger.info("模型尚未初始化，正在初始化模型...")
                self._initialize_models()
            # 重新讀取最新資料
            self._load_data()
            # 重新建立向量資料庫（此處可依需求選擇只更新向量資料庫，而不重新載入模型）
            self._create_vector_database()
            logger.info("定時重建向量資料庫任務完成")
        except Exception as e:
            logger.error(f"定時重建向量資料庫任務失敗: {e}")

    def _check_db_updated(self) -> bool:
        """
        檢查向量資料庫是否已更新
        
        Returns:
            bool: 如果資料庫已更新則返回 True，否則返回 False
        """
        if not os.path.exists(self.vector_db_path):
            return False
            
        current_modified_time = os.path.getmtime(self.vector_db_path)
        if current_modified_time > self.last_db_modified_time:
            logger.info(f"檢測到向量資料庫已更新: {self.vector_db_path}")
            return True
        return False

    async def search_and_answer(self, query: str, chat_history: List[Dict]) -> Tuple[str, List[Dict]]:
        """
        Search relevant texts and generate answer
        
        Args:
            query: User's question
            
        Returns:
            tuple: (generated answer, list of relevant texts)
        """
        # 檢測語言
        detected_lang = await self.detect_language(query)
        
        # 如果系統尚未初始化，回傳提示訊息
        if not self.is_initialized:
            if detected_lang == "台灣繁體中文" or detected_lang == "zh-TW":
                return "資料庫載入中，請稍後再試。", []
            else:
                return "The database is currently loading. Please try again later.", []

        # 檢查向量資料庫是否已更新，如果更新則重新載入
        if self._check_db_updated():
            try:
                # 重新載入資料
                self._load_data()
                # 重新載入向量資料庫
                self.index = faiss.read_index(self.vector_db_path)
                self.last_db_modified_time = os.path.getmtime(self.vector_db_path)
                logger.info("向量資料庫已重新載入")
            except Exception as e:
                logger.error(f"重新載入向量資料庫失敗: {str(e)}")
                # 繼續使用現有的索引
        
        # 搜索相關文本
        relevant_texts = self._search_relevant_texts(query)
        
        # 生成回答
        chat_his = chat_history[-MAX_HISTORY_ROUND:]
        answer = await self._generate_answer(query, relevant_texts, chat_his, detected_lang)

        chat_history.append({
            "User": query,
            "Assistant": answer,
        })

        # if (chat_his):
        #     logger.info(f"History: {chat_his[-1:]}")

        logger.info(f"Query: {query}")
        logger.info(f"Relevant texts: {relevant_texts}")
        # logger.info(f"Detected language: {detected_lang}")
        logger.info(f"Answer: {answer}")
        
        return answer, relevant_texts

    async def translate_text(self, text: str) -> str:
        """
        Translate Chinese text to English
        
        Args:
            text: Chinese text to translate
            
        Returns:
            Translated English text
        """
        try:
            prompt = TRANSLATION_PROMPT.format(text=text)
            return await self.llm_service.generate_response(prompt)
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise
    
    async def detect_language(self, text: str):
        """
        Detect the language of the given text
        
        Args:
            text: Text to detect language
            
        Returns:
            Detected language
        """
        try:
            prompt = LANGUAGE_DETECTION_PROMPT.format(query=text)
            response = await self.llm_service.generate_response(prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"Language detection error: {str(e)}")

    def _search_relevant_texts(self, query: str) -> List[Dict]:
        """
        Search relevant texts
        
        Args:
            query: User's question
            
        Returns:
            List of relevant texts
        """
        # 確保模型已初始化
        if self.st_model is None:
            logger.info("模型尚未初始化，正在初始化模型...")
            self._initialize_models()
        
        query_vector = self.st_model.encode([query])
        distances, indices = self.index.search(
            query_vector.astype('float32'),
            CONFIG["TOP_K_RESULTS"]
        )
        relevant_texts = [
            f"Title: {self.data[i]['title']}\nContext: {self.data[i]['context']}\nSource: {self.data[i]['url']}"
            for i in indices[0]
        ]

        # Reverse the order of relevant texts
        relevant_texts.reverse()

        if self.debug:
            logger.info(f"Relevant texts: {relevant_texts}")

        return relevant_texts

    async def _format_prompt(self, query: str, relevant_texts: List[Dict], history: List[Dict], lang: str = "zh") -> str:
        """
        Format the prompt for the LLM
        
        Args:
            query: User's question
            relevant_texts: List of relevant texts
            lang: Language of the query
            history: Conversation history (context caching)
            
        Returns:
            Formatted prompt
        """
        chat_history_text = "\n".join([f"User: {h['User']}\nAssistant: {h['Assistant']}" for h in history])

        if lang == "台灣繁體中文" or lang == "zh-TW":
            prompt = QA_PROMPT.format(
                query=query,
                context="\n\n".join(relevant_texts),
                lang=lang,
                previous_chat=chat_history_text
            )
        else:
            prompt = QA_PROMPT_EN.format(
                query=query,
                context="\n\n".join(relevant_texts),
                lang=lang,
                previous_chat=chat_history_text
            )
        return prompt

    async def _generate_answer(self, query: str, relevant_texts: List[Dict], history: List[Dict], detected_lang: str) -> str:
        """
        Generate answer
        
        Args:
            query: User's question
            relevant_texts: List of relevant texts
            history: Conversation history (context caching)
            detected_lang: Detected language
            
        Returns:
            Generated answer
        """
        prompt = await self._format_prompt(query, relevant_texts, history, detected_lang)
        response = await self.llm_service.generate_response(prompt)
        return response
