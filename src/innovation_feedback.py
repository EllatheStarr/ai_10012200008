"""
File: innovation_feedback.py
Author: Student Name
Index Number: AI_20240001
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Innovation feature - Feedback loop for retrieval improvement
"""

import json
from typing import Dict, List, Optional
from collections import defaultdict

class GhanaFeedbackLoop:
    """
    Innovation: Feedback loop for improving retrieval quality
    Users can rate responses, and the system learns which chunks are most useful
    """
    
    def __init__(self, feedback_file: str = "logs/feedback_data.json"):
        self.feedback_file = feedback_file
        self.feedback_data = self.load_feedback()
        self.chunk_effectiveness = defaultdict(lambda: {"positive": 0, "negative": 0, "score": 0.5})
        self._calculate_effectiveness()
    
    def load_feedback(self) -> List[Dict]:
        """Load past feedback data"""
        import os
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, "r") as f:
                return json.load(f)
        return []
    
    def save_feedback(self):
        """Save feedback data"""
        import os
        os.makedirs("logs", exist_ok=True)
        with open(self.feedback_file, "w") as f:
            json.dump(self.feedback_data, f, indent=2)
    
    def _calculate_effectiveness(self):
        """Calculate effectiveness scores for each chunk based on feedback"""
        for feedback in self.feedback_data:
            for chunk_id in feedback.get("chunks_used", []):
                if feedback.get("rating", 0) >= 4:  # Positive rating (4-5 stars)
                    self.chunk_effectiveness[chunk_id]["positive"] += 1
                elif feedback.get("rating", 0) <= 2:  # Negative rating (1-2 stars)
                    self.chunk_effectiveness[chunk_id]["negative"] += 1
        
        for chunk_id in self.chunk_effectiveness:
            data = self.chunk_effectiveness[chunk_id]
            total = data["positive"] + data["negative"]
            if total > 0:
                data["score"] = data["positive"] / total
            else:
                data["score"] = 0.5  # Neutral starting score
    
    def add_feedback(self, query: str, response: str, chunks_used: List[str], rating: int, user_comment: str = ""):
        """
        Add user feedback
        rating: 1-5 stars (5 = very helpful, 1 = not helpful)
        """
        feedback_entry = {
            "query": query,
            "response_preview": response[:200],
            "chunks_used": chunks_used,
            "rating": rating,
            "user_comment": user_comment,
            "timestamp": str(__import__('datetime').datetime.now())
        }
        
        self.feedback_data.append(feedback_entry)
        self.save_feedback()
        self._calculate_effectiveness()
        
        print(f"✅ Feedback recorded (Rating: {rating}/5)")
    
    def re_rank_with_feedback(self, chunks: List[Dict]) -> List[Dict]:
        """
        Re-rank retrieved chunks using feedback effectiveness scores
        """
        for chunk in chunks:
            chunk_id = chunk.get("chunk_id")
            effectiveness = self.chunk_effectiveness.get(chunk_id, {"score": 0.5})["score"]
            
            # Adjust similarity score based on feedback
            original_score = chunk.get("similarity_score", 0.5)
            adjusted_score = (original_score * 0.6) + (effectiveness * 0.4)  # 60% similarity, 40% feedback
            chunk["feedback_adjusted_score"] = adjusted_score
        
        # Re-rank by adjusted score
        chunks.sort(key=lambda x: x.get("feedback_adjusted_score", 0), reverse=True)
        
        return chunks
    
    def get_statistics(self) -> Dict:
        """Get feedback statistics"""
        if not self.feedback_data:
            return {"total_feedback": 0, "average_rating": 0}
        
        ratings = [f["rating"] for f in self.feedback_data]
        avg_rating = sum(ratings) / len(ratings)
        
        # Most effective chunks
        effective_chunks = sorted(
            [(k, v["score"]) for k, v in self.chunk_effectiveness.items() if v["positive"] + v["negative"] > 0],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "total_feedback": len(self.feedback_data),
            "average_rating": round(avg_rating, 2),
            "most_effective_chunks": effective_chunks,
            "total_positive": sum(1 for f in self.feedback_data if f["rating"] >= 4),
            "total_negative": sum(1 for f in self.feedback_data if f["rating"] <= 2)
        }


if __name__ == "__main__":
    feedback_loop = GhanaFeedbackLoop()
    
    # Simulate feedback
    feedback_loop.add_feedback(
        query="What is healthcare budget?",
        response="GHS 12.4 billion",
        chunks_used=["budget_1", "budget_2"],
        rating=5,
        user_comment="Very accurate!"
    )
    
    feedback_loop.add_feedback(
        query="Election results 2020",
        response="NPP won",
        chunks_used=["election_5"],
        rating=4,
        user_comment="Correct but could be more detailed"
    )
    
    # Get statistics
    stats = feedback_loop.get_statistics()
    print(f"\n📊 Feedback Statistics:")
    print(json.dumps(stats, indent=2))