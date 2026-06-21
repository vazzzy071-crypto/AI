import mimetypes
from google import genai
from google.genai import types
from tools import gemini_tools

class GeminiAssistant:
    def __init__(self, name: str, api_key: str):
        self.name = name
        self.api_key = api_key
        
        if not self.api_key or self.api_key == "your_api_key_here":
            self.client = None
            self.error = f"API Key for {self.name} is missing or invalid."
        else:
            try:
                self.client = genai.Client(api_key=self.api_key)
                self.error = None
            except Exception as e:
                self.client = None
                self.error = str(e)
                
    def get_chat_session(self, history_data=None):
        """Reconstructs the chat session from Streamlit history."""
        if self.error:
            return None
            
        config = types.GenerateContentConfig(
            tools=gemini_tools,
            temperature=0.7,
        )
        
        history = []
        if history_data:
            for msg in history_data:
                # We only append text parts to history for simplicity,
                # as recreating file uploads in history can be complex
                text_parts = [types.Part.from_text(text=p) for p in msg["parts"] if isinstance(p, str)]
                if text_parts:
                    history.append(types.Content(role=msg["role"], parts=text_parts))
                
        try:
            return self.client.chats.create(
                model='gemini-2.5-flash',
                config=config,
                history=history
            )
        except Exception as e:
            self.error = f"Failed to initialize chat session: {str(e)}"
            return None

    def send_message_stream(self, chat_session, prompt: str, files=None):
        """Sends a message to the chat session and yields the response chunks."""
        if self.error:
            yield f"Error: {self.error}"
            return
            
        if not chat_session:
             yield "Error: Chat session is not initialized."
             return

        message_parts = [prompt]
        if files:
             for f in files:
                 mime_type, _ = mimetypes.guess_type(f.name)
                 if not mime_type:
                     mime_type = "application/octet-stream"
                 
                 message_parts.append(
                     types.Part.from_bytes(
                         data=f.getvalue(),
                         mime_type=mime_type,
                     )
                 )
                 
        try:
             # The SDK handles tool calling automatically under the hood
             response_stream = chat_session.send_message_stream(message_parts)
             for chunk in response_stream:
                 if chunk.text:
                     yield chunk.text
        except genai.errors.APIError as e:
             yield f"\n\n**API Error:** {str(e)}"
        except Exception as e:
             yield f"\n\n**Error:** {str(e)}"
