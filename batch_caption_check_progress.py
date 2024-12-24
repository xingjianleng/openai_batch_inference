import argparse
from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import time


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_map_file", type=str, default="openai_batch_files/tasks_job_map.json")
    parser.add_argument("--exp_name", type=str, default="tasks")
    parser.add_argument("--output_dir", type=str, default="openai_batch_files")
    args = parser.parse_args()

    load_dotenv()
    client = OpenAI()

    with open(args.job_map_file, "r") as f:
        job_map = json.load(f)
    os.makedirs(args.output_dir, exist_ok=True)

    response_filenames = []
    while True:
        all_finished = True
        for chunk_file, job_id in job_map.items():
            res = client.batches.retrieve(job_id)
            
            if res.status == "completed":
                file_response = client.files.content(res.output_file_id)
                output_file = chunk_file.replace(".jsonl", "_response.jsonl")
                if os.path.exists(output_file):
                    response_filenames.append(output_file)
                    print(f"Response already saved to {output_file}")
                    continue

                with open(output_file, "w") as f:
                    f.write(file_response.text)
                response_filenames.append(output_file)
                print(f"Saved response to {output_file}")

            else:
                all_finished = False
                print(f"Job {job_id} is not completed yet.")
                print(f"{res}\n")

        if all_finished:
            break
        time.sleep(60)

    # Gather all responses into a single file named {exp_name}_all_responses.jsonl
    output_file = os.path.join(args.output_dir, f"{args.exp_name}_all_responses.jsonl")
    with open(output_file, "w") as fw:
        for response_file in response_filenames:
            with open(response_file, "r") as fr:
                for line in fr:
                    fw.write(line)
        print(f"Saved all responses to {output_file}")
