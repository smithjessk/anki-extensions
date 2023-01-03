#!/Users/jesssmith/opt/anaconda3/bin/python3


# %%

import os
import re
import sys
from typing import Iterable

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def clean_openai_output(x: str) -> Iterable[str]:
    lines = x.strip().split("\n")
    for line in lines:
        base = line.replace("- ", "").strip()
        base_split_again = base.split(",")
        for part in base_split_again:
            part = re.sub("^-", "", part)
            if part not in ["", " ", "  ", "\t", "\n"]:
                yield part.strip()


def extract_important_words(input: str, is_debug_mode: bool = False):
    """tries to clean up gpt-3's output"""
    # TODO consider finetraining on a bunch of my own ankis on wikipedia or w/e- may help both formatting and topic selection
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Extract keywords from this text:\n\n{input}\n\n\n",
        temperature=0.3,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.8,
        presence_penalty=0,
    )
    openai_output = response.choices[0].text
    return clean_openai_output(openai_output)


def ankify_via_openai(input: str, is_debug_mode: bool = False) -> str:
    important_words = list(extract_important_words(input, is_debug_mode=is_debug_mode))
    input = input.lower()
    important_words = list(map(lambda x: x.lower(), important_words))
    print(f"Important words: {list(important_words)}", file=sys.stderr)
    words_to_cloze = set(important_words)
    n_clozes_inserted = 0
    for word_to_cloze in words_to_cloze:
        input = input.replace(
            word_to_cloze,
            "{{c" + str(n_clozes_inserted + 1) + "::" + word_to_cloze + "}}",
        )
        n_clozes_inserted += 1

    return input.strip()


# add argparse argument for a filepath
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="path to file to ankify")
parser.add_argument("--debug", help="print debug info", action="store_true")
args = parser.parse_args()


def replace_parentheticals(input: str) -> str:
    return re.sub(r"\[\d+\]", "", input)


def clean_input_lines(lines: Iterable[str]) -> str:
    nonempty_lines = filter(lambda x: x != "", lines_as_list)
    nonempty_lines = map(lambda x: x.strip(), nonempty_lines)
    return replace_parentheticals("\n".join(nonempty_lines))


if __name__ == "__main__":
    filepath = args.filepath
    with open(filepath, "r") as file:
        lines_as_list = file.readlines()
        cleaned_lines = clean_input_lines(lines_as_list)
        print(ankify_via_openai(cleaned_lines, is_debug_mode=args.debug))

# %%
