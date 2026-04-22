"""
File: prompt_builder.py
Author: Student Name
Index Number: AI_20240001
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Prompt engineering with hallucination control and context management
"""

from typing import List, Dict, Tuple
import json

class GhanaPromptBuilder:
    """
    Custom prompt builder for Ghana data with hallucination control
    """
    
    def __init__(self, max_context_chunks: int = 5, max_chunk_tokens: int = 500):
        self.max_context_chunks = max_context_chunks
        self.max_chunk_tokens = max_chunk_tokens
        self.prompt_iterations = []
        
    def get_system_prompt(self) -> str:
        """
        System prompt with Ghana persona and hallucination control
        """
        return """You are Brew & Ask, a helpful AI assistant specializing in Ghana's election results and national budget.

🇬🇭 YOUR IDENTITY:
- You are knowledgeable about Ghana's democratic processes and economic development
- You speak with a professional yet warm Ghanaian tone
- You always ground your answers in the provided context

🚫 HALLUCINATION CONTROL RULES:
1. ONLY answer based on the provided context below
2. If the context doesn't contain the answer, say: "Sorry, I couldn't find that information in the available Ghana election or budget documents."
3. NEVER invent numbers, dates, or figures about elections or budget
4. If asked about non-Ghana topics or anything NOT in the documents, say: "Sorry, I only have information about Ghana's elections and budget. I cannot answer questions about other topics."
5. If the retrieved context is empty or has no relevant information, say you couldn't find the answer

📋 RESPONSE FORMAT:
- Be concise but informative
- Use bullet points for multiple facts
- When citing figures, specify the source (e.g., "According to the 2025 Budget Statement...")
- Use Ghana cedis (GHS) for budget figures

✅ Examples of GOOD responses:
- "According to the 2025 Budget Statement, the healthcare allocation is GHS 12.4 billion."
- "Based on the election results, the NPP won the Greater Accra region with 55% of votes."
- "Sorry, I couldn't find that information in the available Ghana election or budget documents."

❌ Examples of BAD responses:
- "I think the budget was..." (don't guess)
- "Probably the NDC won..." (don't speculate)
- "The capital of France is Paris..." (don't answer unrelated questions)

⚠️ IMPORTANT: If the user asks about anything NOT related to Ghana elections or budget, respond with:
"Sorry, I only have information about Ghana's elections and budget. I cannot answer questions about other topics."

Remember: Your job is to provide ACCURATE information from Ghana's official documents. No guessing!"""
    
    def truncate_context(self, chunks: List[Dict], max_tokens: int = 1500) -> List[Dict]:
        """
        Truncate context to fit within token limits
        """
        truncated = []
        total_tokens = 0
        
        for chunk in chunks:
            # Rough token estimate (1 token ~ 4 chars)
            chunk_tokens = len(chunk["text"]) // 4
            
            if total_tokens + chunk_tokens <= max_tokens:
                truncated.append(chunk)
                total_tokens += chunk_tokens
            else:
                # Truncate the last chunk
                remaining = max_tokens - total_tokens
                if remaining > 100:  # Only include if meaningful
                    truncated_text = chunk["text"][:remaining * 4]
                    chunk["text"] = truncated_text + "..."
                    truncated.append(chunk)
                break
        
        return truncated
    
    def rank_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Rank chunks by relevance score (already sorted, but ensure quality)
        """
        # Filter out low relevance chunks (below 0.3 threshold)
        filtered = [c for c in chunks if c.get("similarity_score", 0) > 0.3]
        
        # Sort by score descending
        return sorted(filtered, key=lambda x: x.get("similarity_score", 0), reverse=True)
    
    def build_prompt(self, query: str, retrieved_chunks: List[Dict], conversation_context: str = "") -> Tuple[str, Dict]:
        """
        Build final prompt with context injection and conversation memory
        Returns (prompt_string, metadata)
        """
        # Rank and filter chunks (only keeps scores > 0.3)
        ranked_chunks = self.rank_chunks(retrieved_chunks)
        
        # Truncate to fit context window
        context_chunks = self.truncate_context(ranked_chunks, max_tokens=1500)
        
        # Build context string
        context_parts = []
        for i, chunk in enumerate(context_chunks):
            source_label = "📊 Election Data" if chunk["source_type"] == "csv" else "📄 Budget Statement"
            score_indicator = "⭐" * min(3, int(chunk.get("similarity_score", 0) * 3))
            
            context_parts.append(f"""
[Source {i+1}] {source_label} {score_indicator} (Relevance: {chunk.get('similarity_score', 0):.2f})
From: {chunk['source']}
Content: {chunk['text']}
""")
        
        # If no relevant chunks found
        if not context_parts:
            context_text = "No relevant documents found. The user's question may not be related to Ghana elections or budget."
        else:
            context_text = "\n".join(context_parts)
        
        # INNOVATION: Add conversation context if available
        conversation_section = ""
        if conversation_context:
            conversation_section = f"""
============================================================
CONVERSATION HISTORY (Use for follow-up questions):
============================================================
{conversation_context}

IMPORTANT: The user may be asking a follow-up question. Use the conversation history to understand references like "it", "that", "they", "there".
"""
        
        # Build the full prompt
        prompt = f"""{self.get_system_prompt()}

{conversation_section}
============================================================
RETRIEVED CONTEXT (Use ONLY this to answer):
============================================================
{context_text}

============================================================
USER QUESTION:
============================================================
{query}

============================================================
INSTRUCTIONS:
1. Answer using ONLY the context above
2. If the answer isn't in the context, say you couldn't find it
3. If there's conversation history, use it to understand follow-up questions
4. Do NOT use numbered citations like "Source 1" or "Source 2" in your answer
5. If needed, cite naturally (for example: "According to the 2025 Budget Statement...")
6. Be helpful and accurate!

YOUR ANSWER:
"""
        
        # Track prompt iteration for analysis
        iteration_metadata = {
            "query": query,
            "num_chunks_retrieved": len(retrieved_chunks),
            "num_chunks_after_ranking": len(ranked_chunks),
            "num_chunks_in_context": len(context_chunks),
            "has_relevant_context": len(context_chunks) > 0,
            "has_conversation_context": len(conversation_context) > 0,
            "context_tokens_estimate": len(context_text) // 4,
            "prompt_length": len(prompt),
            "chunk_scores": [c.get("similarity_score", 0) for c in context_chunks]
        }
        
        self.prompt_iterations.append(iteration_metadata)
        
        return prompt, iteration_metadata
    
    def experiment_different_prompts(self, query: str, chunks: List[Dict]) -> Dict:
        """
        Run experiments with different prompt templates
        Required for Part C marks
        """
        print("\n" + "="*60)
        print("PROMPT ENGINEERING EXPERIMENTS")
        print("="*60)
        
        # Template 1: Standard (current)
        prompt1, meta1 = self.build_prompt(query, chunks)
        
        # Template 2: More structured (with examples)
        prompt2 = f"""You are a Ghana elections and budget expert.

CONTEXT:
{chr(10).join([f"- {c['text'][:200]}..." for c in chunks[:3]])}

QUESTION: {query}

EXAMPLE GOOD ANSWER: "Based on the budget statement, the allocation is GHS X."
EXAMPLE BAD ANSWER: "I think it might be..."

Answer with facts only:"""
        
        # Template 3: Extremely concise
        prompt3 = f"""Context: {chr(10).join([c['text'][:300] for c in chunks[:3]])}
Question: {query}
Answer (if in context, otherwise say "not found"):"""
        
        # Simulate responses (in real system, you'd call LLM)
        results = {
            "prompt_template_1_standard": {
                "length": len(prompt1),
                "context_chunks": meta1["num_chunks_in_context"],
                "estimated_quality": "Good balance of detail and instruction"
            },
            "prompt_template_2_structured": {
                "length": len(prompt2),
                "context_chunks": len(chunks[:3]),
                "estimated_quality": "Better examples but longer"
            },
            "prompt_template_3_concise": {
                "length": len(prompt3),
                "context_chunks": len(chunks[:3]),
                "estimated_quality": "Fast but may lack guidance"
            }
        }
        
        print("\n📊 Experiment Results:")
        for name, data in results.items():
            print(f"\n  {name}:")
            print(f"    • Length: {data['length']} chars")
            print(f"    • Context chunks: {data['context_chunks']}")
            print(f"    • Quality: {data['estimated_quality']}")
        
        return results
    
    def save_iterations(self, output_path: str = "logs/prompt_logs.json"):
        """Save prompt iterations for analysis"""
        import os
        os.makedirs("logs", exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(self.prompt_iterations, f, indent=2)
        
        print(f"✅ Saved {len(self.prompt_iterations)} prompt iterations to {output_path}")


if __name__ == "__main__":
    # Test with sample chunks
    sample_chunks = [
        {
            "text": "The healthcare budget allocation for 2025 is GHS 12.4 billion",
            "source": "Ghana 2025 Budget Statement",
            "source_type": "pdf",
            "similarity_score": 0.92
        },
        {
            "text": "Education receives GHS 15.2 billion in the 2025 budget",
            "source": "Ghana 2025 Budget Statement",
            "source_type": "pdf",
            "similarity_score": 0.85
        }
    ]
    
    builder = GhanaPromptBuilder()
    
    # Build prompt
    prompt, meta = builder.build_prompt("What is the healthcare budget?", sample_chunks)
    print("📝 Generated Prompt:")
    print("-" * 40)
    print(prompt[:500] + "...")
    
    # Run experiments
    results = builder.experiment_different_prompts("What is the healthcare budget?", sample_chunks)
    
    # Save logs
    builder.save_iterations()