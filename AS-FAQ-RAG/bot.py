import os
from utils.respond import SearchQASystem
os.environ['GOOGLE_API_KEY'] = 'XXXXX' # 設置Google API密鑰


question = "請問有哪些學術研究計畫可以申請？"
question = "請問中研院南部院區的停車規定?"
question = "請問有哪些事項需所務會議決議後，送院方報備?"

qa_system = SearchQASystem()
answer, sources = qa_system.search_and_answer(question)

print("Answer:", answer)
