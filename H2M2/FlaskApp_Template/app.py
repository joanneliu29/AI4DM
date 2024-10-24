from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from model import runModels, music
from model_milestone2 import runModels_langchain, music2, runModels_langchain_RAG, random_mood
import os
import numpy as np
import random


load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

@app.route('/')
def index():
    return render_template('about.html', active='index')

@app.route('/milestone1', methods=['GET', 'POST'])
def interaction_1():
    if request.method == 'POST':
        text_emotion = request.form["emotion"]

        # Generate the poem
        poem = runModels(text_emotion)

        # Replace newlines with <br> for proper HTML rendering
        poem = poem.replace("\n", "<br>")
        music_file = music(poem)
        #print(music_file)

        # Redirect back to the page with the poem included
        return redirect(url_for('interaction_1', poem=poem, music_file=music_file))

    poem = request.args.get('poem', None)
    music_file = request.args.get('music_file', None)
    return render_template('milestone1.html', active='interaction_1', poem=poem, music_file=music_file)

@app.route('/milestone2', methods=["GET","POST"])
def interaction_2():
    if request.method == 'POST':
        text_emotion = request.form["emotion"]
        text_theme = request.form["poemTheme"]
        cwd = os.getcwd()

        db_dir = os.path.join(cwd,"chroma_db")

        music_style = request.form.get('musicRadioOptions')

        (poem, theme) = runModels_langchain_RAG(text_emotion, text_theme, db_dir)

        poem = poem.replace("\n", "<br>")
        music_file = music2(poem, music_style)
        random_emotion = random_mood()
        print(random_emotion)

        return redirect(url_for('interaction_2', poem=poem, music_file=music_file, music_style=music_style, theme=theme, random_emotion=random_emotion, text_emotion=text_emotion, text_theme=text_theme))
    
    poem = request.args.get('poem', None)
    music_file = request.args.get('music_file', None)
    music_style = request.args.get('music_style', None)
    theme = request.args.get('theme', None)
    random_emotion = request.args.get('random_emotion', None)
    text_emotion = request.args.get('text_emotion', None)
    text_theme = request.args.get('text_theme', None)
    
    return render_template('milestone2.html', active='interaction_2', poem=poem, music_file=music_file, music_style=music_style, theme=theme, random_emotion=random_emotion, text_emotion=text_emotion, text_theme=text_theme)

@app.route('/download/<filename>')
def download_file(filename):
    """
    Serve the generated music file.
    """
    return send_file(filename, as_attachment=True)

@app.route('/random_mood', methods=['GET'])
def get_random_mood():
    mood = random_mood()
    return mood.strip()  # Return the mood as plain text

if __name__ == '__main__':
    app.run(host='0.0.0.0')
