from PyPDF2 import PdfReader
from .prompts import dev_prompt_agent


def read_text(file):
    return file.read()


def read_pdf(file):
    reader = PdfReader(file)
    return "\n\n".join(
        [reader.pages[i].extract_text() for i in range(len(reader.pages))]
    )


"""def agent_prompt_history(data: list[dict[str]]) -> dict:
    new_data = [
        {
            "role": "developer",
            "content": dev_prompt_agent
        }
    ] + data

    return new_data"""
