from openai import OpenAI
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from utils import load_openai_config
import japanize_matplotlib


yaml_file = 'config.yaml'
organization, PROJECT_ID, OPENAI_API_KEY = load_openai_config(yaml_file)
if os.environ.get("OPENAI_API_KEY") is None:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

client = OpenAI(
    organization=organization,
    project=PROJECT_ID,
)

def get_embedding(text, model="text-embedding-3-large"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

df = pd.DataFrame(columns=["Time", "ProductId", "UserId", "Score", "Summary", "Text"])
# x = []
# x.append("""
# この文章のEmbeddingを取得してください。
# """)
# x.append("""
# この文章のEmbeddingも取得してください。
# """)
# x.append("""
# 今日もカレーが美味しい日ですか？
# """)
# x.append("""
# このEmbeddingは取得可能ですか？
# """)

df = pd.read_csv('output/jp_sentences.csv')
x = list(map(lambda x:x[0], df.loc[:].to_numpy()))
y = []
for x_ in x:
    y.append(
        np.array(get_embedding(x_, model='text-embedding-3-small'))
    )

similarity_matrix = cosine_similarity(y)
plt.figure(figsize=(18, 18))
sns.heatmap(
        similarity_matrix, annot=True, cmap="coolwarm", fmt=".2f",
        xticklabels=x, yticklabels=x
    )
plt.title("Embedding Cosine Similarity Matrix")

os.makedirs('output', exist_ok=True)
plt.savefig("output/heatmap.png")

df.to_csv('output/embedded_1k_reviews.csv', index=False)