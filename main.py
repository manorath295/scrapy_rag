from scrape_website import scrape
from rag import setup_and_run_rag_pipeline

def main():
    
    scrape("https://docs.chaicode.com/youtube/getting-started/")

    # 2. Ask a question
    question = "What this post is about whatit want to tell i am providing you scrpping lonk why are oyu saying i dont have contex tto answer this wuestion  https://x.com/Life_of_coder/status/1932120974620823688 this is url"
    answer = setup_and_run_rag_pipeline(question)

    print(f"\n❓ Question: {question}\n✅ Answer: {answer}\n")

if __name__ == "__main__":
    main()
