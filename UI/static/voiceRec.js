const startBtn = document.querySelector("#start-btn")
var SpeechRecognition = window.SpeechRecognition || webkitSpeechRecognition;
var SpeechGrammarList = window.SpeechGrammarList || webkitSpeechGrammarList;
var SpeechRecognitionEvent = window.SpeechRecognitionEvent || webkitSpeechRecognitionEvent;

var recognition = new SpeechRecognition();
var speechRecognitionList = new SpeechGrammarList();


recognition.grammars = speechRecognitionList;
recognition.continuous = true;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

/*
const SpeechRecognition = window.SpeechRecognition ;

SpeechRecognition.continuous = ;
SpeechRecognition.lang = "en-US";
SpeechRecognition.interimResults = false;
SpeechRecognition.maxAlternatives = 1;
*/
var content = ''



recognition.onstart  = function(){
    document.getElementById('img-mic').src="static/images/mic7.svg";
}

recognition.onend  = function(){
    document.getElementById('img-mic').src="static/images/mic6.svg";
}

startBtn.addEventListener("click",() => {
    recognition.start();
    if(content.length) {
        content += ''
    }
});

startBtn.addEventListener("mouseover",() => {
    recognition.stop();
});


recognition.onresult = (e) => {
     var current = e.resultIndex;
     var transcript = e.results[current][0].transcript;
  console.log( e.results);
  transcript = transcript + '.'
    content = transcript
      document.getElementById('chat__sent').value  = content;

      console.log('test start');
      console.log( 'transcript: ' +transcript);

      /* count 10 second and stop recognition*/
     /*utter.text = 'Hi, How are you';
       console.log(transcript);
     synth.speak(utter);
*/
    /* recognition.stop()*/
};