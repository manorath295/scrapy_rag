from scrape_website import scrape
from rag import setup_and_run_rag_pipeline

def main():
    
    scrape("website url")

    # 2. Ask a question
    question = "Here Ask The Qestion"
    answer = setup_and_run_rag_pipeline(question)

    print(f"\n❓ Question: {question}\n✅ Answer: {answer}\n")

if __name__ == "__main__":
    main()
