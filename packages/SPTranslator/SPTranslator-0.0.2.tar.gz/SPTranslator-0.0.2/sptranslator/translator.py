import os
from typing import List
import openai
import logging
import tiktoken
from lark import Lark, UnexpectedInput

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class Translator:

    def __init__(self, source_lang: str, target_lang: str, syntax, api_key: str = "") -> None:
        openai.api_key = api_key
        if api_key == "":
            openai.api_key = os.getenv("OPENAI_API_KEY")
        if openai.api_key == "":
            raise ValueError("OPENAI_API_KEY not found.")

        self.source_lang = source_lang
        self.target_lang = target_lang
        self.syntax = syntax


    def translation(self, texts: List[str]) -> List[str]:
        logger.info("Starting batched translation.")

        prompts = [
            f"#### instruction:\n\nPlease convert the following {self.syntax} code in {self.source_lang} to a {self.syntax} code in {self.target_lang}.\n\n### original {self.syntax} code:\n\n{text}\n\n### {self.target_lang} {self.syntax} code:\n\n"
            for text in texts
        ]

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompts,
            temperature=0.3,
            max_tokens=1500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        result = []
        for choice in response.choices:
            result.append(choice.text)

        logger.info(result)
        logger.info("Batched translation completed.")
        return result


    def translate_text(self, text: str) -> str:
        chunks = divide_into_chunks(text)
        batch_size = 200

        # Batch send API requests
        translated_chunks = []
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            translated_batch = self.translation(batch)
            translated_chunks.extend(translated_batch)

        # join the chunks together
        result = '\n\n'.join(translated_chunks)

        return result


    def translate_file(self, input_path: str, output_path: str) -> None:
        with open(input_path, "r") as f:
            text = f.read()

        translated_text = self.translate_text(text)

        with open(output_path, mode='w') as f:
            f.write(translated_text)
    
        if input_path.endswith(".tex"):
            # Check if the translation is valid LaTeX
            check_braces(translated_text) # simple LaTeX syntax check


def divide_into_chunks(text: str) -> List[str]:
    chunks = text.split('\n\n')
    tokenizer = tiktoken.encoding_for_model("text-davinci-003") 

    ntokens = []
    for chunk in chunks:
        ntokens.append(len(tokenizer.encode(chunk)))

    return group_chunks(chunks, ntokens)


def group_chunks(chunks: List[str], ntokens: List[int], max_len: int = 400) -> List[str]:
    if len(chunks) != len(ntokens):
        raise ValueError("The lengths of chunks and ntokens should be equal.")
    
    batches = []
    cur_batch = ""
    cur_tokens = 0

    for chunk, ntoken in zip(chunks, ntokens):
        if cur_tokens + ntoken > max_len: # Limit the number of words to within block_size
            batches.append(cur_batch)
            cur_batch = ""
            cur_tokens = 0
        cur_batch += "\n\n" + chunk
        cur_tokens += ntoken + 2  # +2 for the newlines between chunks

    if cur_batch:  # Add the last cur_batch if it is not empty
        batches.append(cur_batch)

    batches = [s[2:] for s in batches]
    return batches

# simple LaTeX syntax check
def check_braces(text: str) -> bool:
    grammar = """
        start: "{" inner "}"
        inner: (CHARACTER | "{" inner "}")*
        CHARACTER: /[^{}]+/
    """

    parser = Lark(grammar, start='start')
    
    try:
        parser.parse("{" + text + "}")
        return True
    except UnexpectedInput:
        raise ValueError("Unmatched braces.")
        return False
    