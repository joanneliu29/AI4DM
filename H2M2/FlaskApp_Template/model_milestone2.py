import itertools
from transformers import MusicgenForConditionalGeneration
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
from openai import OpenAI
import torch
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model.to(device);
# Use a pipeline as a high-level helper
from transformers import pipeline
from dotenv import load_dotenv
from transformers import AutoProcessor
import scipy
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import random


def poemGeneration_langChain(msg, theme):
    """
    msg is the emotion that the user input;
    type is the type of music genre that the user chooses
    """
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.2,
        max_tokens=200,
        timeout=None,
        max_retries=2
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a expert poem writer. Using deep meaning and short lines or words you generate poem in less than 20 words based on the given emotion and around the theme of {theme}",
            ),
            (
                "human", 
                "{scenario_lang}"
            ),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    out_message = chain.invoke({
        "scenario_lang" : msg,
        "theme" : theme,

    })

    return out_message

def runModels_langchain(emotion, theme):
    poem = poemGeneration_langChain(emotion,theme)
    return([poem,theme])

def getRetriever(dir):
    """
    dir is the directory of the vector DB
    """
    embeddings_used = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorDB = Chroma(persist_directory=dir,embedding_function=embeddings_used)
    retriever = vectorDB.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return retriever


def random_mood(): 
    """Choose a line at random from the a big file"""
    line_pos = {} 
 
    with open('emotions.txt', 'r') as file: 
        # Count the number of lines & record their position 
        for line_count in itertools.count(): 
            file_pos = file.tell() 
            line = file.readline() 
            if not line: 
                break 
            line_pos[line_count] = file_pos 
 
        # Choose a line number 
        chosen_line = random.randint(0, line_count-1) 
 
        # Go to the start of the chosen line. 
        file.seek(line_pos[chosen_line]) 
        line = file.readline() 
        print(line)
    return line 

def poemGeneration_langChain_RAG(msg,theme,retrieverDir):
    """
    msg is the scenario for the story from the pic (hugging face model output);
    type is the genre of the story- Horror, Fantasy, Adventure, Comedy, Mystery, Romance
    retriever is the vector DB with relevant stories from txt version of 
        stories dataset from Hugging face - https://huggingface.co/datasets/ShehryarAzhar/stories
    """
    llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            max_tokens=200,
            timeout=None,
            max_retries=2
        )

    system_prompt = (
        "You are a expert poem writer about the theme of {theme}" 
        "Use the following pieces of retrieved context to generate a poem based on the given emotion and around the theme of {theme} "
        "keep the poem to less than 20 words."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{scenario_lang}"),
        ]
    )

    rag_chain = prompt | llm | StrOutputParser()

    retriever = getRetriever(retrieverDir)

    out_message = rag_chain.invoke({
            "theme" : theme,
            "context":retriever,
            "scenario_lang" : msg,
        })
    
    return out_message


def runModels_langchain_RAG(emotion, theme, retrieverDir):
    poem = poemGeneration_langChain_RAG(emotion,theme,retrieverDir)
    return([poem,theme])

def music2(poem, type):
    audio_length_in_s = 512 / model.config.audio_encoder.frame_rate

    audio_length_in_s
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")

    inputs = processor(
        text=["background music with the style" +type+ "for the poem" + poem],
        padding=True,
        return_tensors="pt",
    )

    audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=512)
    sampling_rate = model.config.audio_encoder.sampling_rate
    output_filename = 'musicgen_out.wav'
    scipy.io.wavfile.write(output_filename, rate=sampling_rate, data=audio_values[0, 0].numpy())
    return output_filename
