import streamlit as st 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

from langchain.schema import SystemMessage,HumanMessage,AIMessage

from dotenv import load_dotenv
import os 


load_dotenv()
google_api_key: str = os.getenv("GOOGLE_API_KEY")

llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=google_api_key
)


if 'conversation' not in st.session_state:
    st.session_state['conversation'] =  ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful assistant that programmer."),
    # HumanMessage(content="{input}")
    ])

if "messages" not in st.session_state:
    st.session_state["messages"] = []


chain: RunnableSequence = st.session_state.conversation | llm | StrOutputParser()



st.title("Chat with GEMINI AI")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.conversation.append(HumanMessage(content=prompt))
    # Display user message in chat message container
    st.session_state.messages.append({"role":"user", "content": prompt})
    


    # Run the chain
    streaming = chain.stream({"input":prompt})

    with st.chat_message("assistant"):
        # st.markdown(response.content)
        response = st.write_stream(streaming)


    # Add assistant message to chat history
    # print(response)
    st.session_state.conversation.append(AIMessage(content=response))
    st.session_state.messages.append({"role":"assistant", "content": response})



