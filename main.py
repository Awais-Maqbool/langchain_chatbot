from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="gemma:2b",
    temperature=0,
    # other params...
)

response = llm.invoke('waht is rag')
print(response.content)