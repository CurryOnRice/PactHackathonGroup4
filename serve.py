#!/usr/bin/env python
from typing import List
import os
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser
from langserve import add_routes

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import ConversationChain
import gradio as gr
from langchain.prompts import PromptTemplate






load_dotenv()
API_KEY = os.getenv('OPEN_API_KEY')
llm = ChatOpenAI(openai_api_key=API_KEY)

chat = ChatOpenAI()
conversation = ConversationChain(llm=chat)


tupleEmpty = ()

def chatButtonPressed(text, chatHistory):

    #chatHistory.append(text)

    chat = ChatOpenAI()
    chat(
        [
            HumanMessage(
                content=text
            )
        ]
        )
    
    response = conversation.run(text)

    chatHistory.append((text, response))

    return {
        userBox: gr.Textbox(value=""),
        chatbox: chatHistory,
        }

    return 
    
    

def returnString(emotion):

    prompt1 = ""

    match emotion:
        case "Feliz", "Confiante":
            prompt1 = "Comece por perguntar ao utilizador porque está {emotion}."
        case "Calmo":
            prompt1 = "Comece por perguntar se gosta da música de fundo."
        case "Zangado", "Triste", "Perturbado":
            prompt1 = "Tente acalmar o utilizador, que se sente {emotion}."
        case "Não sei":
            prompt1 = "Tente perceber como o utilizador se está a sentir."

    return prompt1


def updated_interface(personName, age, gender, emotion, audior):

    if(personName=="" or age==None or gender==None or emotion==None or audior==None):
            return {
            pageOne: gr.Column(visible=True),
            pageTwo: gr.Column(visible=False),
            audio:   gr.Audio("restaurant.mp3", interactive=False, visible=False, autoplay=False, container=False)
,
        }



    prompt1 = ""

    match emotion:
        case "Feliz":
            prompt1 = "Comece por perguntar ao utilizador se há algum motivo particular pelo qual está feliz."
        case "Confiante":
            prompt1 = "Comece por perguntar ao utilizador se há algum motivo particular pelo qual está confiante."
        case "Calmo":
            prompt1 = "Comece por perguntar se gosta da música de fundo."
        case "Zangado":
            prompt1 = "Tente acalmar o utilizador, que se sente zangado."
        case "Triste":
            prompt1 = "Tente motivar o utilizador, que se sente triste."
        case "Perturbado":
            prompt1 = "Tente motivar o utilizador, que se sente perturbado."
        case "Não sei":
            prompt1 = "Tente perceber como o utilizador se está a sentir."



    prompt_template = PromptTemplate.from_template(
        "O nome do utilizador é {name}."
        "A idade do utilizador é {age}."
        "O género do utilizador é {gender}."
        "O utilizador sente-se {emotion}."
        "O utilizador está a ouvir {audior}."
        "Se a idade do utilizador tiver menos de 30 anos, utilize gíria."
        "Você é um psicólogo e amigo do utilizador, que tem pensamentos suicidas."
        "Se o utilizador lhe perguntar como está, responda que está feliz."
        
        "{firstprompt}"
    )
    
    prompt = prompt_template.format(name=personName, age=age, gender=gender, emotion=emotion, audior=audior, firstprompt=prompt1)

    global conversation
    conversation = ConversationChain(llm=chat)

    conversation(prompt)

    if(audior=="Fogueira"):
        finalSound = gr.Audio("fireplace.mp3", interactive=False, visible=False, autoplay=True, container=False)
    if(audior=="Ondas do Mar"):
        finalSound = gr.Audio("ocean.mp3", interactive=False, visible=False, autoplay=True, container=False)
    if(audior=="Jazz"):
        finalSound = gr.Audio("jazz.mp3", interactive=False, visible=False, autoplay=True, container=False, )
    if(audior=="Silêncio"):
        finalSound = gr.Audio("jazz.mp3", interactive=False, visible=False, autoplay=False, container=False, )

    
    
    return {
            pageOne: gr.Column(visible=False),
            pageTwo: gr.Column(visible=True),
            audio: finalSound,
        }




css = """
#buttonred {color: red;}
.feedback textarea {font-size: 24px !important}
"""

#css=".gradio-container {background-color: #ffffff}"
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    
    with gr.Column(visible=True) as pageOne:

        audio = gr.Audio("restaurant.mp3", interactive=False, visible=False, autoplay=False, container=False)

        gr.Label(value = "O seu amigo virtual.", container=False)

        personName = gr.Textbox(label="Nome", placeholder='Introduza o seu nome.')

        age = gr.Slider(minimum=0.0, maximum=100.0, step=1.0, label="Idade")

        gender = gr.Radio(["Homem", "Mulher", "Outro"], label="Qual é o seu género?"),

        color = gr.Radio(["Feliz", "Calmo", "Confiante", "Zangado", "Triste", "Perturbado", "Não sei"], label="Como se sente?"),

        som = gr.Radio(["Silêncio", "Fogueira", "Ondas do Mar", "Jazz"], label="Qual o som que mais o relaxa?"),


        button = gr.Button(value="Confirmar")


    with gr.Column(visible=False) as pageTwo:
        gr.Label(value = "O seu amigo virtual.", container=False)
        chatbox = gr.Chatbot(label="Conversa")
        userBox = gr.Textbox(container=False, placeholder='Introduza a sua mensagem.')
        chatbutton = gr.Button(value="Enviar Mensagem")
        

    button.click(updated_interface, inputs=[personName, age, gender[0], color[0], som[0]], outputs=[pageOne, pageTwo, audio],)
    chatbutton.click(chatButtonPressed, inputs = [userBox, chatbox], outputs = [userBox, chatbox])





if __name__ == "__main__":
    conversation = ConversationChain(llm=chat)
    demo.launch(show_api=False) 