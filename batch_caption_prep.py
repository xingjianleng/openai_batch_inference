import argparse
import random
import json
from PIL import Image
from io import BytesIO
import os
import base64


def encoder_image(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_dir", type=str, default="data/images")
    parser.add_argument("--output_file", type=str, default="openai_batch_files/tasks.jsonl")
    parser.add_argument("--prompts", type=str, nargs="+",
                        default=["Provide a detailed and accurate caption for the image."])
    parser.add_argument("--model", type=str, default="gpt-4o-mini-2024-07-18")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--max_tokens", type=int, default=256)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    img_files = [os.path.join(args.img_dir, f) for f in os.listdir(args.img_dir)]
    outputs = []

    for i, img_file in enumerate(img_files):
        img = Image.open(img_file).convert("RGB")
        img_base64 = encoder_image(img)
        prompt = random.choice(args.prompts)
        conv = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}},
                    {"type": "text", "text": prompt}
                ],
            }
        ]
        task = {
            "custom_id": os.path.basename(img_file),
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": args.model,
                "temperature": args.temperature,
                "max_tokens": args.max_tokens,
                "seed": args.seed,
                "messages": conv,
            }
        }
        outputs.append(task)

    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    with open(args.output_file, "w") as f:
        for task in outputs:
            f.write(json.dumps(task) + "\n")
