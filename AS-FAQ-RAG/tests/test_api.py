import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from api import app, stream_response, CONFIG

# 測試 FastAPI 端點，確保問答 API 可以正常工作，包括成功案例和錯誤處理。

client = TestClient(app)

class TestAPI:
    """API 端點的單元測試"""
    
    @pytest.mark.asyncio
    @patch('api.qa_system')
    async def test_stream_response_success(self, mock_qa_system):
        """測試成功的響應流"""
        # 模擬 QA 系統的回應
        mock_qa_system.search_and_answer = AsyncMock()
        mock_qa_system.search_and_answer.return_value = ("模擬回答", ["來源1", "來源2"])
        
        # 獲取流回應
        generator = stream_response("測試問題")
        response = await anext(generator)
        
        # 驗證結果
        data = json.loads(response)
        assert data["answer"] == "模擬回答"
        assert data["sources"] == ["來源1", "來源2"]
        mock_qa_system.search_and_answer.assert_called_once_with("測試問題")
    
    @pytest.mark.asyncio
    @patch('api.qa_system')
    async def test_stream_response_error(self, mock_qa_system):
        """測試錯誤處理"""
        # 模擬錯誤情況
        mock_qa_system.search_and_answer = AsyncMock()
        mock_qa_system.search_and_answer.side_effect = Exception("測試錯誤")
        
        # 獲取流回應
        generator = stream_response("測試問題")
        response = await anext(generator)
        
        # 驗證結果
        data = json.loads(response)
        assert "error" in data
        assert data["error"] == "An internal error has occurred!"
    
    @patch('api.stream_response')
    def test_ask_question_endpoint(self, mock_stream_response):
        """測試 /ask 端點"""
        # 模擬流回應
        mock_stream_response.return_value = (item for item in ['{"answer": "測試回答", "sources": []}'])
        
        # 發送請求到端點
        response = client.post("/ask", json={"question": "測試問題"})
        
        # 驗證結果
        assert response.status_code == 200
        mock_stream_response.assert_called_once_with("測試問題")
    
    def test_ask_question_missing_question(self):
        """測試缺少問題時的錯誤處理"""
        # 發送請求到端點，但沒有提供問題
        response = client.post("/ask", json={})
        
        # 驗證結果
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["error"] == "Question not provided"

    def test_get_embedding_info(self):
        """測試 /api/rag/embedding-info 端點"""
        # 發送請求到端點
        response = client.get("/api/rag/embedding-info")
        
        # 驗證結果
        assert response.status_code == 200
        data = response.json()
        assert "embedding_model" in data
        assert data["embedding_model"] == CONFIG["VECTOR_MODEL"]

    def test_get_llm_info(self):
        """測試 /api/rag/llm-info 端點"""
        # 發送請求到端點
        response = client.get("/api/rag/llm-info")
        
        # 驗證結果
        assert response.status_code == 200
        data = response.json()
        assert "llm_provider" in data
        assert data["llm_provider"] == CONFIG["DEFAULT_LLM_PROVIDER"].value