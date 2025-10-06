import pandas as pd
import minsearch

def load_index(data_path='../data/cooking_knowledge.csv'):
    df_ck = pd.read_csv(datapath)
    df_ck.insert(0, 'ID', df_ck.index)

    documents = df_ck.to_dict(orient='records')

    index = minsearch.Index(
        text_fields=['type', 'question', 'response'],
        keyword_fields=['ID']
    )
    index.fit(documents)