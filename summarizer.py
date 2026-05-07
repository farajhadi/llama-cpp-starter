#this is a very basic script just to show one of the many use cases of local llms

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import requests


API_URL = "http://localhost:8080/v1/chat/completions"


def read_text_file(file_path: Path) -> str:
    """Read a UTF-8 text file and return its contents."""
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except UnicodeDecodeError as exc:
        raise UnicodeDecodeError(
            exc.encoding,
            exc.object,
            exc.start,
            exc.end,
            f"Could not decode {file_path} as UTF-8. Try saving it as UTF-8 text.",
        ) from exc


def summarize_text(text: str, model: str = "local-model") -> str:
    """Send text to the local LLM and return the summary."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that creates concise, natural paragraph summaries. "
                "Summarize the text in 2-3 clear sentences without using bullet points or lists."
            ),
        },
        {
            "role": "user",
            "content": (
                "Please summarize the following document in plain English as one short paragraph.\n\n"
                f"{text}"
            ),
        },
    ]

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=120)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(
            "Could not reach the local LLM server at http://localhost:8080. "
            "Make sure llama.cpp server is running."
        ) from exc

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(
            "Unexpected response format from the LLM API. "
            "Expected an OpenAI-compatible chat completion response."
        ) from exc


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Summarize a text file using a local LLM server."
    )
    parser.add_argument("file_path", help="Path to a text file to summarize")
    parser.add_argument(
        "--model",
        default="local-model",
        help="Model name sent to the API (default: local-model)",
    )
    return parser.parse_args()


def main() -> int:
    """Program entry point."""
    args = parse_args()
    path = Path(args.file_path)

    try:
        text = read_text_file(path)
        if not text.strip():
            print("The file is empty.", file=sys.stderr)
            return 1

        summary = summarize_text(text, model=args.model)
        print("\nSummary:\n")
        print(summary)
        return 0
    except (FileNotFoundError, UnicodeDecodeError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())