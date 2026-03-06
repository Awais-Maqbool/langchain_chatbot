from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os


# load_dotenv()
# llm = ChatOllama(
#     model='model_name',
#     temperature='temperature',
# )

load_dotenv()
llm = ChatOllama(
    model=os.getenv('model_name'),
    temperature=float(os.getenv('temperature','0.7')),
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
    MessagesPlaceholder(variable_name='chat_history'),   # dynamically point out the history
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

# response = chain.invoke({'question :what is rag '})
# print(response)


chat_histry = []
# max_turns = 5   #10 exchanges = 20 messages (Human + AI)


def chat(question):

    current_turns = len(chat_histry)//2
    if current_turns>=os.getenv('max_turns'):
        return(
            '....context window is full'
            'the ai nay not follow your previous thread properly'
            'please type "clear" for a new chat'
        )
    response = chain.invoke({'question':question,'chat_history' : chat_histry})

    chat_histry.append(HumanMessage(content=question))
    chat_histry.append(AIMessage(content=response))

    remaining = os.getenv('max_turns')-(current_turns+1)
    if remaining<=2:
        response+= f'warning: your {remaining} turns {current_turns} left'

    return response

# print(chat('what is dog'))            #chat_history = [] ->empty
# print(chat('is dog a faithfull animal?'))
# print(chat('how many types of cat in the world'))

def main():
    print('langchain chat bot ready! (type "quit" for exit , "clear" reset the history)')
    while True: 
        user_input = input('you:').strip()

        if not user_input:
            continue

        if user_input.lower()=='quit':
            break
        if user_input.lower()=='clear':
            chat_histry.clear()
            print('hisory cleared,Starting fresh')
            continue

        print(f'Ai: {chat(user_input)}\n')
main()
