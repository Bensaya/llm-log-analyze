# Log Analysis with FastAPI, LlamaIndex, and Ollama

This project demonstrates how to build a log analysis service using FastAPI, LlamaIndex, and Ollama.  It allows users to create a searchable index, and query the index using natural language. Persistence is implemented using the file system, but can be adapted for a database in production.


![Log Analysis Flow](llama-logs2.png) 


## Features

* *Asynchronous Indexing:*  Log files are indexed in the background using LlamaIndex and Ollama.
* *Natural Language Querying:*  Query the log data using natural language via POST request to /query_logs/your_query.


## Requirements

* Python 3.9+
* Ollama (running locally)


## Setup

1. Ensure Ollama is running locally (default: http://localhost:11434).  You can change the default base_url if needed.
2. Run the following:
bash
ollama run llama3.2 

bash
git clone https://github.paypal.com/GRS-TLV/llm-log-analyzer-example.git 

bash
cd logs_analyzer && pip install -r requirments.txt 

bash
python3 server.py

## Usage
See example usage in [client.ipynb](client.ipynb) notebook outputs.

### 1. Query the logs in logs directory

bash
curl -X POST http://127.0.0.1:8000/query_logscreate%20report%20of%20the%20"ERROR"%20state%20builds%20on%20linux/

### 2. Use from script
bash
python3 client.py