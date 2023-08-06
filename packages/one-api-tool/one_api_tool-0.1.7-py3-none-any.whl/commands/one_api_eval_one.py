import argparse
from oneapi import eval_one

def main():
    parser = argparse.ArgumentParser(description="oneapi <command> [<args>]")
    parser.add_argument("--config_file", type=str, help="config file path", required=True)
    parser.add_argument("--prompt", type=str, help="question", required=True)
    parser.add_argument("--answers",type=list, help="answer list", required=True)
    parser.add_argument("--target",type=str, default="standard answer", help="", required=False)
    parser.add_argument("--eval_model_name",type=str, default="", help="evaluate model name, e.g., gpt-35-turbo, gpt-4", required=False)
    args = parser.parse_args()

    result = eval_one(
        prompt=args.prompt, 
        answers=args.answers, 
        target=args.target, 
        eval_model_name=args.eval_model_name,
        )
    print(result)

if __name__ == "__main__":
    main()