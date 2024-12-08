let speech;

window.addEventListener('load', function() {
    // Initialize speech synthesis
    speech = new p5.Speech();
    
    // Create start button
    let startBtnDiv = document.querySelector('#startBtnDiv');
    let startBtn = document.createElement('button');
    startBtn.textContent = 'Start Narrating!';
    startBtn.className = 'btn btn-primary';
    startBtn.onclick = startSpeaking;
    startBtnDiv.appendChild(startBtn);

    // Create stop button
    let stopBtnDiv = document.querySelector('#stopBtnDiv');
    let stopBtn = document.createElement('button');
    stopBtn.textContent = 'Stop Narrating!';
    stopBtn.className = 'btn btn-danger';
    stopBtn.onclick = stopSpeaking;
    stopBtnDiv.appendChild(stopBtn);
});

function startSpeaking() {
    const story_text = document.querySelector("#storyID").innerText;
    if (story_text !== "Waiting for the problem...") {
        speech.speak(story_text);
    }
}

function stopSpeaking() {
    speech.stop();
}

// Keep the random story functionality
function updateRandomStory() {
    fetch('/random_story')
        .then(response => response.text())
        .then(data => {
            document.getElementById('formFile').value = data;
        })
        .catch(error => console.error('Error fetching random story:', error));
}

document.querySelector('.btn-secondary').addEventListener('click', updateRandomStory);
