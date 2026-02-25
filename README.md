# AI Agent

A simple agentic coding assistant powered by Google Gemini. The agent can inspect, read, write, and execute files inside a sandboxed working directory by autonomously choosing and calling the right tools based on a plain-English prompt.

## How it works

```
User prompt (CLI)
       │
       ▼
   main.py  ──── system prompt ────▶ Gemini API
       │                                  │
       │          ◀── function calls ──────┘
       ▼
 call_function.py  (dispatcher)
       │
       ├── get_files_info     – list directory contents
       ├── get_file_content   – read a file (truncated at MAX_CHARS)
       ├── write_file         – create or overwrite a file
       └── run_python_file    – execute a .py script and capture output
       │
       └── result ──▶ Gemini API  (loop up to 20 iterations)
                            │
                            ▼
                     Final text response
```

The agent loops until Gemini returns a plain-text answer or the 20-iteration safety limit is hit.

## Project structure

```
ai-agent/
├── main.py            # Entry point – CLI arg parsing and agentic loop
├── call_function.py   # Function dispatcher (routes Gemini tool calls)
├── prompts.py         # System prompt given to the model
├── config.py          # Shared constants (MAX_CHARS, WORKING_DIR)
├── requirements.txt
└── functions/
    ├── get_file_content.py  # Read a file
    ├── get_file_info.py     # List directory entries
    ├── run_python_file.py   # Execute a Python script
    └── write_file.py        # Write / create a file
```

## Security model

All file-system operations are sandboxed to `WORKING_DIR` (default `./calculator`). Each function validates the resolved path with `os.path.commonpath` before doing anything, so path-traversal attempts (e.g. `../../etc/passwd`) are rejected. Python execution has a 30-second timeout and runs inside the same sandboxed directory.

## Setup

**Requirements:** Python 3.9+, a [Gemini API key](https://aistudio.google.com/app/apikey).

```bash
# 1. Clone and enter the repo
git clone <repo-url>
cd ai-agent

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API key
echo "GEMINI_API_KEY=your_key_here" > .env
```

## Usage

```bash
python main.py "your prompt here"
```

Add `--verbose` to see token counts and the raw output of each tool call:

```bash
python main.py "your prompt here" --verbose
```

### Examples

```bash
# List what's in the working directory
python main.py "What files are in the project?"

# Read and summarise a file
python main.py "Explain what main.py does"

# Run a script and report the output
python main.py "Run calculator.py and tell me the result"

# Write a new file
python main.py "Create a file called notes.txt with a summary of the project"
```

## Configuration

Edit `config.py` to change global settings:

| Constant      | Default          | Description                                      |
|---------------|------------------|--------------------------------------------------|
| `MAX_CHARS`   | `10000`          | Maximum characters read from a file before truncation |
| `WORKING_DIR` | `"./calculator"` | Sandboxed directory the agent can operate in     |

## Model

The agent uses `gemini-2.5-flash` by default. To switch models, update the `model` argument in `main.py`:

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',   # change this
    ...
)
```