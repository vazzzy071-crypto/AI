# Gemini Assistant

A Python web application that provides a powerful, single AI assistant powered by Google's Gemini API. 

## Setup Instructions

1. **Clone or Download** this project to your local machine.

2. **Create a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Copy `.env.example` to a new file called `.env`.
   - Open `.env` and fill in your details:
     - Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
     - Set the `GEMINI_API_KEY` and your preferred `ASSISTANT_NAME`.

## Running the App

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will launch in your default web browser. Enjoy your intelligent assistant!
