# Search and QA System

A powerful vector search-based Question Answering system that combines FAISS similarity search with multiple Language Model providers for text generation and translation. The system supports multilingual capabilities with Chinese-to-English translation and uses state-of-the-art embedding models for semantic search.

## Features

- Multiple LLM provider support (Gemini, OpenAI, Groq, Ollama)
- Vector-based semantic search using FAISS
- Multilingual support with Chinese-to-English translation
- Configurable context retrieval
- Source attribution for answers
- Debug mode for detailed logging
- Persistent vector database storage

## Prerequisites

- Python 3.7+
- Required API keys for chosen LLM providers
- Sufficient disk space for vector database storage

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd search-qa-system
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Set up your environment variables in the `.env` file:

```bash
cp .env.example .env
```

Edit the `.env` file to include your API keys:

```env
GOOGLE_API_KEY=your-google-api-key
OPENAI_API_KEY=your-openai-api-key
GROQ_API_KEY=your-groq-api-key
OLLAMA_BASE_URL=http://localhost:11434  # Default for local Ollama
```

## System Configuration

The system configuration can be customized through the `CONFIG` dictionary:

```python
CONFIG = {
    "CSV_PATH": "combined_context_en.csv",
    "VECTOR_DB_PATH": "vector_database.bin",
    "DEFAULT_LLM_PROVIDER": LLMProvider.GEMINI,
    "VECTOR_MODEL": "multi-qa-mpnet-base-dot-v1",
    "TOP_K_RESULTS": 5,
    # ... other configurations
}
```

## Usage

### Basic Usage

```python
from search_qa_system import SearchQASystem, LLMProvider

# Initialize the system
qa_system = SearchQASystem()

# Ask a question (supports Chinese)
question = "請問什麼是區塊鏈？"
answer, sources = qa_system.search_and_answer(question)

print(f"Question: {question}")
print(f"Answer: {answer}")
print("Sources:")
for source in sources:
    print(f"- {source}")
```

### Using Different LLM Providers

```python
# Initialize with specific provider
qa_system = SearchQASystem(llm_provider=LLMProvider.OPENAI)

# Or with Groq
qa_system = SearchQASystem(llm_provider=LLMProvider.GROQ)
```

### Debug Mode

```python
# Enable debug mode for detailed logging
qa_system = SearchQASystem(debug=True)
```

## System Architecture

1. **Data Loading**: System loads QA pairs from a CSV file containing titles, contexts, and source URLs.

2. **Vector Database**:
   - Uses FAISS for efficient similarity search
   - Embeddings generated using Sentence Transformers
   - Persistent storage of vector database

3. **Query Processing**:
   - Translation of Chinese queries to English
   - Vector embedding of queries
   - Similarity search for relevant contexts
   - LLM-based answer generation with source attribution

4. **LLM Integration**:
   - Modular design supporting multiple LLM providers
   - Configurable model selection for each provider
   - Error handling and logging

## CSV Data Format

The system expects a CSV file with the following columns:
- `title`: Content title
- `context`: Main content text
- `url`: Source URL
- `en_title`: English title (if available)
- `en_context`: English context (if available)

## Error Handling

The system includes comprehensive error handling and logging:
- Initialization errors
- API connection issues
- Data loading problems
- Vector database operations
- LLM generation errors

## Logging

Logging is configured with the following format:
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Add your license information here]

## Acknowledgments

- FAISS by Facebook Research
- Sentence Transformers by UKPLab
- Various LLM providers (Google, OpenAI, Groq, Ollama)
