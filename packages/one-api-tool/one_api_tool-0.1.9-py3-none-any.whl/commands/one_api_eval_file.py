import os
import sys
import fire
sys.path.append(os.path.normpath(f"{os.path.dirname(os.path.abspath(__file__))}/.."))
from oneapi.one_ai_eval import eval_one_file

def main(
        config_file: str, 
        eval_data_path: str, 
        output_path: str='', 
        model: str='',
        eval_categories: str='',
        sample_num: int=0, 
        request_interval: int=1,
        retry:bool=True,
        detail:bool=False
        ):

    eval_one_file(
        config_file=config_file, 
        eval_data_path=eval_data_path, 
        output_path=output_path, 
        model=model,
        eval_categories=eval_categories,
        sample_num=sample_num, 
        request_interval=request_interval,
        retry=retry,
        detail=detail
        )
    

if __name__ == "__main__":
    fire.Fire(main)