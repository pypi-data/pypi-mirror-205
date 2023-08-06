import argparse
from oneapi import OneAPITool

def main():
    parser = argparse.ArgumentParser(description="oneapi <command> [<args>]")
    parser.add_argument("--config_file", type=str, help="config file path", required=True)
    parser.add_argument("--prompt", type=str, help="question", required=True)
    parser.add_argument("--eval_model_name",type=str, default="", help="evaluate model name, e.g., gpt-35-turbo, gpt-4", required=False)
    parser.add_argument("--temperature",type=float, default=1., help="evaluate model name, e.g., gpt-35-turbo, gpt-4", required=False)
    parser.add_argument("--max_new_tokens",type=int, default=2048, help="evaluate model name, e.g., gpt-35-turbo, gpt-4", required=False)
    args = parser.parse_args()
    tool = OneAPITool.from_config_file(args.config_file)
    result = tool.simple_chat(
        prompt=args.prompt, 
        model=args.eval_model_name,
        temperature=args.temperature,
        max_new_tokens=args.max_new_tokens,
        )
    print(result)

if __name__ == "__main__":
    main()