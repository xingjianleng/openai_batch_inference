import argparse
from openai import OpenAI
import json
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch_file_dir", type=str, default="openai_batch_files")
    parser.add_argument("--task_name", type=str, default="tasks",
                        help="Name of the task (without file extensions!).")
    args = parser.parse_args()

    load_dotenv()
    client = OpenAI()
    job_map = {}

    chunk_files = [
        os.path.join(args.batch_file_dir, f) for f in os.listdir(args.batch_file_dir)
        if f.startswith(f"{args.task_name}_chunk_") and f.endswith(".jsonl")
    ]
    for chunk_file in chunk_files:
        with open(chunk_file, "rb") as f:
            batch_input_file = client.files.create(
                file=f,
                purpose="batch",  # <-- don't change this
            )
            batch_input_file_id = batch_input_file.id

        result = client.batches.create(
            input_file_id=batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={"description": "Image Captioning"},
        )
        job_map[chunk_file] = result.id
    
    with open(os.path.join(args.batch_file_dir, f"{args.task_name}_job_map.json"), "w") as f:
        json.dump(job_map, f, indent=2)
