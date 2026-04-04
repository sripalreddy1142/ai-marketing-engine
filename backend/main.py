from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key="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")

class Campaign(BaseModel):
    topic: str
    type: str

@app.get("/")
def home():
    return {"message": "AI Marketing Engine Running"}

@app.post("/generate")
def generate_content(data: Campaign):
    try:

        if data.type == "all":
            prompt = f"""
Generate marketing content for: {data.topic}

Include:
1. LinkedIn Post
2. Instagram Caption
3. Email Content
"""
        else:
            prompt = f"Generate {data.type} marketing content for: {data.topic}"

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant",
        )

        content = response.choices[0].message.content

        return {"content": content}

    except Exception as e:
        return {"error": str(e)}