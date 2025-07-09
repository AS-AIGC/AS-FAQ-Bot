"""
AS-FAQ-RAG 測試模組

此測試模組包含針對 AS-FAQ-RAG 系統的單元測試，用於確保系統各個組件的正確性和穩定性。
測試涵蓋了 LLM 服務、搜索與問答系統以及 API 端點等核心功能。
"""

import os
import sys

# 添加專案根目錄到 Python 路徑中，確保測試可以正確匯入專案中的模組
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))