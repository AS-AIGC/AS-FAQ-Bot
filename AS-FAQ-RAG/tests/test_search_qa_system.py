import os
import pytest
import asyncio
from unittest.mock import patch, MagicMock, mock_open, AsyncMock
import csv
import io
import faiss
import numpy as np
from utils.respond import SearchQASystem, LLMProvider, CONFIG

# 測試 SearchQASystem 類別，包括資料載入、模型初始化、向量資料庫設置、相關文本搜尋和問答功能。

class TestSearchQASystem:
    """SearchQASystem 的單元測試"""

    @patch('utils.respond.SentenceTransformer')
    @patch('utils.respond.faiss')
    @patch('utils.respond.open', new_callable=mock_open, read_data='category,title,context,url,contact,en_title,en_context\nTest,標題,內容,http://example.com,test@example.com,Title,Content')
    @patch('utils.respond.LLMService')
    @patch('utils.respond.os.path.exists')
    def setup_search_qa_system(self, mock_exists, mock_llm_service, mock_file, mock_faiss, mock_st,
                            csv_path="tests/test.csv", vector_db_path="tests/test.bin", llm_provider=LLMProvider.OLLAMA):
        """設置 SearchQASystem 測試環境"""
        # 模擬文件存在檢查
        mock_exists.return_value = True

        # 模擬 SentenceTransformer
        mock_st_instance = MagicMock()
        mock_st_instance.encode.return_value = np.array([[0.1, 0.2, 0.3, 0.4, 0.5]])
        mock_st.return_value = mock_st_instance

        # 模擬 FAISS
        mock_index = MagicMock()
        mock_index.search.return_value = (np.array([[0.1, 0.2, 0.3]]), np.array([[0, 1, 2]]))
        mock_faiss.read_index.return_value = mock_index

        # 模擬 LLMService 並使用 AsyncMock 模擬異步 generate_response
        mock_llm_instance = MagicMock()
        mock_llm_instance.generate_response = AsyncMock()
        mock_llm_service.return_value = mock_llm_instance

        # 創建系統
        system = SearchQASystem(
            csv_path=csv_path,
            vector_db_path=vector_db_path,
            llm_provider=llm_provider
        )

        return system, mock_st_instance, mock_index, mock_llm_instance

    def test_load_data(self):
        """測試載入數據"""
        system, _, _, _ = self.setup_search_qa_system()
        assert len(system.data) == 1
        assert system.data[0]['title'] == '標題'
        assert system.data[0]['context'] == '內容'
        assert system.data[0]['url'] == 'http://example.com'

    def test_initialize_models(self):
        """測試初始化模型"""
        system, mock_st_instance, _, _ = self.setup_search_qa_system()
        assert system.st_model == mock_st_instance

    @patch('utils.respond.os.path.exists')
    def test_setup_vector_database_new(self, mock_exists):
        """測試設置向量數據庫 - 創建新的"""
        mock_exists.return_value = False
        with patch('utils.respond.open', new_callable=mock_open, read_data='category,title,context,url,contact,en_title,en_context\nTest,標題,內容,http://example.com,test@example.com,Title,Content'):
            with patch('utils.respond.SentenceTransformer') as mock_st:
                with patch('utils.respond.faiss') as mock_faiss:
                    with patch('utils.respond.LLMService'):
                        # 模擬 SentenceTransformer
                        mock_st_instance = MagicMock()
                        mock_st_instance.encode.return_value = np.array([[0.1, 0.2, 0.3, 0.4, 0.5]])
                        mock_st.return_value = mock_st_instance

                        # 創建系統
                        system = SearchQASystem(
                            csv_path="test.csv",
                            vector_db_path="test.bin",
                            llm_provider=LLMProvider.OLLAMA
                        )

                        # 驗證創建了新的向量數據庫
                        mock_faiss.IndexFlatL2.assert_called_once()
                        mock_faiss.write_index.assert_called_once()

    @patch('utils.respond.os.path.exists')
    def test_search_relevant_texts(self, mock_exists):
        """測試搜索相關文本"""
        mock_exists.return_value = True
        system, mock_st_instance, mock_index, _ = self.setup_search_qa_system()

        # 添加測試數據
        system.data = [
            {'title': '標題1', 'context': '內容1', 'url': 'http://example.com/1'},
            {'title': '標題2', 'context': '內容2', 'url': 'http://example.com/2'},
            {'title': '標題3', 'context': '內容3', 'url': 'http://example.com/3'}
        ]

        # 測試搜索
        results = system._search_relevant_texts("測試查詢")

        # 驗證結果
        assert len(results) == 3
        mock_st_instance.encode.assert_called_once_with(["測試查詢"])
        mock_index.search.assert_called_once()

    @patch('utils.respond.os.path.exists')
    def test_format_prompt(self, mock_exists):
        """測試格式化提示"""
        mock_exists.return_value = True
        system, _, _, _ = self.setup_search_qa_system()
        
        loop = asyncio.get_event_loop()
        prompt = loop.run_until_complete(system._format_prompt(
            "測試問題",
            ["文本1", "文本2"],
            "台灣繁體中文"
        ))
        
        assert "測試問題" in prompt
        assert "文本1" in prompt
        assert "文本2" in prompt

    @patch('utils.respond.os.path.exists')
    def test_search_and_answer(self, mock_exists):
        """測試搜索和回答流程"""
        mock_exists.return_value = True
        system, mock_st_instance, mock_index, mock_llm = self.setup_search_qa_system()
        
        # 設置語言檢測和生成回答的返回值
        mock_llm.generate_response.side_effect = ["台灣繁體中文", "模擬回答"]
        # 避免實際搜尋數據，直接返回模擬結果列表
        system._search_relevant_texts = MagicMock(return_value=["文本A", "文本B", "文本C"])
        # 修正：強制設為已初始化，避免回傳『資料庫載入中，請稍後再試。』
        system.is_initialized = True
        
        # 測試搜索和回答
        loop = asyncio.get_event_loop()
        answer, sources = loop.run_until_complete(system.search_and_answer("測試問題"))
        
        # 驗證結果
        assert answer == "模擬回答"
        assert len(sources) == 3  # 使用模擬的相關文本列表
        assert mock_llm.generate_response.call_count == 2  # 語言檢測和生成回答