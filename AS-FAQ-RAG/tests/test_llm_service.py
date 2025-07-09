import os
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from utils.respond import LLMService, LLMProvider, CONFIG

# 測試 LLMService 類別，確保不同 LLM 提供者（Gemini、OpenAI、Groq、Ollama）可以正常初始化和生成回應。

class TestLLMService:
    """LLMService 的單元測試"""

    # 測試 _setup_provider
    @patch('utils.respond.genai')
    def test_gemini_setup(self, mock_genai):
        """測試 Gemini 提供者初始化"""
        # 設置環境變量
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
            with patch.dict(CONFIG, {"GOOGLE_API_KEY": "test-key"}):
                service = LLMService(LLMProvider.GEMINI)
                mock_genai.configure.assert_called_once_with(api_key="test-key")

    @patch('utils.respond.openai')
    def test_openai_setup(self, mock_openai):
        """測試 OpenAI 提供者初始化"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch.dict(CONFIG, {"OPENAI_API_KEY": "test-key"}):
                service = LLMService(LLMProvider.OPENAI)
                mock_openai.OpenAI.assert_called_once_with(api_key="test-key")

    @patch('utils.respond.Groq')
    def test_groq_setup(self, mock_groq):
        """測試 Groq 提供者初始化"""
        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}):
            with patch.dict(CONFIG, {"GROQ_API_KEY": "test-key"}):
                service = LLMService(LLMProvider.GROQ)
                mock_groq.assert_called_once_with(api_key="test-key")

    # 測試 generate_response 方法
    @patch('utils.respond.requests.post')
    @patch('utils.respond.asyncio')
    def test_ollama_generate_response(self, mock_asyncio, mock_post):
        """測試 Ollama 生成回應"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "模擬回應"}
        # 使用 AsyncMock 提供 to_thread 返回值
        mock_asyncio.to_thread = AsyncMock(return_value=mock_response)

        service = LLMService(LLMProvider.OLLAMA)
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(service.generate_response("測試提示"))

        assert result == "模擬回應"
        mock_asyncio.to_thread.assert_called_once()

    @patch('utils.respond.genai')
    def test_gemini_generate_response(self, mock_genai):
        """測試 Gemini 生成回應"""
        # 設置模擬返回值
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "模擬 Gemini 回應"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        # 創建服務並調用方法
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
            with patch.dict(CONFIG, {"GOOGLE_API_KEY": "test-key"}):
                service = LLMService(LLMProvider.GEMINI)
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete(service.generate_response("測試提示"))

        # 驗證結果
        assert result == "模擬 Gemini 回應"
        mock_model.generate_content.assert_called_once_with("測試提示")

    def test_missing_api_key(self):
        """測試缺少 API 密鑰時的錯誤處理"""
        with patch.dict(CONFIG, {"GOOGLE_API_KEY": ""}):
            with pytest.raises(ValueError, match="GOOGLE_API_KEY not set"):
                LLMService(LLMProvider.GEMINI)

        with patch.dict(CONFIG, {"OPENAI_API_KEY": ""}):
            with pytest.raises(ValueError, match="OPENAI_API_KEY not set"):
                LLMService(LLMProvider.OPENAI)

        with patch.dict(CONFIG, {"GROQ_API_KEY": ""}):
            with pytest.raises(ValueError, match="GROQ_API_KEY not set"):
                LLMService(LLMProvider.GROQ)