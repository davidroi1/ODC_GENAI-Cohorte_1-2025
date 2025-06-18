from openai import OpenAI

import configs

client = OpenAI(api_key=configs.OPENAI_API_KEY)


def invoke(query, instruction, roles):
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
