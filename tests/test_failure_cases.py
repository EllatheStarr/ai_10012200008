"""
File: test_failure_cases.py
Author: Emmanuella Uwudia
Index Number: AI_10012200008
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Test retrieval failure cases and fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embeddings import GhanaEmbeddingPipeline
from src.vector_store import GhanaVectorStore
from src.retrieval import GhanaRetrievalSystem
from src.rag_pipeline import GhanaRAGPipeline

def test_ambiguous_queries():
    """Test how system handles ambiguous queries"""
    print("\n" + "="*60)
    print("TEST 1: Ambiguous Query Handling")
    print("="*60)
    
    vector_store = GhanaVectorStore()
    vector_store.load_index()
    embedder = GhanaEmbeddingPipeline()
    retriever = GhanaRetrievalSystem(vector_store, embedder)
    
    ambiguous_queries = [
        ("who won", "Missing context - which election?"),
        ("tell me about it", "Vague pronoun - what is 'it'?"),
        ("what about", "Incomplete question"),
        ("budget", "Too broad - which budget?"),
        ("election", "Too broad - which election?")
    ]
    
    for query, issue in ambiguous_queries:
        print(f"\n📝 Query: '{query}'")
        print(f"   Issue: {issue}")
        
        # Without fix
        results_no_fix = retriever.retrieve_with_scores(query, k=3, use_expansion=False)
        print(f"   Without expansion: {len(results_no_fix)} results")
        if results_no_fix:
            print(f"     Top score: {results_no_fix[0]['similarity_score']:.3f}")
        
        # With fix (query expansion)
        results_with_fix = retriever.retrieve_with_scores(query, k=3, use_expansion=True)
        print(f"   WITH expansion: {len(results_with_fix)} results")
        if results_with_fix:
            print(f"     Top score: {results_with_fix[0]['similarity_score']:.3f}")
        
        # Assess improvement
        improvement = len(results_with_fix) > len(results_no_fix)
        print(f"   Improvement: {'✅ YES' if improvement else '❌ NO'}")

def test_out_of_scope_queries():
    """Test how system handles out-of-scope queries"""
    print("\n" + "="*60)
    print("TEST 2: Out-of-Scope Query Handling")
    print("="*60)
    
    rag = GhanaRAGPipeline()
    
    out_of_scope_queries = [
        "What is the capital of France?",
        "Who won the World Cup?",
        "How do I bake a cake?",
        "Tell me about climate change",
        "What is the meaning of life?"
    ]
    
    for query in out_of_scope_queries:
        print(f"\n📝 Query: '{query}'")
        result = rag.process_query(query, k=3)
        
        response_lower = result["response"].lower()
        
        # Check for appropriate refusal
        appropriate_refusal = any(phrase in response_lower for phrase in [
            "only have information about ghana",
            "cannot answer",
            "outside my scope",
            "couldn't find",
            "elections and budget"
        ])
        
        print(f"   Response: {result['response'][:150]}...")
        print(f"   Appropriate refusal: {'✅ YES' if appropriate_refusal else '❌ NO'}")

def test_low_confidence_queries():
    """Test how system handles low confidence retrieval"""
    print("\n" + "="*60)
    print("TEST 3: Low Confidence Query Handling")
    print("="*60)
    
    vector_store = GhanaVectorStore()
    vector_store.load_index()
    embedder = GhanaEmbeddingPipeline()
    retriever = GhanaRetrievalSystem(vector_store, embedder)
    
    low_confidence_queries = [
        "purple elephant budget",
        "imaginary programme xyz",
        "nonsense query that doesn't exist"
    ]
    
    for query in low_confidence_queries:
        print(f"\n📝 Query: '{query}'")
        results = retriever.retrieve_with_scores(query, k=5, use_expansion=True)
        
        if results:
            scores = [r['similarity_score'] for r in results]
            max_score = max(scores)
            print(f"   Max similarity score: {max_score:.3f}")
            
            if max_score < 0.3:
                print(f"   Result: ✅ Correctly identified as low confidence")
            else:
                print(f"   Result: ⚠️ Unexpectedly high confidence for nonsense query")
        else:
            print(f"   Result: ✅ No results returned (good)")

def test_query_expansion_fix():
    """Demonstrate how query expansion fixes retrieval failures"""
    print("\n" + "="*60)
    print("TEST 4: Query Expansion - Failure Case Fix Demonstration")
    print("="*60)
    
    vector_store = GhanaVectorStore()
    vector_store.load_index()
    embedder = GhanaEmbeddingPipeline()
    retriever = GhanaRetrievalSystem(vector_store, embedder)
    
    # This query fails without expansion
    failure_query = "how much money for roads"
    
    print(f"\n📝 Original Query: '{failure_query}'")
    print("\n🔧 PROBLEM: Informal phrasing 'how much money for roads' doesn't match 'road infrastructure budget' in documents")
    
    # Without fix
    print("\n❌ WITHOUT QUERY EXPANSION:")
    no_expand_results = retriever.retrieve_with_scores(failure_query, k=3, use_expansion=False)
    if no_expand_results:
        for r in no_expand_results:
            print(f"   Score: {r['similarity_score']:.3f} | {r['source']}")
    else:
        print("   No results found")
    
    # With fix
    print("\n✅ WITH QUERY EXPANSION:")
    print(f"   Expanded queries: {retriever.expand_query(failure_query)[:3]}")
    with_expand_results = retriever.retrieve_with_scores(failure_query, k=3, use_expansion=True)
    if with_expand_results:
        for r in with_expand_results:
            print(f"   Score: {r['similarity_score']:.3f} | {r['source']}")
    else:
        print("   Still no results")
    
    print("\n📌 FIX APPLIED: Added synonyms 'roads', 'infrastructure', 'budget' to query expansion")

if __name__ == "__main__":
    print("\n🔍 FAILURE CASE TESTS")
    print("="*60)
    
    test_ambiguous_queries()
    test_out_of_scope_queries()
    test_low_confidence_queries()
    test_query_expansion_fix()
    
    print("\n" + "="*60)
    print("✅ All failure case tests complete!")
    print("\nSummary of fixes implemented:")
    print("  1. Query expansion for ambiguous/informal queries")
    print("  2. Out-of-scope detection with polite refusal")
    print("  3. Low confidence threshold (0.25) for source display")
    print("  4. Synonym expansion for Ghana-specific terms (NPP, NDC, GHS, etc.)")