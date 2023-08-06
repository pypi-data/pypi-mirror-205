import pandas as pd
import textai as tai
import txtai as tai
import pandas as pd
df = pd.read_csv('data/nlpia_lines.csv')
df
df = pd.read_csv('data/nlpia_lines.csv', index_col=0)
df
df.columns
df[df['is_code_or_output']]
df[~df['line_number']]['filename']
~df['line_number']
df['filename'][df['line_number'] == 1]
from txtai.embeddings import Embeddings

# Create embeddings model, backed by sentence-transformers & transformers
embeddings = Embeddings({"path": "sentence-transformers/nli-mpnet-base-v2"})
hist -f txtai_nli_mpnet.py
