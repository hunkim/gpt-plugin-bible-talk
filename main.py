from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from bible_search import search, build_or_load_index

app = FastAPI()

# Build or load the FAISS index and metadata
index, metadata = build_or_load_index()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")


@app.get("/search")
def search_bible_vector(query: str):
   search_results = search(query, index, metadata, top_k=10)
   return search_results