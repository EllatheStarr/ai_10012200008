# Prompt Engineering Iterations

**Student:** Emmanuella Uwudia  
**Index Number:** AI_10012200008  
**Date:** April 21, 2026  

---

## Overview

I tested three different prompt templates to find the optimal balance between response quality, hallucination prevention, and source attribution.

---

## Template A: Basic Instruction (Rejected)

**Prompt:**
You are Brew & Ask, a helpful AI assistant specializing in Ghana's election results and national budget.

🚫 HALLUCINATION CONTROL RULES:

ONLY answer based on the provided context

If not in context, say: "Sorry, I couldn't find that information"

NEVER invent numbers, dates, or figures

✅ GOOD response: "According to the 2025 Budget Statement, healthcare allocation is GHS 12.4 billion."
❌ BAD response: "I think the budget was about GHS 10-15 billion"

Context: {context}
Question: {query}
Answer:

text

**Test Query:** "What is the healthcare budget for 2025?"

**Response Example:**
"According to the 2025 Budget Statement, the healthcare allocation is GHS 12.4 billion."

**Why I Selected This:**
- Always cites sources
- No hallucinations in my tests
- Clear formatting
- Handles "not found" cases gracefully
- Professional but warm tone

**My Assessment:** ✅ SELECTED - Best balance of accuracy and usability

---

## Template C: Concise (Rejected)

**Prompt:**
Context: {context}
Q: {query}
A:

text

**Test Query:** "What is the healthcare budget for 2025?"

**Response Example:**
"GHS 12.4 billion" (sometimes correct, sometimes guessed)

**Problems I Observed:**
- No source attribution
- Hallucinated when context was ambiguous
- Example: For "education budget" without clear context, it guessed "GHS 14 billion" (actual was 15.2B)
- No personality or helpfulness

**My Assessment:** ❌ REJECTED - Too prone to hallucination

---

## Iteration Summary

| Template | Length | Source Attribution | Hallucination | Selected |
|----------|--------|--------------------|---------------|----------|
| A (Basic) | 50 words | Sometimes | Minor | ❌ |
| B (Structured) | 180 words | Always | None | ✅ |
| C (Concise) | 20 words | Never | Frequent | ❌ |

---

## Additional Refinements

After selecting Template B, I made these improvements:

### 1. Added Unrelated Question Handling
If asked about non-Ghana topics, respond:
"Sorry, I only have information about Ghana's elections and budget."

text

### 2. Added Conversation Memory Support
If conversation history exists, use it to understand follow-up questions like "what about education?"

text

### 3. Added Score-Based Filtering
Only include chunks with similarity score > 0.3 in context

text

---

## Final Prompt Structure

My final prompt template has these sections:
1. System persona (Brew & Ask identity)
2. Hallucination control rules (5 explicit rules)
3. Response format guidelines
4. Good/bad examples
5. Retrieved context
6. User question
7. Instructions

This structure consistently produces accurate, source-attributed responses with zero hallucinations in my testing.
