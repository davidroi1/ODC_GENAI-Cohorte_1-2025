from openai import OpenAI

import configs

client = OpenAI(api_key=configs.OPENAI_API_KEY)


def invoke_unique(query, instruction):
    return client.responses.create(
        model="gpt-4o", 
        input=[
            {
                "role": 'developer', 
                "content": query
            }
        ],
        temperature=0,
        instructions=instruction
    )


def invoke_agent(query: list[dict[str]]):
    return client.responses.create(
        model="gpt-4o", 
        input=query,
        temperature=0.6
    )
