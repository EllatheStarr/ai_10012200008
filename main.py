"""
File: main.py
Author: Student Name
Index Number: AI_20240001
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Entry point for Brew & Ask - runs data prep, pipeline, and UI
"""

import subprocess
import sys
import os
import argparse

def run_data_preparation():
    """Run all data preparation steps"""
    print("\n" + "="*60)
    print("STEP 1: Data Preparation")
    print("="*60)
    
    # Run data cleaning
    print("\n🟡 Running data cleaning...")
    subprocess.run([sys.executable, "src/data_cleaning.py"])
    
    # Run chunking
    print("\n🟡 Running chunking...")
    subprocess.run([sys.executable, "src/chunking.py"])
    
    # Run embeddings
    print("\n🟡 Generating embeddings...")
    subprocess.run([sys.executable, "src/embeddings.py"])
    
    # Build vector store
    print("\n🟡 Building vector store...")
    subprocess.run([sys.executable, "src/vector_store.py"])
    
    print("\n✅ Data preparation complete!")

def run_pipeline_test():
    """Test the RAG pipeline"""
    print("\n" + "="*60)
    print("STEP 2: Pipeline Test")
    print("="*60)
    
    from src.rag_pipeline import GhanaRAGPipeline
    
    pipeline = GhanaRAGPipeline()
    
    test_queries = [
        "What is the healthcare budget?",
        "Which party won the 2020 election?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        result = pipeline.process_query(query)
        print(f"📊 Response: {result['response'][:200]}...")
        print(f"📈 Scores: {[f'{s:.3f}' for s in result['similarity_scores'][:3]]}")
    
    pipeline.save_logs()
    print("\n✅ Pipeline test complete!")

def run_adversarial_tests():
    """Run adversarial tests"""
    print("\n" + "="*60)
    print("STEP 3: Adversarial Tests")
    print("="*60)
    
    from src.rag_pipeline import GhanaRAGPipeline
    from src.adversarial_tests import GhanaAdversarialTester
    
    pipeline = GhanaRAGPipeline()
    tester = GhanaAdversarialTester(pipeline)
    
    results = tester.run_adversarial_tests()
    comparison = tester.compare_rag_vs_pure_llm([
        "What is the healthcare budget for 2025?",
        "Who won the 2020 election?"
    ])
    
    tester.save_results()
    print("\n✅ Adversarial tests complete!")

def run_ui():
    """Launch Streamlit UI"""
    print("\n" + "="*60)
    print("STEP 4: Launching UI")
    print("="*60)
    print("\n🚀 Starting Brew & Ask UI...")
    print("   Press Ctrl+C to stop\n")
    
    subprocess.run([sys.executable, "-m", "streamlit", "run", "ui/app.py"])

def main():
    parser = argparse.ArgumentParser(description="Brew & Ask - Ghana Elections & Budget Assistant")
    parser.add_argument("--prepare", action="store_true", help="Run data preparation only")
    parser.add_argument("--test", action="store_true", help="Run pipeline test only")
    parser.add_argument("--adversarial", action="store_true", help="Run adversarial tests only")
    parser.add_argument("--ui", action="store_true", help="Launch UI only")
    parser.add_argument("--all", action="store_true", help="Run everything (prepare, test, adversarial, ui)")
    
    args = parser.parse_args()
    
    # Create necessary directories
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/vectors", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    
    print("\n🇬🇭" + "="*58)
    print(" Brew & Ask - Ghana Elections & Budget Assistant")
    print("="*58 + "🇬🇭")
    
    if args.all:
        run_data_preparation()
        run_pipeline_test()
        run_adversarial_tests()
        run_ui()
    elif args.prepare:
        run_data_preparation()
    elif args.test:
        run_pipeline_test()
    elif args.adversarial:
        run_adversarial_tests()
    elif args.ui:
        run_ui()
    else:
        # Default: show help
        parser.print_help()
        print("\nExample usage:")
        print("  python main.py --prepare    # Prepare data")
        print("  python main.py --ui         # Launch UI")
        print("  python main.py --all        # Run everything")

if __name__ == "__main__":
    main()