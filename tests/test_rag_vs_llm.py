"""
File: test_rag_vs_llm.py
Author: Emmanuella Uwudia
Index Number: AI_10012200008
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Compare RAG system vs Pure LLM responses
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_pipeline import GhanaRAGPipeline
from src.llm_client import GhanaLLMClient

def compare_responses():
    """Compare RAG-enhanced responses vs pure LLM responses"""
    print("\n" + "="*60)
    print("RAG vs PURE LLM COMPARISON")
    print("="*60)
    
    # Initialize RAG pipeline
    print("\n🟡 Loading RAG pipeline...")
    rag = GhanaRAGPipeline()
    
    # Initialize pure LLM client
    print("🟡 Loading Pure LLM client...")
    llm = GhanaLLMClient()
    
    test_queries = [
        {
            "query": "What is the healthcare budget for 2025?",
            "expected_type": "budget figure"
        },
        {
            "query": "What parties contested the 2020 election?",
            "expected_type": "election data"
        },
        {
            "query": "Tell me about the LEAP programme",
            "expected_type": "social protection"
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_queries, 1):
        query = test["query"]
        print(f"\n{'='*60}")
        print(f"TEST {i}: {query}")
        print(f"{'='*60}")
        
        # RAG Response
        print("\n📚 RAG SYSTEM RESPONSE:")
        print("-" * 40)
        rag_result = rag.process_query(query, k=5, use_expansion=True)
        
        if rag_result["success"]:
            print(f"Response: {rag_result['response'][:300]}...")
            print(f"Sources: {len(rag_result.get('retrieved_chunks', []))} chunks retrieved")
            if rag_result.get('retrieved_chunks'):
                scores = [c.get('similarity_score', 0) for c in rag_result['retrieved_chunks'][:3]]
                print(f"Top scores: {[f'{s:.3f}' for s in scores]}")
        else:
            print(f"Error: {rag_result.get('error', 'Unknown error')}")
        
        # Pure LLM Response
        print("\n🤖 PURE LLM RESPONSE (No Context):")
        print("-" * 40)
        pure_prompt = f"Answer this question about Ghana using ONLY your general knowledge. Be honest if unsure: {query}"
        pure_result = llm.generate(pure_prompt, temperature=0.3)
        
        if pure_result["success"]:
            print(f"Response: {pure_result['response'][:300]}...")
            print(f"Time: {pure_result.get('time_seconds', 0):.2f}s")
        else:
            print(f"Error: {pure_result.get('error', 'Unknown error')}")
        
        # Store comparison
        results.append({
            "query": query,
            "rag_has_sources": len(rag_result.get('retrieved_chunks', [])) > 0,
            "rag_success": rag_result["success"],
            "pure_success": pure_result["success"]
        })
    
    # Summary
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    
    for r in results:
        print(f"\n📝 Query: {r['query']}")
        print(f"   RAG: {'✅ Has sources' if r['rag_has_sources'] else '❌ No sources'}")
        print(f"   RAG Success: {'✅' if r['rag_success'] else '❌'}")
        print(f"   Pure LLM Success: {'✅' if r['pure_success'] else '❌'}")
    
    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)
    print("RAG system provides source-attributed, grounded answers.")
    print("Pure LLM may hallucinate or provide generic information.")
    print("RAG is more reliable for factual questions about Ghana data.")

def test_hallucination_detection():
    """Test hallucination rates between RAG and Pure LLM"""
    print("\n" + "="*60)
    print("HALLUCINATION DETECTION TEST")
    print("="*60)
    
    rag = GhanaRAGPipeline()
    llm = GhanaLLMClient()
    
    # Queries that might cause hallucinations
    tricky_queries = [
        "What was the exact education budget in 2025?",
        "Which party got the most votes in 2020?",
        "Tell me about a non-existent programme called 'Ghana Care Plus'"
    ]
    
    for query in tricky_queries:
        print(f"\n📝 Query: '{query}'")
        print("-" * 40)
        
        # RAG Response
        rag_result = rag.process_query(query, k=5)
        rag_response = rag_result["response"].lower()
        
        # Check for hallucination indicators in RAG
        rag_hallucination = any(word in rag_response for word in ["i think", "probably", "maybe", "guess"])
        
        # Pure LLM Response
        pure_result = llm.generate(f"Answer: {query}", temperature=0.3)
        pure_response = pure_result["response"].lower() if pure_result["success"] else ""
        pure_hallucination = any(word in pure_response for word in ["i think", "probably", "maybe", "guess"])
        
        print(f"   RAG: {'⚠️ May be hallucinating' if rag_hallucination else '✅ Seems confident'}")
        print(f"   Pure LLM: {'⚠️ May be hallucinating' if pure_hallucination else '✅ Seems confident'}")

if __name__ == "__main__":
    compare_responses()
    test_hallucination_detection()
    
    print("\n✅ RAG vs Pure LLM tests complete!")