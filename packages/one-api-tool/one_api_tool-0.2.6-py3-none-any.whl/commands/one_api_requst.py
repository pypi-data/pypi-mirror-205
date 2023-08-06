import sys
import os
import fire

sys.path.append(
    os.path.normpath(f"{os.path.dirname(os.path.abspath(__file__))}/.."))
from oneapi import OneAPITool


def main(config_file: str,
         prompt: str,
         model: str = '',
         temperature: float = 1.,
         max_new_tokens: int = 2048):
    tool = OneAPITool.from_config_file(config_file)
    result = tool.simple_chat(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_new_tokens=max_new_tokens,
    )
    print(f'{model} response:\n{result}')


if __name__ == "__main__":
    fire.Fire(main)