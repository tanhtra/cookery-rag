import pandas as pd
import os, json
from tqdm.auto import tqdm
from openai import OpenAI

client = OpenAI()

entry_template = """
    type: {type}
    question: {question}
    answer: {response}
    """.strip()

prompt_template = """
    You're a cooking course instructor. Answer the QUESTION based on the CONTEXT from the cooking knowledge database.
    Use only the facts from the CONTEXT when answering the QUESTION.
    
    QUESTION: {question}
    
    CONTEXT: 
    {context}
    """.strip()

def search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )
    return results

def build_prompt(query, search_results):
    context = ""
    
    for doc in search_results:
        context = context + entry_template.format(**doc) + "\n\n"
            
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

def llm(prompt, model='gpt-4o-mini'):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
    
def rag(query, model='gpt-4o-mini'):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt, model=model)
    return answer