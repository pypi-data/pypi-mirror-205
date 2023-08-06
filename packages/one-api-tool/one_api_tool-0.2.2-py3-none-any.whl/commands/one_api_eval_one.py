import sys
import os
import fire

sys.path.append(
    os.path.normpath(f"{os.path.dirname(os.path.abspath(__file__))}/.."))
from oneapi.one_ai_eval import eval_one
from oneapi.one_api import OneAPITool


def main(config_file: str,
         prompt: str,
         answers: list,
         target: str = '',
         model: str = '',
         detail: bool = True):
    tool = OneAPITool.from_config_file(config_file)
    result = eval_one(prompt=prompt,
                      candidate_answers=answers,
                      target=target,
                      model=model,
                      api_tool=tool,
                      detail=detail)
    print('\nSCORE:')
    print(result)


if __name__ == "__main__":
    fire.Fire(main)
