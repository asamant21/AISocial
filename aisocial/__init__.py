import os

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
BASE_PROMPT = PromptTemplate(template="{question}\n:", input_variables=["question"])

llm = OpenAI(
    model_name="text-davinci-003",
    temperature=1.0,
    openai_api_key=OPENAI_API_KEY,
)
chain = LLMChain(llm=llm, prompt=BASE_PROMPT)


def clean_parsed_output(output: str) -> str:
    """Clean parsed llm output."""
    output = output.strip(" ").strip('";')
    if output[-1] == ".":
        output = output[:-1]
    return output
