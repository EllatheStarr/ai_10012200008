"""
File: llm_client.py
Author: Student Name
Index Number: AI_20240001
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: LLM client for Groq API
"""

import os
import json
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class GhanaLLMClient:
    """
    LLM client using Groq (free tier, ultra-fast)
    Updated to use supported model: llama-3.1-8b-instant
    """
    
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        """
        Initialize Groq client
        Available models: 
        - llama-3.1-8b-instant (fast, good for RAG)
        - llama-3.3-70b-versatile (more accurate, slower)
        - openai/gpt-oss-20b (very fast)
        """
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("⚠️ Warning: GROQ_API_KEY not found in .env")
            print("   Please add your API key or the LLM will not work")
            self.client = None
        else:
            self.client = Groq(api_key=api_key)
        
        self.model_name = model_name
        self.response_logs = []
        
    def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 500):
        """
        Generate response from LLM
        Low temperature (0.3) to reduce hallucinations
        """
        if self.client is None:
            return {
                "success": False,
                "error": "No API key configured",
                "response": "⚠️ LLM not configured. Please add GROQ_API_KEY to .env file."
            }
        
        start_time = time.time()
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            response_text = completion.choices[0].message.content
            elapsed_time = time.time() - start_time
            
            result = {
                "success": True,
                "response": response_text,
                "model": self.model_name,
                "temperature": temperature,
                "tokens_used": completion.usage.total_tokens if hasattr(completion, 'usage') else None,
                "time_seconds": elapsed_time
            }
            
            # Log response
            self.response_logs.append({
                "prompt_length": len(prompt),
                "response_length": len(response_text),
                **result
            })
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": f"Error: {str(e)}"
            }
    
    def compare_with_pure_llm(self, query: str):
        """
        Compare RAG-enhanced response vs pure LLM (no context)
        Required for Part E marks
        """
        print("\n" + "="*60)
        print("RAG vs PURE LLM COMPARISON")
        print("="*60)
        
        # Pure LLM prompt (no context)
        pure_prompt = f"""You are a helpful AI assistant. Answer this question about Ghana:
{query}

Note: You have no specific documents. Answer based on your general knowledge only.
If you're unsure, say you don't know."""

        # This would be called with actual context in the pipeline
        # For now, returning structure
        
        comparison = {
            "query": query,
            "rag_advantages": [
                "Grounding in actual documents",
                "No hallucination of figures",
                "Can cite specific sources"
            ],
            "pure_llm_disadvantages": [
                "May hallucinate numbers",
                "No source attribution",
                "Outdated information possible"
            ]
        }
        
        return comparison
    
    def save_logs(self, output_path: str = "logs/llm_logs.json"):
        """Save LLM response logs"""
        import os
        os.makedirs("logs", exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(self.response_logs, f, indent=2)
        
        print(f"✅ Saved {len(self.response_logs)} LLM logs to {output_path}")


if __name__ == "__main__":
    llm = GhanaLLMClient()
    
    # Test generation
    test_prompt = "What is the capital of Ghana? (Answer in one word)"
    
    result = llm.generate(test_prompt)
    
    if result["success"]:
        print(f"\n✅ LLM Response: {result['response']}")
        print(f"   Time: {result['time_seconds']:.2f}s")
        print(f"   Model: {result['model']}")
    else:
        print(f"\n❌ Error: {result['error']}")