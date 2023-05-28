import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle

# Load Sentence Transformer Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to load and preprocess the CSV file
def load_and_preprocess_data(filename):
    df = pd.read_csv(filename)  # Load the CSV file
    df.columns = ['index', 'book', 'book_id', 'chapter', 'verse', 'text']  # Set the column names
    df = df.dropna(subset=['text'])  # Drop rows with NaN in 'text' column
    df['vector'] = df['text'].apply(lambda x: model.encode(x))  # Create embeddings for each verse
    matrix = np.vstack(df['vector'])  # Convert the list of vectors into a matrix
    return df, matrix

# Save the index and metadata to files
def save_index(index, metadata, index_file, metadata_file):
    faiss.write_index(index, index_file)
    with open(metadata_file, 'wb') as f:
        pickle.dump(metadata, f)

# Load the index and metadata from files
def load_index(index_file, metadata_file):
    index = faiss.read_index(index_file)
    with open(metadata_file, 'rb') as f:
        metadata = pickle.load(f)
    return index, metadata

# Build or load the FAISS index and metadata
def build_or_load_index( df_file = 'bible.csv',index_file = 'bible_index.faiss', metadata_file = 'bible_metadata.pkl'):
    if os.path.exists(index_file) and os.path.exists(metadata_file):
        index, metadata = load_index(index_file, metadata_file)
    else:
        df, matrix = load_and_preprocess_data(df_file)
        index = faiss.IndexFlatL2(matrix.shape[1])
        index.add(matrix)
        metadata = df[['index', 'book', 'book_id', 'chapter', 'verse', 'text']].to_dict()
        save_index(index, metadata, index_file, metadata_file)
    return index, pd.DataFrame(metadata)

# Now you can search the index
# Now you can search the index
def search(query, index, metadata, top_k=10):
    query_vector = model.encode(query)
    D, I = index.search(np.array([query_vector]), top_k)
    results = []
    for i in range(I.shape[1]):
        data = metadata.iloc[I[0][i]].to_dict()
        # remove index, book_id from data
        data.pop('index')
        data.pop('book_id')
        results.append(data)

    # remove index, book_id from results
    return results

if __name__ == "__main__":
    # Example usage
    df_file = 'bible.csv'
    index_file = 'bible_index.faiss'
    metadata_file = 'bible_metadata.pkl'
    index, metadata = build_or_load_index(df_file, index_file, metadata_file)
    results = search('In the beginning God created the heavens and the earth.', index, metadata)
    print(results)