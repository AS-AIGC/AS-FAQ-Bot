"""
Search and QA System
This module implements a vector search-based QA system using FAISS for similarity search,
combined with multiple LLM providers for text generation and translation.

Dependencies:
    - google.generativeai
    - openai
    - groq
    - sentence_transformers
    - faiss-cpu
    - csv
    - os
    - requests
"""

import os
import csv
import logging
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

# Global Configuration
class LLMProvider(Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    OLLAMA = "ollama"
    GROQ = "groq"

# Global Variables
CONFIG = {
    # File Paths
    "CSV_PATH": "combined_context_en.csv",
    "VECTOR_DB_PATH": "vector_database.bin",
    
    # Default Provider
    "DEFAULT_LLM_PROVIDER": LLMProvider.GEMINI,
    
    # API Keys and Endpoints
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", ""),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
    "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    
    # Model Configuration
    "GEMINI_MODEL": os.getenv("GEMINI_MODEL", "gemini-2.0-flash-001"),
    "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
    "GROQ_MODEL": os.getenv("GROQ_MODEL","mixtral-8x7b-32768"),
    "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL", "llama3.2-vision:latest"),
    
    # Vector Search Configuration
    "VECTOR_MODEL": os.getenv("VECTOR_MODEL", "multi-qa-mpnet-base-dot-v1"),
    "TOP_K_RESULTS": 10,
    
    # Debug Mode
    "DEBUG_MODE": False,
    
    # System Prompts
    "SYSTEM_PROMPT": """
    你是專業問題回覆人員，主要職責是接收並理解用戶的提問...（以下省略）
    """,
    # 翻譯提示
    "TRANSLATION_PROMPT": """
    Task: Translate the following Chinese text to English.
    Maintain the original meaning and context while ensuring natural English expression.
    Only reply with the translated English text.
    
    Chinese text: {text}
    
    Translated English text:
    """,

    # 語言偵測提示
    "LANGUAGE_DETECTION_PROMPT": """
    Task: Detect the language of the following text: "{query}"
    If the text is Chinese, reply "台灣繁體中文". If the text is in any other language, reply "english".
    Only reply with the language code.
    """,
    
    # 問答提示
    # 中文
    "QA_PROMPT": """
    使用者的問題: {query}，以 {lang} 回覆
    {context}
    """,
    
    # 英文
    "QA_PROMPT_EN": """
    USER's QUESTION: "{query}" , response in {lang}
    {context}
    """
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    
    def generate_response(self, prompt: str) -> str:
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
                    system_instruction= CONFIG["SYSTEM_PROMPT"]
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
                response = requests.post(
                    f"{CONFIG['OLLAMA_BASE_URL']}/api/generate",
                    json={
                        "model": CONFIG["OLLAMA_MODEL"],
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "num_ctx": 8192
                        }
                    }
                )
                return response.json()["response"]
                
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
        
        try:
            self._initialize_system()
        except Exception as e:
            logger.error(f"System initialization failed: {str(e)}")
            raise

    def _initialize_system(self) -> None:
        """Initialize system components"""
        self._load_data()
        self._initialize_models()
        self._setup_vector_database()

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
        """Initialize required models"""
        try:
            self.st_model = SentenceTransformer(CONFIG["VECTOR_MODEL"])
            logger.info("Successfully initialized Sentence Transformer model")
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise

    def _setup_vector_database(self) -> None:
        """Set up or load vector database"""
        try:
            if not os.path.exists(self.vector_db_path):
                self._create_vector_database()
            else:
                self.index = faiss.read_index(self.vector_db_path)
                logger.info("Successfully loaded existing vector database")
        except Exception as e:
            logger.error(f"Error setting up vector database: {str(e)}")
            raise

    def _create_vector_database(self) -> None:
        """Create new vector database"""
        texts = [f"{d['en_title']}\n{d['en_context']}" for d in self.data]
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
            # 重新讀取最新資料
            self._load_data()
            # 重新建立向量資料庫（此處可依需求選擇只更新向量資料庫，而不重新載入模型）
            self._create_vector_database()
            logger.info("定時重建向量資料庫任務完成")
        except Exception as e:
            logger.error(f"定時重建向量資料庫任務失敗: {e}")

    def translate_text(self, text: str) -> str:
        """
        Translate Chinese text to English
        
        Args:
            text: Chinese text to translate
            
        Returns:
            Translated English text
        """
        try:
            prompt = CONFIG["TRANSLATION_PROMPT"].format(text=text)
            return self.llm_service.generate_response(prompt)
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise
    
    def detect_language(self, text: str):
        """
        Detect the language of the given text
        
        Args:
            text: Text to detect language
            
        Returns:
            Detected language
        """
        try:
            prompt = CONFIG["LANGUAGE_DETECTION_PROMPT"].format(query=text)
            response = self.llm_service.generate_response(prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"Language detection error: {str(e)}")

    def search_and_answer(self, query: str) -> Tuple[str, List[str]]:
        """
        Search relevant texts and generate answer
        
        Args:
            query: User's question
            
        Returns:
            tuple: (generated answer, list of relevant texts)
        """
        try:
            # Translate query
            en_query = self.translate_text(query)
            query_vector = self.st_model.encode([en_query])

            # Detect language
            lang = self.detect_language(query)
            logger.info(f"Detected language: {lang}")
            
            # Search similar texts
            distances, indices = self.index.search(
                query_vector.astype('float32'),
                CONFIG["TOP_K_RESULTS"]
            )
            
            # Prepare relevant texts
            relevant_texts = [
                f"Title: {self.data[i]['title']}\nContext: {self.data[i]['context']}\nSource: {self.data[i]['url']}"
                for i in indices[0]
            ]
            
            if self.debug:
                logger.debug(f"Relevant texts: {relevant_texts}")
            
            # Build prompt and generate answer
            if lang == "台灣繁體中文" or lang == "zh-TW":
                prompt = CONFIG["QA_PROMPT"].format(
                    query=query,
                    context="\n\n".join(relevant_texts),
                    lang=lang
                )
            else:
                prompt = CONFIG["QA_PROMPT_EN"].format(
                    query=query,
                    context="\n\n".join(relevant_texts),
                    lang=lang
                )
            
            response = self.llm_service.generate_response(prompt)
            return response, relevant_texts
            
        except Exception as e:
            logger.error(f"Error in search and answer process: {str(e)}")
            raise

# Usage example
if __name__ == "__main__":
    try:
        # Initialize system with specific LLM provider
        qa_system = SearchQASystem()  # Uses default values from CONFIG
        
        # Test query
        question = "請問什麼是區塊鏈？"
        answer, sources = qa_system.search_and_answer(question)
        
        print(f"Question: {question}")
        print(f"Answer: {answer}")
        print("Relevant sources:")
        for source in sources:
            print(f"- {source}")
            
    except Exception as e:
        logger.error(f"Error during test execution: {str(e)}")
