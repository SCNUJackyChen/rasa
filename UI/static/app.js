var synth = window.speechSynthesis;
function textToSpecch(text)
{
 if(document.querySelector('#chatbox__synth').checked)
    {
var synth = window.speechSynthesis;
let utter = new SpeechSynthesisUtterance('hi');
   var voices = synth.getVoices();
    utter.text = text;
    utter.voice = voices[0];
     synth.speak(utter);
}
}
class Chatbox {

    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'), /* function in button*/
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            selectButton: document.querySelector('#chatbox__content'),
            selectButton1: document.querySelector('#chatbox__content1'),
            selectButton2: document.querySelector('#chatbox__content2')

        }

        this.state = false; /* close the chatbox */
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton,selectButton,selectButton1,selectButton2} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox)) /*if click then do the function*/

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        selectButton.addEventListener('click', () => this.select1SendButton(chatBox))

         selectButton1.addEventListener('click', () => this.select2SendButton(chatBox))

         selectButton2.addEventListener('click', () => this.select3SendButton(chatBox))

        const node = chatBox.querySelector('#chat__sent');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
        /* 长按Press space， can speech and convert the speech to text */
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box add chatbox--active in css
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }
   /* testfunction(text){
        console.log(text)
    }  */
    onSendButton(chatbox) {
        var textField = chatbox.querySelector('#chat__sent');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }
      /*  this.testfunction(text1)*/
        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
/* $SCRIPT_ROOT    'http://127.0.0.1:5000/predict'*/
        fetch($SCRIPT_ROOT +'/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
            console.log(msg2.message);
            textToSpecch(msg2.message);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {

            if (item.name === "Sam")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
                /*console.log(item.message);*/
               /* textToSpecch(item.message);*/
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

    select1SendButton(chatbox) {
        var textField = chatbox.querySelector('#chatbox__content');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
/* $SCRIPT_ROOT    'http://127.0.0.1:5000/predict'*/
        fetch($SCRIPT_ROOT +'/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
             textToSpecch(msg2.message);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }
    select3SendButton(chatbox) {
        var textField = chatbox.querySelector('#chatbox__content2');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
/* $SCRIPT_ROOT    'http://127.0.0.1:5000/predict'*/
        fetch($SCRIPT_ROOT +'/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
             textToSpecch(msg2.message);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }
        select2SendButton(chatbox) {
        var textField = chatbox.querySelector('#chatbox__content1');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
/* $SCRIPT_ROOT    'http://127.0.0.1:5000/predict'*/
        fetch($SCRIPT_ROOT +'/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
             textToSpecch(msg2.message);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }
}


const chatbox = new Chatbox();
chatbox.display();