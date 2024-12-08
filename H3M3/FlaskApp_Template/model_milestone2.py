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


def storyGeneration_langChain(msg, theme):
    """
    msg is the emotion that the user input;
    type is the type of music genre that the user chooses
    """
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.2,
        max_tokens=1000,
        timeout=None,
        max_retries=2
    )

    system_prompt = (
        "You are an AI educator tasked with changing wording of math word problems to a student's interests and background to make learning more engaging. The student's persona is as follows: {theme}"
        "Original math problem: {scenario_lang}"
        "Take the following math word problem and rewrite it to align with Mia's interests, ensuring the problem is age-appropriate and maintains the same mathematical challenge. DO NOT SOLVE THE PROBLEM. Simply rewrite the question to match Mia’s interests."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{scenario_lang}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    out_message = chain.invoke({
        "scenario_lang" : msg,
        "theme" : theme,

    })

    return out_message

def runModels_langchain(story, theme):
    newStory = storyGeneration_langChain(story,theme)
    return([newStory,theme])

def getRetriever(dir):
    """
    dir is the directory of the vector DB
    """
    embeddings_used = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorDB = Chroma(persist_directory=dir,embedding_function=embeddings_used)
    retriever = vectorDB.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return retriever


def random_story(): 
    """Choose a line at random from the a big file"""
    try:
        line_pos = {} 
     
        with open('contextStories.txt', 'r') as file: 
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
            return line
    except Exception as e:
        print(f"Error reading file: {e}")
        return "Error reading story"

def storyGeneration_langChain_RAG(msg,theme,retrieverDir):
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
        "You are an AI educator tasked with changing wording of math word problems to a student's interests and background to make learning more engaging. The student's persona is as follows: {theme}"
        "Original math problem: {scenario_lang}"
        "Take the following math word problem and rewrite it to align with student's interests, ensuring the problem is age-appropriate and maintains the same mathematical challenge. DO NOT SOLVE THE PROBLEM. Simply rewrite the question to match Mia’s interests."
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


def runModels_langchain_RAG(story, theme, retrieverDir):
    newStory = storyGeneration_langChain_RAG(story,theme,retrieverDir)
    return([newStory,theme])

