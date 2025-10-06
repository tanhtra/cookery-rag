import streamlit as st
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
import traceback

import pandas as pd
from openai import OpenAI
import minsearch

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

df_ck = pd.read_csv('data/cooking_knowledge.csv')
df_ck.insert(0, 'ID', df_ck.index)
documents = df_ck.to_dict(orient='records')

index = minsearch.Index(
    text_fields=['type', 'question', 'response'],
    keyword_fields=['ID']
)
index.fit(documents)

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

def llm(prompt, model='gpt-4o-mini', key_string=''):
    client = OpenAI(api_key=key_string)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
    
def rag(query, model='gpt-4o-mini', key_string=''):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt, model=model, key_string=key_string)
    return answer

def execute_code(code_string, key_string):
    """
        Ask the question - query the LLM
    """
    if not code_string.strip():
        return "", ""

    # Create string buffers to capture output
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    try:
        # Redirect stdout and stderr to capture output
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            # Execute the code
            answer = rag(code_string, 'gpt-4o-mini', key_string)
            print(answer)

        # Get the captured output
        output = stdout_buffer.getvalue()
        error = stderr_buffer.getvalue()

        return output, error

    except Exception as e:
        # Capture any execution errors
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        return "", error_msg

def main():
    st.title("Cookery App - Let me help you cook up a meal... safely")
    st.markdown("What is your question?  And it better be cooking related...")

    # Create tabs for better organization
    tab1, tab2 = st.tabs(["Question field", "How to"])

    with tab1:
        # Code input area
        code_input = st.text_area("Enter your question:")
        key_input = st.text_input("Enter OpenAI Key:", type='password')

        # Execution button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            run_button = st.button("Ask the question", type="primary")
        with col2:
            clear_button = st.button("Forget about it")

        if clear_button:
            st.rerun()

        # Execute code when button is pressed
        if run_button and code_input:
            with st.spinner("Executing code..."):
                output, error = execute_code(code_input, key_input)

            # Display results
            if output:
                st.subheader("Answer to the cooking:")
                st.write(output)

            if error:
                st.subheader("Error:")
                st.error(error)

        elif run_button and not code_input:
            st.warning("Please type in a question before you ask for the question to be answered...")

    with tab2:
        st.markdown("""
            # About Cookery RAG

            Cookery RAG is your intelligent culinary companion powered by advanced language models. Whether you're a beginner cook looking for basic techniques or an experienced chef seeking inspiration, our AI assistant is designed to help you navigate the world of cooking with confidence.

            ## What CookingBot AI Can Help You With

            **Recipe Assistance** - Get step-by-step cooking instructions, ingredient substitutions, and recipe modifications

            **Technique Guidance** - Learn proper cooking methods, knife skills, and kitchen fundamentals

            **Flavour Pairing** - Discover which ingredients work well together and how to balance flavours

            **Dietary Adaptations** - Modify recipes for vegetarian, vegan, gluten-free, and other dietary needs

            **Troubleshooting** - Fix cooking mishaps and learn from kitchen mistakes

            ## Why Choose Cookery RAG?

            - **Instant Answers**: Get immediate responses to your cooking questions 24/7
            - **Personalised Guidance**: Tailored advice based on your skill level and preferences
            - **Global Cuisine Knowledge**: Explore recipes and techniques from around the world
            - **Safe & Reliable**: Focused specifically on culinary topics with food safety awareness

            Ready to elevate your cooking game? Ask Cookery RAG anything about food, recipes, techniques, or kitchen tips!
        """)

if __name__ == "__main__":
    main()