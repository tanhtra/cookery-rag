# Chef’s AI Assistant – LLM Zoomcamp Project  

Welcome to my **LLM Zoomcamp Project**!  
In this repository, we’ll build an AI Assistant designed to help *chefs in training* navigate the complex knowledgebase of cooking.  

Using techniques like **Retrieval-Augmented Generation (RAG)** and **hybrid search**, we’ll see how an LLM can be grounded in a structured knowledge base to provide trustworthy, context-driven answers.  

---

## Project Motivation  

Cooking is full of concepts, techniques, and rules that beginners can find overwhelming:  

- *What does blanching mean?*  
- *How do you sauté vegetables properly?*  
- *What’s the difference between roasting and baking?*  
- *What can I use instead of buttermilk?*  

Instead of sifting through articles or multiple recipe blogs, this assistant provides **fast, accurate, and context-grounded answers** directly from a curated cooking knowledgebase.  

![Screenshot](img/cookery.png)

---

## Dataset  

We’ll use the dataset **Cooking Knowledge Basics** from Kaggle:  
[Cooking Knowledge Basics Dataset](https://www.kaggle.com/datasets/tiyabk/cooking-knowledge-basics)  

**Format:** CSV with three key columns  
- `type` – category of knowledge
- `question` – student-style cooking question  
- `response` – reference answer  

This makes it perfect for a **knowledge-augmented Q&A assistant**.  

---

### Ingestion

The ingestion script is located in core.ipynb with a copy of it in ingest.py

With the use of minsearch the knowledge base ingestion script should be run during startup.

### Experiments

For experiments, please use the jupyter notebook core.ipynb and rag_eval.ipynb

### Retrieval evaluation

With a basic approach - using minsearch without boosting:
- Hit rate 83.6%
- MRR 64%

With a bit of boosting:
- Hit rate 85.6%
- MRR 66.4%

With the boosting parameter
```json
    boost = {
            'id': 2.7692628744506598,
            'question': 0.3243327894022373,
            'response': 0.5744326020937277
            }
```

### RAG flow evaluation

LLM-as-a-judge was used to evaluate the quality of the RAG flow.

For the default gpt-4o-mini in a sample of 100 records:
- 85% RELEVANT
- 11% PARTLY_RELEVANT
- 4% NON_RELEVANT

The use of gpt-4o was also used:
- 85% RELEVANT
- 12% PARTLY_RELEVANT
- 3% NON_RELEVANT


# Running Cookery-RAG with Docker Compose

Follow these steps to build and run the Cookery-RAG Streamlit app in a containerized environment. Users will enter their OpenAI API key directly in the app UI.

## Prerequisites

- Docker & Docker Compose installed  
- Git installed  

## 1. Clone the Repository

```bash
git clone https://github.com/tanhtra/cookery-rag.git
cd cookery-rag
```

## 2. Verify Project Structure

Ensure you have:

```
cookery-rag/
├── cookery/             ← Python package containing appcore.py
│   └── appcore.py
├── requirements.txt     ← app dependencies
├── Dockerfile           ← builds the Streamlit image
└── docker-compose.yml   ← orchestrates the container
```

## 3. requirements.txt

Include at least:

```
streamlit>=1.28.0
openai
requests
python-dotenv
```

## 4. Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cookery ./cookery

EXPOSE 8501

ENV STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    PYTHONUNBUFFERED=1

CMD ["streamlit", "run", "cookery/appcore.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
*Already included in the repo

## 5. docker-compose.yml

```yaml
version: "3.8"

services:
  cookery-app:
    build: .
    container_name: cookery_streamlit
    ports:
      - "8501:8501"
    volumes:
      - ./cookery:/app/cookery
      - ./requirements.txt:/app/requirements.txt:ro
    restart: unless-stopped
```
*Already included in the repo


## 6. Build and Run

From the repo root:

```bash
docker-compose up --build
```

Streamlit will start inside the container.

## 7. Access the App

Open your browser to:

```
http://localhost:8501
```

## 8. Enter Your OpenAI API Key

1. In the app, you’ll see an **OpenAI API Key** input field.  
2. Paste your OpenAI key (`sk-…`) into the text box.  

## 9. Development Tips

The `cookery` volume mount enables instant reloads when you edit `appcore.py`.  
After installing new Python packages, update `requirements.txt` and rerun:

  ```bash
  docker-compose up --build
  ```

To stop the app:

  ```bash
  docker-compose down
  ```