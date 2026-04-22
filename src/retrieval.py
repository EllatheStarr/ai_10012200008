"""
File: retrieval.py
Author: Emmanuella Uwudia
Index Number: AI_10012200008
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Custom retrieval with top-k, similarity scoring, and query expansion
"""

import numpy as np
import json
import re
from typing import List, Dict, Tuple, Optional
from src.embeddings import GhanaEmbeddingPipeline
from src.vector_store import GhanaVectorStore

class GhanaRetrievalSystem:
    """
    Custom retrieval system for Ghana data
    Features: Top-k retrieval, similarity scoring, query expansion
    """
    
    def __init__(self, vector_store: GhanaVectorStore, embedder: GhanaEmbeddingPipeline):
        self.vector_store = vector_store
        self.embedder = embedder
        self.retrieval_logs = []
        
    def expand_query(self, query: str) -> List[str]:
        """
        Query expansion using Ghana-specific synonyms and variations
        """
        expansions = [query]  # Original query first
        
        # Ghana election synonyms - ENHANCED for winner/presidential queries
        election_synonyms = {
            "election": ["elections", "vote", "voting", "polls", "ballot", "presidential election", "general election"],
            "won": ["won", "winner", "win", "victory", "defeated", "beat", "winning party", "election winner"],
            "win": ["won", "winner", "victory", "defeated", "beat", "winning party"],
            "winner": ["won", "win", "victory", "winning party", "election winner"],
            "presidential": ["president", "presidency", "presidential election", "presidential race"],
            "party": ["political party", "candidate", "faction", "winning party", "party name"],
            "region": ["constituency", "district", "area"],
            "npp": ["new patriotic party", "npp party", "akufo-addo"],
            "ndc": ["national democratic congress", "ndc party", "mahama"],
            "2020": ["2020 election", "2020 presidential", "election 2020", "2020 results", "2020 polls"],
            "turnout": ["voter turnout", "participation", "voting percentage"],
            "results": ["outcome", "figures", "statistics", "data", "election results"],
            "who": ["which party", "what party", "election winner"]
        }
        
        # Budget synonyms
        budget_synonyms = {
            "budget": ["allocation", "spending", "expenditure", "fiscal", "financial"],
            "ghs": ["cedis", "ghana cedis", "money", "funds"],
            "healthcare": ["health", "medical", "hospitals", "nhis"],
            "education": ["schools", "teaching", "students", "free shs"],
            "infrastructure": ["roads", "bridges", "construction", "development"],
            "economy": ["gdp", "growth", "economic", "finance"],
            "tax": ["taxes", "revenue", "levy", "duty"],
            "debt": ["borrowing", "loan", "liability", "deficit"]
        }
        
        # Combine all synonyms
        all_synonyms = {**election_synonyms, **budget_synonyms}
        
        # Expand query with synonyms
        words = query.lower().split()
        for word in words:
            # Also check for phrases (e.g., "who won" -> "which party won")
            if word in all_synonyms:
                for syn in all_synonyms[word][:2]:  # Limit to 2 synonyms per word
                    expanded = query.replace(word, syn)
                    if expanded not in expansions:
                        expansions.append(expanded)
        
        # Special handling for "who won" type queries
        if re.search(r'who won', query.lower()):
            expansions.append("which party won the presidential election")
            expansions.append("election winner 2020")
            expansions.append("presidential election results winner party")
        
        # Special handling for "2020 election" queries
        if '2020' in query.lower() and ('election' in query.lower() or 'won' in query.lower()):
            expansions.append("2020 presidential election results winner")
            expansions.append("which party won the 2020 presidential election in Ghana")
        
        # Also add shorter version (remove stop words)
        stop_words = {"what", "is", "are", "the", "a", "an", "of", "to", "for", "in", "on", "at", "which", "who"}
        short_query = " ".join([w for w in words if w not in stop_words])
        if short_query and short_query != query.lower() and len(short_query.split()) >= 2:
            expansions.append(short_query)
        
        # Remove duplicates and limit
        expansions = list(dict.fromkeys(expansions))
        return expansions[:5]  # Limit to 5 expansions
    
    def retrieve_with_scores(self, query: str, k: int = 5, use_expansion: bool = True) -> List[Dict]:
        """
        Retrieve top-k chunks with similarity scores
        Optional: Use query expansion for better recall
        BOOST: Winner summary chunks get 30% score boost
        """
        log_entry = {
            "query": query,
            "use_expansion": use_expansion,
            "k": k,
            "timestamp": str(np.datetime64('now')),
            "results": []
        }
        
        if use_expansion:
            expanded_queries = self.expand_query(query)
            log_entry["expanded_queries"] = expanded_queries
            
            # Get embeddings for all expanded queries - get more results for better dedup
            all_results = []
            for expanded in expanded_queries[:3]:
                expanded_embedding = self.embedder.embed_query(expanded)
                results = self.vector_store.search(expanded_embedding, k=k * 2)
                all_results.extend(results)
            
            # Deduplicate by chunk_id and keep highest score
            seen = {}
            for result in all_results:
                chunk_id = result["chunk_id"]
                score = result["similarity_score"]
                
                # BOOST: Give 30% higher score to winner summary chunks
                if "summary" in chunk_id or "winner" in chunk_id or "region_summary" in chunk_id:
                    score = score * 1.3
                    result["similarity_score"] = score
                    result["boosted"] = True
                
                if chunk_id not in seen or score > seen[chunk_id]["similarity_score"]:
                    seen[chunk_id] = result
            
            # Sort by boosted score and take top-k
            final_results = sorted(seen.values(), key=lambda x: x["similarity_score"], reverse=True)[:k]
        else:
            # Standard retrieval without expansion
            query_embedding = self.embedder.embed_query(query)
            final_results = self.vector_store.search(query_embedding, k=k)
        
        # Add scores to log
        for result in final_results:
            log_entry["results"].append({
                "chunk_id": result["chunk_id"],
                "similarity_score": result["similarity_score"],
                "source": result["source"],
                "text_preview": result["text"][:200]
            })
        
        self.retrieval_logs.append(log_entry)
        
        return final_results
    
    def show_failure_cases(self) -> Dict:
        """
        Demonstrate retrieval failure cases and fixes
        Required for Part B marks
        """
        print("\n" + "="*60)
        print("FAILURE CASE DEMONSTRATION")
        print("="*60)
        
        failure_queries = [
            "What was the voter turnout in 2024?",  # Data might not have 2024
            "Tell me about the opposition party",  # Ambiguous
            "How much money for roads?"  # Informal phrasing
        ]
        
        results = {}
        
        for query in failure_queries:
            print(f"\n📝 Query: '{query}'")
            print("-" * 40)
            
            # Without fix (no expansion)
            no_expansion_results = self.retrieve_with_scores(query, k=3, use_expansion=False)
            print(f"❌ Without fix (no expansion): {len(no_expansion_results)} results")
            for r in no_expansion_results:
                print(f"   Score: {r['similarity_score']:.3f} | Source: {r['source']}")
            
            # With fix (query expansion)
            with_expansion_results = self.retrieve_with_scores(query, k=3, use_expansion=True)
            print(f"✅ With fix (query expansion): {len(with_expansion_results)} results")
            for r in with_expansion_results:
                print(f"   Score: {r['similarity_score']:.3f} | Source: {r['source']}")
            
            results[query] = {
                "without_fix": [{"score": r["similarity_score"], "source": r["source"]} for r in no_expansion_results],
                "with_fix": [{"score": r["similarity_score"], "source": r["source"]} for r in with_expansion_results],
                "improvement": "Significant" if len(with_expansion_results) > len(no_expansion_results) else "Minor"
            }
        
        return results
    
    def save_logs(self, output_path: str = "logs/retrieval_logs.json"):
        """Save retrieval logs for analysis"""
        import os
        os.makedirs("logs", exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(self.retrieval_logs, f, indent=2)
        
        print(f"✅ Saved {len(self.retrieval_logs)} retrieval logs to {output_path}")


if __name__ == "__main__":
    # Load vector store and embedder
    vector_store = GhanaVectorStore()
    vector_store.load_index()
    
    embedder = GhanaEmbeddingPipeline()
    
    # Initialize retrieval system
    retriever = GhanaRetrievalSystem(vector_store, embedder)
    
    # Test retrieval for winner query
    test_query = "Which party won the 2020 presidential election?"
    
    print(f"\n🔍 Testing query: '{test_query}'")
    print("-" * 50)
    
    # With query expansion
    results = retriever.retrieve_with_scores(test_query, k=5, use_expansion=True)
    print("\n📊 Results WITH query expansion and winner boost:")
    for r in results:
        boosted = "★ BOOSTED" if r.get("boosted", False) else ""
        print(f"  [Rank {r['rank']}] Score: {r['similarity_score']:.4f} | {r['source']} {boosted}")
        if 'summary' in r.get('chunk_id', '') or 'winner' in r.get('chunk_id', ''):
            print(f"    → WINNER CHUNK: {r['text'][:150]}...")
    
    # Show failure cases
    failures = retriever.show_failure_cases()
    
    # Save logs
    retriever.save_logs()