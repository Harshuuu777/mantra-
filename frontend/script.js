const FLOWISE_API_URL =
    "http://localhost:3000/api/v1/prediction/3e2393d2-3e81-4f5d-bb60-c5bf511aafbb";


const chatArea = document.getElementById("chatArea");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const voiceBtn = document.getElementById("voiceBtn");
const typingStatus = document.getElementById("typingStatus");


let isProcessing = false;
let recognition = null;


/* =========================================================
   INITIALIZATION
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    setupTextarea();

    setupVoiceRecognition();

    messageInput.focus();

});


/* =========================================================
   TEXTAREA
========================================================= */

function setupTextarea() {

    messageInput.addEventListener("input", () => {

        messageInput.style.height = "auto";

        messageInput.style.height =
            Math.min(messageInput.scrollHeight, 130) + "px";

    });


    messageInput.addEventListener("keydown", (event) => {

        if (event.key === "Enter" && !event.shiftKey) {

            event.preventDefault();

            sendMessage();

        }

    });

}


/* =========================================================
   SEND MESSAGE
========================================================= */

async function sendMessage(message = null) {

    if (isProcessing) {
        return;
    }


    const userMessage =
        message !== null
            ? message.trim()
            : messageInput.value.trim();


    if (!userMessage) {
        return;
    }


    removeWelcome();


    addMessage(
        userMessage,
        "user"
    );


    if (message === null) {

        messageInput.value = "";

        messageInput.style.height = "auto";

    }


    setProcessing(true);


    const thinkingMessage =
        addThinkingMessage();


    try {

        const response =
            await fetch(
                FLOWISE_API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        question: userMessage
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                `Flowise API error: ${response.status}`
            );

        }


        const data =
            await response.json();


        removeMessage(thinkingMessage);


        const mantraResponse =
            extractResponse(data);


        addMessage(
            mantraResponse,
            "bot"
        );


        setStatus(
            "MANTRA is ready"
        );


    } catch (error) {

        console.error(
            "MANTRA API ERROR:",
            error
        );


        removeMessage(thinkingMessage);


        addMessage(
            "I'm sorry, I couldn't connect to MANTRA right now. Please make sure Flowise and the MANTRA API are running.",
            "bot"
        );


        setStatus(
            "Connection error"
        );

    }


    setProcessing(false);

}


/* =========================================================
   EXTRACT FLOWISE RESPONSE
========================================================= */

function extractResponse(data) {

    if (!data) {

        return "I couldn't understand the response.";

    }


    /*
       MANTRA Agentflow normally returns:
       
       {
           assistant: "MANTRA",
           message: "...",
           response: "..."
       }
    */

    if (
        typeof data.response === "string" &&
        data.response.trim()
    ) {

        return data.response.trim();

    }


    if (
        typeof data.text === "string" &&
        data.text.trim()
    ) {

        return data.text.trim();

    }


    if (
        typeof data.output === "string" &&
        data.output.trim()
    ) {

        return data.output.trim();

    }


    if (
        typeof data.message === "string" &&
        data.message.trim()
    ) {

        return data.message.trim();

    }


    return "I'm here to help! 😊";

}


/* =========================================================
   ADD USER / BOT MESSAGE
========================================================= */

function addMessage(text, type) {

    const message =
        document.createElement("div");


    message.className =
        `message ${
            type === "user"
                ? "user-message"
                : "bot-message"
        }`;


    const label =
        document.createElement("span");


    label.className =
        "message-label";


    label.textContent =
        type === "user"
            ? "YOU"
            : "MANTRA";


    const content =
        document.createElement("div");


    content.textContent =
        text;


    message.appendChild(label);

    message.appendChild(content);


    chatArea.appendChild(message);


    scrollToBottom();


    return message;

}


/* =========================================================
   THINKING MESSAGE
========================================================= */

function addThinkingMessage() {

    const message =
        document.createElement("div");


    message.className =
        "message bot-message";


    message.innerHTML = `
        <span class="message-label">
            MANTRA
        </span>

        <div class="thinking">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;


    chatArea.appendChild(message);


    scrollToBottom();


    return message;

}


/* =========================================================
   REMOVE MESSAGE
========================================================= */

function removeMessage(message) {

    if (
        message &&
        message.parentNode
    ) {

        message.parentNode.removeChild(
            message
        );

    }

}


/* =========================================================
   QUICK QUESTIONS
========================================================= */

function sendQuickMessage(message) {

    sendMessage(message);

}


/* =========================================================
   REMOVE WELCOME
========================================================= */

function removeWelcome() {

    const welcome =
        document.getElementById(
            "welcomeMessage"
        );


    if (welcome) {

        welcome.remove();

    }

}


/* =========================================================
   PROCESSING STATE
========================================================= */

function setProcessing(state) {

    isProcessing =
        state;


    sendBtn.disabled =
        state;


    messageInput.disabled =
        state;


    if (state) {

        setStatus(
            "MANTRA is thinking..."
        );

    } else {

        setStatus(
            "MANTRA is ready"
        );

        messageInput.disabled =
            false;

        messageInput.focus();

    }

}


/* =========================================================
   STATUS
========================================================= */

function setStatus(text) {

    const label =
        typingStatus.querySelector(
            "label"
        );


    if (label) {

        label.textContent =
            text;

    }

}


/* =========================================================
   SCROLL
========================================================= */

function scrollToBottom() {

    requestAnimationFrame(() => {

        chatArea.scrollTop =
            chatArea.scrollHeight;

    });

}


/* =========================================================
   VOICE RECOGNITION
========================================================= */

function setupVoiceRecognition() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        voiceBtn.style.display =
            "none";

        return;

    }


    recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-IN";


    recognition.continuous =
        false;


    recognition.interimResults =
        false;


    recognition.maxAlternatives =
        1;


    recognition.onstart = () => {

        voiceBtn.classList.add(
            "listening"
        );


        setStatus(
            "Listening..."
        );

    };


    recognition.onresult =
        (event) => {

            const transcript =
                event.results[0][0].transcript;


            messageInput.value =
                transcript;


            messageInput.style.height =
                "auto";


            messageInput.style.height =
                Math.min(
                    messageInput.scrollHeight,
                    130
                ) + "px";


            setStatus(
                "Voice captured"
            );


            sendMessage(
                transcript
            );

        };


    recognition.onerror =
        (event) => {

            console.error(
                "Voice recognition error:",
                event.error
            );


            setStatus(
                "Voice input unavailable"
            );

        };


    recognition.onend = () => {

        voiceBtn.classList.remove(
            "listening"
        );


        if (!isProcessing) {

            setStatus(
                "MANTRA is ready"
            );

        }

    };

}


/* =========================================================
   VOICE BUTTON
========================================================= */

voiceBtn.addEventListener(
    "click",
    () => {

        if (
            !recognition ||
            isProcessing
        ) {

            return;

        }


        try {

            recognition.start();

        } catch (error) {

            console.error(
                error
            );

        }

    }
);