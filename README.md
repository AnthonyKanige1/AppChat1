AppChat

AppChat is a real-time multilingual chat application built with FastAPI on the backend and HTML, CSS, and JavaScript on the frontend. It automatically translates messages into the system language chosen by each user, shows country flags alongside messages, and organizes the chat with timestamps and smooth animations.

Requirements

Python 3.9+

Install dependencies with pip:

pip install fastapi uvicorn[standard] deep-translator


A modern browser such as Chrome, Firefox, Edge, or Safari

Instructions

Clone the repository (or start fresh with Git):

git clone https://github.com/yourusername/AppChat.git
cd AppChat


Create and activate a virtual environment (recommended):

python -m venv .venv
# Mac/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate


Install dependencies:

pip install fastapi uvicorn[standard] deep-translator


Run the server:

uvicorn server:app --reload


Open the app in your browser:
Go to http://127.0.0.1:8000
(Open two tabs with that link to test functionality of translator, i.e. texting yourself basically)

How to Use APPCHAT:

1.Type a message in the input box and press Enter or click Send.

2.Select your preferred system language from the dropdown.

3.Messages from others are automatically translated into your chosen language.

4.If you change your system language, all previous messages (including the “(Original Language: …)” tag) are retranslated instantly.

5.Only the most recent message in a given language will display the flag and original language note; older messages keep only the translation for a clean chat view.

Technologies Used:

Backend: FastAPI, Uvicorn

Frontend: HTML, CSS, JavaScript

Translation: deep-translator (Google Translate API wrapper)
