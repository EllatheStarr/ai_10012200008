"""
File: embeddings.py
Author: Student Name
Index Number: AI_20240001
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Custom embedding pipeline for Ghana data
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import json
import time

class GhanaEmbeddingPipeline:
    """
    Custom embedding generation for Ghana election and budget data
    Uses sentence-transformers (no OpenAI embeddings to keep free)
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        all-MiniLM-L6-v2: 384 dimensions, fast, good for semantic search
        """
        print(f"🟡 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.embedding_dimension = 384
        print(f"✅ Model loaded. Embedding dimension: {self.embedding_dimension}")
        
    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for a list of texts
        Returns numpy array of shape (len(texts), embedding_dimension)
        """
        print(f"🟡 Generating embeddings for {len(texts)} texts...")
        
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_embeddings = self.model.encode(batch, convert_to_numpy=True)
            all_embeddings.append(batch_embeddings)
            
            if (i + batch_size) % 100 == 0:
                print(f"  Processed {i + len(batch)}/{len(texts)} texts")
        
        embeddings = np.vstack(all_embeddings)
        print(f"✅ Generated {embeddings.shape[0]} embeddings of dimension {embeddings.shape[1]}")
        
        return embeddings
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query
        """
        embedding = self.model.encode([query], convert_to_numpy=True)
        return embedding[0]
    
    def process_chunks(self, chunks: List[Dict]) -> Dict[str, Any]:
        """
        Generate embeddings for all chunks and return with metadata
        """
        texts = [chunk["text"] for chunk in chunks]
        
        start_time = time.time()
        embeddings = self.generate_embeddings(texts)
        elapsed_time = time.time() - start_time
        
        # Store embeddings with chunk metadata
        chunk_embeddings = []
        for i, chunk in enumerate(chunks):
            chunk_embeddings.append({
                "chunk_id": chunk["chunk_id"],
                "embedding": embeddings[i].tolist(),
                "text": chunk["text"],
                "source": chunk["source"],
                "source_type": chunk["source_type"]
            })
        
        result = {
            "embeddings": embeddings,
            "metadata": {
                "model": self.model_name,
                "dimension": self.embedding_dimension,
                "num_chunks": len(chunks),
                "generation_time_seconds": elapsed_time,
                "average_time_per_chunk_ms": (elapsed_time / len(chunks)) * 1000
            },
            "chunk_embeddings": chunk_embeddings
        }
        
        print(f"\n📊 Embedding Statistics:")
        print(f"  • Total chunks: {len(chunks)}")
        print(f"  • Total time: {elapsed_time:.2f} seconds")
        print(f"  • Average time: {(elapsed_time / len(chunks)) * 1000:.2f} ms per chunk")
        
        return result
    
    def save_embeddings(self, embeddings: np.ndarray, metadata: Dict, output_dir: str = "data/vectors/"):
        """
        Save embeddings and metadata to disk
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Save embeddings as numpy array
        np.save(f"{output_dir}/embeddings.npy", embeddings)
        
        # Save metadata
        with open(f"{output_dir}/embedding_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Saved embeddings to {output_dir}")
        
    def load_embeddings(self, output_dir: str = "data/vectors/") -> tuple:
        """
        Load embeddings and metadata from disk
        """
        embeddings = np.load(f"{output_dir}/embeddings.npy")
        
        with open(f"{output_dir}/embedding_metadata.json", "r") as f:
            metadata = json.load(f)
        
        print(f"✅ Loaded {embeddings.shape[0]} embeddings from {output_dir}")
        return embeddings, metadata


if __name__ == "__main__":
    # Load chunks
    with open("data/processed/all_chunks.json", "r") as f:
        chunks = json.load(f)
    
    # Initialize embedding pipeline
    embedder = GhanaEmbeddingPipeline()
    
    # Generate embeddings
    result = embedder.process_chunks(chunks)
    
    # Save embeddings
    embedder.save_embeddings(result["embeddings"], result["metadata"])
    
    # Test query embedding
    test_query = "What is the healthcare budget for 2025?"
    query_embedding = embedder.embed_query(test_query)
    print(f"\n✅ Test query embedding shape: {query_embedding.shape}")