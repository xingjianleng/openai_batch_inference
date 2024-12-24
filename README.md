# OpenAI-Batch-Inference
Leverage OpenAI's Batch API for cheaper inference. The example code purposes to demonstrate an example usage on image captioning.

## Install dependencies
```bash
conda create -f environment.yml
```
or
```bash
pip install -r requirements.txt
```

## Run code
Before starting, make sure you have setup `OPENAI_API_KEY` in your environment variables, or store it in a file named `.env` in the root directory of this project. Besides, prepare a list of images stored on your local machine.

Run the `prep` code to generate a single `jsonl` file for all batch requests.
```bash
python batch_caption_prep.py
```

Run the `chunk` code to split the `jsonl` file into smaller chunks to fit into the batch request size limit.
```bash
python batch_caption_chunk.py
```

Run the `submit` code to submit the batch requests to Batch API.
```bash
python batch_caption_submit.py
```

Run the `check` code to check the progress of the batch requests, download the results, and merge them into a single file.
```bash
python batch_caption_check_progress.py
```
