from fastapi import FastAPI, HTTPException, UploadFile, Body, Response
from schemas import Command, Instruction
import json
from typing import Annotated

from api_llm.src.chain import invoke
from src.prompts import summary_prompt, demande_json, dev_instruction
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

    summary = invoke(query=summary_prompt.format(content=content))

    return {
        "filename": file.filename,
        "summary": summary.output_text,
    }

# -----------------------------------------------------
@app.post('/commande/')
async def commande_client(demande: Annotated[str, Body()]):
    commande_response = invoke(query=demande_json.format(demande=demande))
    json_data = json.loads(commande_response.output_text)
    
    return json_data


# rout for developer
@app.post('/llm/developer/')
async def developer_role(demande: Command):
    response = invoke(query=demande_json.format(demande=demande), instruction=dev_instruction, roles="developer")
    dev_json_data = json.loads(response.output_text)

    return dev_json_data, response.output[0].role


@app.post('/llm/assistance/')
async def assistance_role(demande: Command):
    response = invoke(query=demande_json.format(demande=demande), instruction=dev_instruction, roles="assistant")
    dev_json_data = json.loads(response.output_text)

    return dev_json_data, response.output[0].role


@app.post('/llm/user/')
async def user_role(demande: Command):
    response = invoke(query=demande_json.format(demande=demande), instruction=dev_instruction, roles="user")
    dev_json_data = json.loads(response.output_text)

    return dev_json_data, response.output[0].role


# rout for developer
@app.post('/chat')
async def agent_chat(discution: Annotated[list[dict[str, str]], Body()]):
    agent_response = invoke_agent(query=discution)

    return {
        "role": "assistant",
        "content": agent_response.output_text
    }