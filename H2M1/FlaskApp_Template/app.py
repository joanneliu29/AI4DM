from flask import Flask, render_template, request, redirect, url_for, send_file
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from model import runModels, music
import os
import numpy as np


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

@app.route('/download/<filename>')
def download_file(filename):
    """
    Serve the generated music file.
    """
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
