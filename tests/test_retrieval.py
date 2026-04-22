"""
File: test_retrieval.py
Author: Emmanuella Uwudia
Index Number: AI_10012200008
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Test retrieval quality and similarity scoring
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embeddings import GhanaEmbeddingPipeline
from src.vector_store import GhanaVectorStore
from src.retrieval import GhanaRetrievalSystem

def test_basic_retrieval():
    """Test basic retrieval without query expansion"""
    print("\n" + "="*60)
    print("TEST 1: Basic Retrieval (No Query Expansion)")
    print("="*60)
    
    # Load components
    vector_store = GhanaVectorStore()
    vector_store.load_index()
    embedder = GhanaEmbeddingPipeline()
    retriever = GhanaRetrievalSystem(vector_store, embedder)
    
    test_queries = [
        "healthcare budget",
        "education spending",
        "election results",
        "LEAP programme"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        results = retriever.retrieve_with_scores(query, k=3, use_expansion=False)
        
        if results:
            print(f"   Retrieved {len(results)} chunks:")
            for r in results:
                print(f"     • Score: {r['similarity_score']:.3f} | {r['source']}")
                print(f"       {r['text'][:100]}...")
        else:
            print("   No results found")

def test_query_expansion():
    """Test retrieval WITH query expansion"""
    print("\n" + "="*60)
    print("TEST 2: Retrieval with Query Expansion")
    print("="*60)
    
    vector_store = GhanaVectorStore()
    vector_store.load_index()
    embedder = GhanaEmbeddingPipeline()
    retriever = GhanaRetrievalSystem(vector_store, embedder)
    
    test_queries = [
        "healthcare budget",
        "who won",
        "education money",
        "roads spending"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        
        # Show expanded queries
        expanded = retriever.expand_query(query)
        print(f"   Expanded to: {expanded[:3]}")
        
        # Get results
        results = retriever.retrieve_with_scores(query, k=3, use_expansion=True)
        
        if results:
            print(f"   Retrieved {len(results)} chunks:")
            for r in results:
                print(f"     • Score: {r['similarity_score']:.3f} | {r['source']}")
        else:
            print("   No results found")

def test_score_distribution():
    """Test similarity score distribution"""
    print("\n" + "="*60)
    print("TEST 3: Score Distribution Analysis")
    print("="*60)
    
    vector_store = GhanaVectorStore()
    vector_store.load_index()
    embedder = GhanaEmbeddingPipeline()
    retriever = GhanaRetrievalSystem(vector_store, embedder)
    
    test_query = "budget allocation 2025"
    
    results = retriever.retrieve_with_scores(test_query, k=10, use_expansion=True)
    
    if results:
        scores = [r['similarity_score'] for r in results]
        print(f"\n📊 Score Distribution for '{test_query}':")
        print(f"   Highest: {max(scores):.3f}")
        print(f"   Lowest: {min(scores):.3f}")
        print(f"   Average: {sum(scores)/len(scores):.3f}")
        
        print(f"\n   Score breakdown:")
        high = [s for s in scores if s >= 0.7]
        medium = [s for s in scores if 0.4 <= s < 0.7]
        low = [s for s in scores if s < 0.4]
        
        print(f"     High (≥0.7): {len(high)} chunks")
        print(f"     Medium (0.4-0.7): {len(medium)} chunks")
        print(f"     Low (<0.4): {len(low)} chunks")

if __name__ == "__main__":
    print("\n🔍 RETRIEVAL SYSTEM TESTS")
    print("="*60)
    
    test_basic_retrieval()
    test_query_expansion()
    test_score_distribution()
    
    print("\n✅ All retrieval tests complete!")