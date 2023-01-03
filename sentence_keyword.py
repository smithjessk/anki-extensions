#!python3

# %%

import os
from typing import Iterable

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def split_text_into_sentences(text: str) -> Iterable[str]:
    """splits text into sentences, and removes empty ones"""
    sentences = text.split(".")
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence not in ["", " ", "\t", "\n"]:
            yield sentence


test_text = """
In computer science, a call stack is a stack data structure that stores information about the active subroutines of a computer program. This kind of stack is also known as an execution stack, program stack, control stack, run-time stack, or machine stack, and is often shortened to just "the stack". Although maintenance of the call stack is important for the proper functioning of most software, the details are normally hidden and automatic in high-level programming languages. Many computer instruction sets provide special instructions for manipulating stacks.
"""


def summarize(sentence: str) -> str:
    """summarizes a sentence using openai's summarization api"""
    prompt = f"Extract one key phrase from this text:\n\n{sentence}\n\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.8,
        presence_penalty=0,
    )

    return response.choices[0].text.strip()  # type: ignore


from dataclasses import dataclass

import yaml

# test it
"""
for sentence in split_text_into_sentences(test_text):
    print({"sentence": sentence, "summary": summarize(sentence)})
"""
# %%

from dataclasses import dataclass

import yaml


@dataclass
class Card:
    """a card to be added to anki. just a front and back"""

    front: str
    back: str

    def __to_yaml(self):
        """returns a yaml representation of the card"""
        return yaml.dump(self.__dict__)

    def to_yaml_for_anki_cli(self):
        """format per https://github.com/julien-sobczak/anki-cli"""
        d = [
            {
                "type": "Basic",
                "tags": ["auto_generated"],
                "fields": {
                    "Front": self.front,
                    "Back": self.back,
                },
            }
        ]
        return yaml.dump(d)


# test

c = Card("myFront", "myBack")
s = c.to_yaml_for_anki_cli()
with open("test.yaml", "w") as f:
    f.write(s)

# %%
