import argparse
import json


def split_file(data, input_file, file_size):
    chunk = []
    current_size = 0
    file_index = 0

    for entry in data:
        entry_size = len(json.dumps(entry).encode("utf-8")) + 1 # +1 for newline
        if current_size + entry_size > file_size:
            output_file = input_file.replace(".json", f"_chunk_{file_index}.json")
            with open(output_file, "w") as f:
                f.write("\n".join(json.dumps(e) for e in chunk) + "\n")
            print(f"Chunk written to {output_file} ({current_size} bytes).")
            chunk = []
            current_size = 0
            file_index += 1

        chunk.append(entry)
        current_size += entry_size

    if chunk:
        output_file = input_file.replace(".json", f"_chunk_{file_index}.json")
        with open(output_file, "w") as f:
            f.write("\n".join(json.dumps(e) for e in chunk) + "\n")
        print(f"Final chunk written to {output_file} ({current_size} bytes).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, default="openai_batch_files/tasks.jsonl", help="Path to input jsonl file.")
    parser.add_argument("--file_size", type=int, default=195 * 1024 * 1024)  # <-- batch api supports 200MB
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        data = [json.loads(line) for line in f]

    split_file(data, args.input_file, args.file_size)
