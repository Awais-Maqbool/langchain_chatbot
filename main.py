from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(
    model="gemma:2b",
    temperature=0,
)

# class base approach

# messages = [
#     SystemMessage(content='you are helpfull ai assistant'),
#     HumanMessage(content='what is rag')
# ]

# list of tuples

# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ]

# prompt template

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

response = chain.invoke({'question :what is rag '})
print(response)