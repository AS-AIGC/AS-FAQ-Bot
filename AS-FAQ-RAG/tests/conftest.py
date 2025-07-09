import os
import sys
import pytest
from unittest.mock import MagicMock, AsyncMock

# 設定測試環境，提供模擬（mock）對象以便測試時使用。

# 將專案根目錄添加到 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_llm_service():
    """提供 LLMService 的 Mock 對象以便測試"""
    mock_service = MagicMock()
    # 使用 AsyncMock 以模擬異步 generate_response 方法
    mock_service.generate_response = AsyncMock(return_value="這是一個模擬的 LLM 回應")
    return mock_service

@pytest.fixture
def mock_sentence_transformer():
    """提供 SentenceTransformer 的 Mock 對象以便測試"""
    mock_transformer = MagicMock()
    mock_transformer.encode.return_value = [[0.1, 0.2, 0.3, 0.4, 0.5]]
    return mock_transformer

@pytest.fixture
def mock_faiss_index():
    """提供 FAISS Index 的 Mock 對象以便測試"""
    mock_index = MagicMock()
    mock_index.search.return_value = ([0.1, 0.2, 0.3], [[0, 1, 2]])
    return mock_index