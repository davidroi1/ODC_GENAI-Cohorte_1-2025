from fastapi import FastAPI, HTTPException, UploadFile, Body, Response
from src.schemas import Command, Instruction
import json
from typing import Annotated

from src.chain import invoke_unique, invoke_agent
from src.prompts import summary_prompt, demande_json
from src.utils import read_pdf, read_text

app = FastAPI(
    title="API LLM", description="Handle OpenAI API for developper", version="0.0.1"
)


@app.get("/")
def api_llm():
    return {"message": "welcom!"}


@app.post("/summary/")
async def get_summary(file: UploadFile):
    if file.content_type == "text/plain":
        content = read_text(file=file.file)
    elif file.content_type == "application/pdf":
        content = read_pdf(file.file)
    else:
        raise HTTPException(
            status_code=500, detail="Only '.pdf' and '.txt' files are supported."
        )

    summary = invoke_unique(query=summary_prompt.format(content=content))

    return {
        "filename": file.filename,
        "summary": summary.output_text,
    }

# -----------------------------------------------------
@app.post('/commande/')
async def commande_client(demande: Annotated[str, Body()]):
    commande_response = invoke_unique(query=demande_json.format(demande=demande))
    json_data = json.loads(commande_response.output_text)
    
    return json_data


# rout for developer
@app.post('/chat')
async def agent_chat(discution: Annotated[list[dict[str, str]], Body()]):
    agent_response = invoke_agent(query=discution)

    return {
        "role": "assistant",
        "content": agent_response.output_text
    }