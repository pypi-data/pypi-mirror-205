import argparse
from oneapi import eval_one_file

def main():
    parser = argparse.ArgumentParser(description="oneapi <command> [<args>]")
    parser.add_argument("--config_file", type=str, help="config file path", required=True)
    parser.add_argument("--eval_data_path",type=str, help="", required=True)
    parser.add_argument("--output_path",type=str, default="", help="", required=False)
    parser.add_argument("--eval_model_name",type=str, default="", help="evaluate model name, e.g., gpt-35-turbo, gpt-4", required=False)
    parser.add_argument("--eval_categories",type=list, default=None, help="choose specific category to eval", required=False)
    parser.add_argument("--sample_num", type=int, default=0, help="sample number of prompts from file to eval", required=False)
    parser.add_argument("--request_interval",type=int, default=1, help="request interval, gpt-4 need longer interval, e.g.,10s", required=False)
    parser.add_argument("--retry",type=bool, default=True, help="", required=False)

    args = parser.parse_args()

    eval_one_file(
        config_file=args.config_file, 
        eval_data_path=args.eval_data_path, 
        output_path=args.output_path, 
        eval_model_name=args.eval_model_name,
        eval_categories=args.eval_categories,
        sample_num=args.sample_num, 
        request_interval=args.request_interval,
        retry=args.retry
        )
    

if __name__ == "__main__":
    main()