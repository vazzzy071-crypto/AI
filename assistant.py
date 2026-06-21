import base64
import mimetypes
from groq import Groq

class GeminiAssistant:
    def __init__(self, name: str, api_key: str):
        self.name = name
        self.api_key = api_key
        
        if not self.api_key or self.api_key == "your_api_key_here":
            self.client = None
            self.error = f"API Key for {self.name} is missing or invalid."
        else:
            try:
                self.client = Groq(api_key=self.api_key)
                self.error = None
            except Exception as e:
                self.client = None
                self.error = str(e)

    def send_message_stream(self, history_data, prompt: str, files=None):
        if self.error:
            yield f"Error: {self.error}"
            return
            
        messages = []
        messages.append({"role": "system", "content": "Siz foydali, aqlli yordamchisiz. Barcha savollarga o'zbek tilida to'g'ri javob berasiz."})
        
        for msg in history_data:
            text_parts = [p for p in msg.get("parts", []) if isinstance(p, str)]
            if text_parts:
                messages.append({
                    "role": "user" if msg["role"] == "user" else "assistant", 
                    "content": "\n".join(text_parts)
                })
                
        content = [{"type": "text", "text": prompt}]
        
        if files:
            for f in files:
                mime_type, _ = mimetypes.guess_type(f.name)
                if not mime_type:
                    mime_type = "image/jpeg"
                
                if mime_type.startswith("image/"):
                    base64_image = base64.b64encode(f.getvalue()).decode('utf-8')
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}",
                        }
                    })

        messages.append({"role": "user", "content": content})
        
        try:
             stream = self.client.chat.completions.create(
                 model='llama-3.2-90b-vision-preview',
                 messages=messages,
                 temperature=0.7,
                 stream=True
             )
             
             for chunk in stream:
                 if chunk.choices[0].delta.content is not None:
                     yield chunk.choices[0].delta.content
        except Exception as e:
             yield f"\n\n**API Error:** {str(e)}"
