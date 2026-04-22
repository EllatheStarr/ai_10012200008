"""
File: rag_pipeline.py
Author: Emmanuella Uwudia
Index Number: AI_10012200008
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Complete RAG pipeline with conversation memory (Innovation Feature)
"""

import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from src.embeddings import GhanaEmbeddingPipeline
from src.vector_store import GhanaVectorStore
from src.retrieval import GhanaRetrievalSystem
from src.prompt_builder import GhanaPromptBuilder
from src.llm_client import GhanaLLMClient

class GhanaRAGPipeline:
    """
    Complete RAG pipeline for Ghana data with CONVERSATION MEMORY
    Innovation Feature: Remembers chat history for contextual follow-up questions
    """
    
    def __init__(self, max_history: int = 10):
        print("🇬🇭 Initializing GH RAG Pipeline with Conversation Memory...")
        
        # Load components
        self.vector_store = GhanaVectorStore()
        self.vector_store.load_index()
        
        self.embedder = GhanaEmbeddingPipeline()
        self.retriever = GhanaRetrievalSystem(self.vector_store, self.embedder)
        self.prompt_builder = GhanaPromptBuilder()
        self.llm = GhanaLLMClient()
        
        # INNOVATION: Conversation memory
        self.conversation_history = []  # Stores (user_msg, assistant_msg)
        self.max_history = max_history  # Keep last N exchanges
        self.use_memory = True  # Feature toggle
        
        self.pipeline_logs = []
        print("✅ Pipeline ready with Conversation Memory!")
        
    def get_conversation_context(self) -> str:
        """
        INNOVATION FEATURE: Build context from recent conversation history
        Returns formatted string of previous exchanges
        """
        if not self.use_memory or not self.conversation_history:
            return ""
        
        context_parts = ["Previous conversation for context:"]
        for i, (user_msg, assistant_msg) in enumerate(self.conversation_history[-self.max_history:]):
            context_parts.append(f"[Previous Q{i+1}] User: {user_msg}")
            context_parts.append(f"[Previous A{i+1}] Assistant: {assistant_msg[:200]}...")
        
        context_parts.append("\nUse the conversation history above to understand follow-up questions.")
        return "\n".join(context_parts)
    
    def build_contextual_query(self, query: str) -> str:
        """
        INNOVATION FEATURE: Enhance query with conversation context
        Helps resolve pronouns like "it", "that", "they"
        """
        if not self.use_memory or not self.conversation_history:
            return query
        
        # Get last exchange for context
        last_user, last_assistant = self.conversation_history[-1] if self.conversation_history else ("", "")
        
        # Check if query contains pronouns that need resolution
        pronouns = ["it", "that", "this", "those", "these", "they", "them", "there"]
        needs_context = any(pronoun in query.lower().split() for pronoun in pronouns)
        
        if needs_context and last_assistant:
            # Add context from last response
            enhanced_query = f"Context from previous answer: {last_assistant[:150]}...\n\nFollow-up question: {query}"
            return enhanced_query
        
        return query
    
    def process_query(self, query: str, k: int = 5, use_expansion: bool = True) -> Dict[str, Any]:
        """
        Process a user query through the full RAG pipeline
        WITH CONVERSATION MEMORY for follow-up questions
        """
        
        start_time = time.time()
        
        # Create log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "stages": {},
            "conversation_memory_used": len(self.conversation_history) > 0
        }
        
        # INNOVATION: Enhance query with conversation context
        contextual_query = self.build_contextual_query(query)
        if contextual_query != query:
            log_entry["enhanced_query"] = contextual_query
            print(f"🔄 Enhanced query with conversation context")
        
        # Stage 1: Retrieval
        print(f"\n🔍 Stage 1: Retrieving relevant chunks for: {query}")
        retrieval_start = time.time()
        retrieved_chunks = self.retriever.retrieve_with_scores(contextual_query, k=k, use_expansion=use_expansion)
        retrieval_time = time.time() - retrieval_start
        
        log_entry["stages"]["retrieval"] = {
            "time_seconds": retrieval_time,
            "num_chunks": len(retrieved_chunks),
            "chunks": [
                {
                    "chunk_id": c["chunk_id"],
                    "score": c.get("similarity_score", 0),
                    "source": c["source"],
                    "text_preview": c["text"][:200]
                }
                for c in retrieved_chunks
            ]
        }
        
        # INNOVATION: Add conversation context to prompt
        conversation_context = self.get_conversation_context()
        
        # Stage 2: Build prompt with context
        print(f"📝 Stage 2: Building prompt with {len(retrieved_chunks)} chunks")
        prompt_start = time.time()
        prompt, prompt_meta = self.prompt_builder.build_prompt(
            query, 
            retrieved_chunks,
            conversation_context=conversation_context  # Pass conversation history
        )
        prompt_time = time.time() - prompt_start
        
        log_entry["stages"]["prompt_building"] = {
            "time_seconds": prompt_time,
            "context_chunks": prompt_meta["num_chunks_in_context"],
            "prompt_length": prompt_meta["prompt_length"],
            "conversation_context_included": len(conversation_context) > 0,
            "prompt_preview": prompt[:500]
        }
        
        # Stage 3: LLM Generation
        print(f"🤖 Stage 3: Generating response with LLM")
        llm_start = time.time()
        llm_response = self.llm.generate(prompt, temperature=0.3, max_tokens=500)
        llm_time = time.time() - llm_start
        
        log_entry["stages"]["llm_generation"] = {
            "time_seconds": llm_time,
            "success": llm_response["success"],
            "response_length": len(llm_response.get("response", "")),
            "model": llm_response.get("model"),
            "tokens_used": llm_response.get("tokens_used")
        }
        
        # Total time
        total_time = time.time() - start_time
        log_entry["total_time_seconds"] = total_time
        
        # Build final result
        result = {
            "success": llm_response["success"],
            "query": query,
            "response": llm_response.get("response", "Error generating response"),
            "error": llm_response.get("error"),
            "retrieved_chunks": retrieved_chunks,
            "similarity_scores": [c.get("similarity_score", 0) for c in retrieved_chunks],
            "prompt": prompt,
            "conversation_memory_used": len(self.conversation_history) > 0,
            "metadata": {
                "retrieval_time": retrieval_time,
                "prompt_time": prompt_time,
                "llm_time": llm_time,
                "total_time": total_time,
                "num_chunks_retrieved": len(retrieved_chunks),
                "use_query_expansion": use_expansion,
                "conversation_history_length": len(self.conversation_history)
            }
        }
        
        # INNOVATION: Store in conversation memory
        self.conversation_history.append((query, result["response"]))
        
        # Keep only last max_history exchanges
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
        
        log_entry["result_summary"] = {
            "success": result["success"],
            "response_preview": result["response"][:200],
            "num_chunks": len(retrieved_chunks),
            "conversation_history_length": len(self.conversation_history)
        }
        
        # Save log
        self.pipeline_logs.append(log_entry)
        
        # Print summary
        print(f"\n✅ Pipeline complete in {total_time:.2f}s")
        print(f"   • Retrieved: {len(retrieved_chunks)} chunks")
        print(f"   • Response: {len(result['response'])} chars")
        print(f"   • Conversation memory: {len(self.conversation_history)} exchanges stored")
        
        self.save_logs()
        return result
    
    def clear_conversation_memory(self):
        """INNOVATION: Clear conversation history for new topic"""
        self.conversation_history = []
        print("🧹 Conversation memory cleared!")
    
    def get_conversation_summary(self) -> Dict:
        """INNOVATION: Get summary of current conversation"""
        return {
            "total_exchanges": len(self.conversation_history),
            "max_capacity": self.max_history,
            "memory_enabled": self.use_memory,
            "recent_topics": [msg[0][:50] for msg in self.conversation_history[-3:]]
        }
    
    def save_logs(self, output_path: str = "logs/pipeline_logs.json"):
        """Save all pipeline logs"""
        import os
        os.makedirs("logs", exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(self.pipeline_logs, f, indent=2)
        
        print(f"✅ Saved {len(self.pipeline_logs)} pipeline logs to {output_path}")
    
    def get_log_summary(self) -> Dict:
        """Get summary statistics from logs"""
        if not self.pipeline_logs:
            return {"error": "No logs available"}
        
        total_queries = len(self.pipeline_logs)
        avg_retrieval_time = sum(l["stages"]["retrieval"]["time_seconds"] for l in self.pipeline_logs) / total_queries
        avg_llm_time = sum(l["stages"]["llm_generation"]["time_seconds"] for l in self.pipeline_logs) / total_queries
        avg_total_time = sum(l["total_time_seconds"] for l in self.pipeline_logs) / total_queries
        
        return {
            "total_queries": total_queries,
            "average_retrieval_time": avg_retrieval_time,
            "average_llm_time": avg_llm_time,
            "average_total_time": avg_total_time,
            "success_rate": sum(1 for l in self.pipeline_logs if l["result_summary"]["success"]) / total_queries,
            "conversation_memory_usage": sum(1 for l in self.pipeline_logs if l.get("conversation_memory_used", False)) / total_queries
        }


if __name__ == "__main__":
    # Initialize pipeline
    pipeline = GhanaRAGPipeline()
    
    # Test conversation flow
    print("\n" + "="*60)
    print("TESTING CONVERSATION MEMORY")
    print("="*60)
    
    # First question
    result1 = pipeline.process_query("What is the healthcare budget for 2025?")
    print(f"\nQ1 Response: {result1['response'][:150]}...")
    
    # Follow-up question (should understand "it" refers to healthcare)
    result2 = pipeline.process_query("How does it compare to education?")
    print(f"\nQ2 Response: {result2['response'][:150]}...")
    
    # Get conversation summary
    summary = pipeline.get_conversation_summary()
    print(f"\n📊 Conversation Summary: {json.dumps(summary, indent=2)}")
    
    # Save logs
    pipeline.save_logs()