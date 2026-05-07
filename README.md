Running LLMs Locally with llama.cpp

This guide shows you how to set up and run language models on your own computer. No cloud services, no API costs, just you and the model.
Why Run Models Locally?
When you run an LLM locally:

It's free. No subscriptions or per-token charges.
Your data stays on your machine. Nothing gets sent to external servers.
It works offline once you've downloaded the model.
You can experiment and learn without worrying about costs adding up.

This makes local LLMs good for personal projects, learning how AI works, and situations where privacy matters.
What This Tutorial Covers
You'll learn how to:

Install llama.cpp
Pick and download a model that fits your hardware
Run a local API server
Build a simple Python app that uses your local model

Prerequisites
You need:

A computer (any OS - this guide uses Windows)
Python 3.7 or higher
Internet connection for setup (runs offline after)
Storage space for the model (usually 2-10GB depending on which one you pick)

Your RAM determines which models you can run, but there are options for every setup. We'll help you choose in the next section.
Picking a Model for Your System
Models come in different sizes. Larger models are smarter but need more memory.
RAM Guide:

4-8GB RAM: Try Qwen 2.5 3B (around 2GB file)
8-16GB RAM: Qwen 2.5 7B works well (around 4GB)
16GB+ RAM: You can run 14B or larger models

Quantization levels:
Models get compressed using quantization. The labels look like Q4, Q5, Q8:

Q4: Good balance of quality and size (start here)
Q5-Q6: Better quality, larger files
Q2-Q3: Smallest but lower quality

For this tutorial we're using Qwen 2.5 3B Q4_K_M - it runs on most computers and works well for learning.
Finding models:
Search Hugging Face for "[model name] GGUF" - that file format works with llama.cpp. Popular options include Qwen, Gemma, Phi, and LLaMA models.

Step 1: Install llama.cpp
First, we need to download llama.cpp. It's what actually runs the models.
Getting it:

Head to https://github.com/ggerganov/llama.cpp/releases and 
grab the latest version. You'll see a bunch of download options. Here's what to pick:

Regular computer? Get Windows x64 (CPU)

Got an NVIDIA graphics card? Grab Windows x64 (CUDA 12), it'll run way faster

AMD graphics card? Get Windows x64 (HIP)

Not sure? Just go with CPU. It works on everything.
Setting up:

Extract the zip file somewhere you can find it easily. I put mine in Downloads. 

You'll get a folder full of files.

Make sure it works:
Open up Command Prompt (just search "cmd" in the start menu). Then:

**cd C:\your-path-here\llama-cpp**

You enter the llama-cpp folder you just extracted. Then you run:

**llama-cli.exe --version**

You should see some version numbers and info about the build. That means it's working.

Step 2: Download a Model
Now we need to download an actual language model to run.
Get the model:

Go to the Qwen 2.5 3B model page: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF

On the right side of the page you’ll see different quantization levels (Q2, Q4, Q5, etc.)

Click on Q4_K_M, then download it.

Once downloaded, move the .gguf file into your llama.cpp folder

This makes it easier to reference when running commands


Why this model?

Small enough to run on most computers (needs ~4GB RAM)
Q4 quantization gives good quality without huge file size
Instruct version means it's trained to follow instructions
(You can use a bigger model, installation and set up does not change)

Expected performance on CPU:

3B models: usually around 5–15 tokens/second
7B models: around 2–8 tokens/second
First response is often slower while the model warms up

(If you have an NVIDIA GPU and use the CUDA build, speeds can be significantly faster.)

The download will take a few minutes depending on your connection. Once it's in your llama.cpp folder, you're ready for the next step.

Step 3: Start the Server

Now we're going to get the model running as a local server.
Starting it up:

Make sure you're still in the llama.cpp folder in your terminal. If you closed it, open Command Prompt again and navigate back there.

Run this:

llama-server.exe -m qwen2.5-3b-instruct-q4_k_m.gguf --port 8080 --host 127.0.0.1

The model will start loading. Takes maybe 10-30 seconds depending on your computer. You'll see a bunch of text scroll by.

When it's ready, you'll see something like:

HTTP server listening on http://127.0.0.1:8080

Try it out:

Open your browser and go to http://localhost:8080

You should see a chat interface. Type something and hit enter - you're talking to your local model now.

Important: Keep that Command Prompt window open. Close it and the server stops. You need it running for the next steps.

Step 4: Run the Summarizer
The repo includes a simple document summarizer that uses your local model.

Open any code editor and clone the repo, then run:

pip install -r requirements.txt

Try it out:
The repo has a test file already. Make sure your llama-server is still running from Step 3, then in the terminal:
python summarizer.py test.txt

You'll see it read the file, send it to your local model, and print out a summary.

That's it. You're using a local LLM through an API, completely offline and free.



How It Works

The summarizer does three simple things:

Reads your text file
Sends it to http://localhost:8080/v1/chat/completions - that's your local model's API
Gets back a summary and prints it

The API call:
When you send a request to the local server, you're basically having a conversation with the model. You give it:

A system message (tells it what to do - "summarize this")
A user message (the actual text to summarize)

The model processes it and sends back its response. Same structure as any API, just running on your computer instead of in the cloud.

Why this matters:
Normally you'd call something like api.openai.com and pay per request. Here you're calling localhost:8080 and it's free. Same format, different location. That's the whole point - you can swap between local and cloud APIs with barely any code changes.

Troubleshooting

"Could not connect to server" or connection errors:

Your llama-server probably isn't running. Go back to Step 3 and start it up. Remember - you need to keep that terminal window open.

"Out of memory" or model won't load:

The model's too big for your RAM. Try downloading a smaller model or a higher quantization (Q2 or Q3 instead of Q4). Check the model selection guide at the top.
Model generates slowly:

That's normal on CPU. The 3B model does around 5-10 tokens per second on most computers. If you have a GPU and downloaded the CUDA version of llama.cpp, it'll be way faster.

Python says "requests module not found":

You forgot to install requirements. Run pip install -r requirements.txt in the project folder.

Server starts but browser shows nothing:

Give it a minute - sometimes the model takes a bit to fully load. Refresh the page.