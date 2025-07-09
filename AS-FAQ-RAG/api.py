from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import AsyncGenerator
import json
import logging
from utils.respond import SearchQASystem, CONFIG, LLMProvider

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以根據需要設置允許的來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Search and QA System
qa_system = SearchQASystem()

async def stream_response(query: str) -> AsyncGenerator[str, None]:
    """
    Async generator function to stream the response.
    
    Args:
        query: User's question.
        
    Yields:
        Chunks of the generated response.
    """
    try:
        answer, sources = await qa_system.search_and_answer(query)
        # print(f"User Question: {query}")
        # print(f"AI Answer: {answer}")
        yield json.dumps({"answer": answer, "sources": sources})
    except Exception as e:
        # Log the error on the server
        logger.error("An error occurred: %s", str(e))
        # Return an error response to the client
        yield json.dumps({"error": "An internal error has occurred!"})
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/ask")
async def ask_question(request: Request):
    """
    API endpoint to handle user questions.
    
    Args:
        request: HTTP request object containing the user's question.
        
    Returns:
        StreamingResponse: Streamed response containing the answer and sources.
    """
    data = await request.json()
    query = data.get("question", "")
    
    if not query:
        return {"error": "Question not provided"}
    
    return StreamingResponse(stream_response(query), media_type="application/json")

@app.get("/api/rag/embedding-info")
def get_embedding_info():
    """
    API endpoint to get the current embedding model information.
    
    Returns:
        dict: A dictionary containing the embedding model name.
    """
    return {"embedding_model": CONFIG["VECTOR_MODEL"]}

@app.get("/api/rag/llm-info")
def get_llm_info():
    """
    API endpoint to get the current LLM provider information.
    
    Returns:
        dict: A dictionary containing the LLM provider name.
    """
    return {"llm_provider": CONFIG["DEFAULT_LLM_PROVIDER"].value}