
from backend.rag.chat_engine import ask_question

question = "How does AI help doctors?"

print("RESEARCHAI PDF CHATBOT")
print("======================")

result = ask_question(question)

print("\nAI ANSWER:")
print(result["answer"])

print("\nSOURCES:")
for source in result["sources"]:
    print("-", source)
