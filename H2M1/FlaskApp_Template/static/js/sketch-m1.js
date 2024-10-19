let divData, poem, speech, startBtn, stopBtn;

function setup(){
    let c = createCanvas(600, 600);
    c.parent('canvas-div');
    divData = document.querySelector("#canvas-div");

    speech = new p5.Speech(); // speech synthesis object

    // Start button setup
    let startBtnDiv = document.querySelector('#startBtnDiv');
    startBtn = createButton('Start Narrating!');
    startBtn.parent(startBtnDiv);
    startBtn.class('btn btn-primary');
    startBtn.mousePressed(startSpeaking);

    // Stop button setup
    let stopBtnDiv = document.querySelector('#stopBtnDiv');
    stopBtn = createButton('Stop Narrating!');
    stopBtn.parent(stopBtnDiv);
    stopBtn.class('btn btn-danger');
    stopBtn.mousePressed(stopSpeaking);

    formatPoem();  // Format the poem after page load
}

function draw(){
    background(33, 33, 33);
    fill(255);
    rectMode(CENTER);

    // Access the poem data
    poem = divData ? divData.dataset.poem : "Waiting for the poem...";

    textSize(18);
    textWrap(WORD);
}


function addLineBreaks(text) {
    // Replace commas and periods with line breaks
    return text.replace(/,/g, ",<br>").replace(/\./g, ".<br>");
}

function formatPoem() {
    // Get the poem text and format it with line breaks
    let paragraphText = document.getElementById("poemID").textContent;
    let formattedText = addLineBreaks(paragraphText);
    document.getElementById("poemID").innerHTML = formattedText;
}

function startSpeaking(){
    if (poem !== "Waiting for the poem...") {
        speech.speak(poem);
    }
}

function stopSpeaking(){
    speech.stop();
}


