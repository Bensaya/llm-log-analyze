from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
import uvicorn

from contextlib import asynccontextmanager
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, get_response_synthesizer
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.ollama import Ollama
import os


# Constants and defaults (configure as needed)
BASE_URL = "http://localhost:11434"  # Default Ollama URL
LOG_DIR = "logs"


@asynccontextmanager
async def lifespan(app: FastAPI):
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.core import Settings

    Settings.embed_model = OllamaEmbedding(
        model_name="llama3.2",
        base_url=BASE_URL
    )
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Initialize or load existing index outside the endpoint handlers.
    global index
    documents = SimpleDirectoryReader(input_dir=LOG_DIR, required_exts=[".log"]).load_data()
    index = VectorStoreIndex.from_documents(documents)
    yield
    # Clean up the ML models and release the resources
    print("Server shutting down...")


app = FastAPI(lifespan=lifespan)


@app.post("/query_logs/{query}")
async def query_logs(query: str = None):
    # 2. Load and process the logs
    try:
        llm = Ollama(base_url=BASE_URL, model="llama3.2", request_timeout=60.0)  # Default Ollama URL
        # configure retriever
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=5,
        )

        # configure response synthesizer
        response_synthesizer = get_response_synthesizer(
            response_mode="tree_summarize",
            llm=llm,
        )

        # assemble query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
        )

        # query_engine = index.as_query_engine(llm=llm,
        #                                      response_mode="tree_summarize",
        #                                      verbose=True,)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing logs: {e}")
    # 3. Perform Query (if provided)
    if query:
        try:
            response = query_engine.query(query)
            return PlainTextResponse(str(response))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error querying logs: {e}")
    else:
        return {"message": "Send a query to analyze."}


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)