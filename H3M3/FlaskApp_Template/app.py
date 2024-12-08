from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from dotenv import load_dotenv
from model_milestone2 import runModels_langchain, runModels_langchain_RAG, random_story
import os
import numpy as np
import random


load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

@app.route('/')
def index():
    return render_template('about.html', active='index')

@app.route('/milestone2', methods=["GET","POST"])
def interaction_2():
    if request.method == 'POST':
        text_story = request.form["story"]
        text_theme = request.form["storyTheme"]
        cwd = os.getcwd()

        db_dir = os.path.join(cwd,"chroma_db")


        (story, theme) = runModels_langchain_RAG(text_story, text_theme, db_dir)

        story = story.replace("\n", "<br>")
        randomStory = random_story()

        return redirect(url_for('interaction_2', story=story, theme=theme, randomStory=randomStory, text_story=text_story, text_theme=text_theme))
    
    story = request.args.get('story', None)
    theme = request.args.get('theme', None)
    randomStory = request.args.get('randomStory', None)
    text_story = request.args.get('text_story', None)
    text_theme = request.args.get('text_theme', None)
    
    return render_template('milestone2.html', active='interaction_2', story=story, theme=theme, randomStory=randomStory, text_story=text_story, text_theme=text_theme)


@app.route('/random_story', methods=['GET'])
def get_random_story():
    mood = random_story()
    return mood.strip()  # Return the mood as plain text

if __name__ == '__main__':
    app.run(host='0.0.0.0')
