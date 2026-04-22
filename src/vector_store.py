"""
File: vector_store.py
Author: Student Name
Index Number: AI_20240001
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: FAISS vector store implementation for Ghana data
"""

import numpy as np
import faiss
import json
from typing import List, Dict, Tuple, Any
import os

class GhanaVectorStore:
    """
    Custom FAISS vector store for Ghana election and budget embeddings
    """
    
    def __init__(self, embedding_dimension: int = 384):
        self.embedding_dimension = embedding_dimension
        self.index = None
        self.chunks = []
        self.chunk_ids = []
        
    def build_index(self, embeddings: np.ndarray, chunks: List[Dict]):
        """
        Build FAISS index from embeddings
        """
        print("🟡 Building FAISS index...")
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create index
        self.index = faiss.IndexFlatIP(self.embedding_dimension)  # Inner Product = Cosine after normalization
        self.index.add(embeddings)
        
        # Store chunks
        self.chunks = chunks
        self.chunk_ids = [chunk["chunk_id"] for chunk in chunks]
        
        print(f"✅ Built index with {self.index.ntotal} vectors")
        
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """
        Search for top-k similar chunks
        Returns list of chunks with similarity scores
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")
        
        # Ensure query is 2D
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Normalize query
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, k)
        
        # Format results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx != -1 and idx < len(self.chunks):
                chunk = self.chunks[idx].copy()
                chunk["similarity_score"] = float(score)  # Cosine similarity after normalization
                chunk["rank"] = i + 1
                results.append(chunk)
        
        return results
    
    def save_index(self, output_dir: str = "data/vectors/"):
        """
        Save FAISS index and chunk metadata
        """
        os.makedirs(output_dir, exist_ok=True)
        
        if self.index is not None:
            faiss.write_index(self.index, f"{output_dir}/faiss_index.bin")
        
        # Save chunk metadata
        metadata = {
            "chunks": self.chunks,
            "chunk_ids": self.chunk_ids,
            "embedding_dimension": self.embedding_dimension,
            "num_vectors": self.index.ntotal if self.index else 0
        }
        
        with open(f"{output_dir}/chunk_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Saved FAISS index and metadata to {output_dir}")
    
    def load_index(self, output_dir: str = "data/vectors/"):
        """
        Load FAISS index and chunk metadata
        """
        index_path = os.path.join(output_dir, "faiss_index.bin")
        metadata_path = os.path.join(output_dir, "chunk_metadata.json")
        embeddings_path = os.path.join(output_dir, "embeddings.npy")
        
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            print(f"✅ Loaded FAISS index with {self.index.ntotal} vectors")
        else:
            # Deployment-safe fallback: rebuild index if embeddings + metadata are available.
            if os.path.exists(embeddings_path) and os.path.exists(metadata_path):
                print(f"⚠️ Index not found at {index_path}. Rebuilding from saved embeddings...")

                with open(metadata_path, "r") as f:
                    metadata = json.load(f)

                chunks = metadata.get("chunks", [])
                embeddings = np.load(embeddings_path).astype("float32")

                if embeddings.ndim != 2 or embeddings.shape[1] != self.embedding_dimension:
                    raise ValueError(
                        f"Embeddings shape {embeddings.shape} does not match expected dimension {self.embedding_dimension}."
                    )

                self.build_index(embeddings, chunks)
                self.save_index(output_dir)
                print("✅ Rebuilt and saved FAISS index successfully")
            else:
                raise FileNotFoundError(
                    f"Index not found at {index_path} and fallback files are missing. "
                    f"Expected {embeddings_path} and {metadata_path}."
                )
        
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            self.chunks = metadata["chunks"]
            self.chunk_ids = metadata["chunk_ids"]
            print(f"✅ Loaded {len(self.chunks)} chunks from metadata")
        
        return self.index is not None


if __name__ == "__main__":
    # Load embeddings
    embeddings = np.load("data/vectors/embeddings.npy")
    
    with open("data/processed/all_chunks.json", "r") as f:
        chunks = json.load(f)
    
    # Build vector store
    vector_store = GhanaVectorStore(embedding_dimension=384)
    vector_store.build_index(embeddings, chunks)
    
    # Save index
    vector_store.save_index()
    
    print(f"\n📊 Vector Store Statistics:")
    print(f"  • Total vectors: {vector_store.index.ntotal}")
    print(f"  • Total chunks: {len(vector_store.chunks)}")
    print(f"  • Embedding dimension: {vector_store.embedding_dimension}")