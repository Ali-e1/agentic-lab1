# Lab 1: LLM agents with Hugging Face models

Course: Agentic AI and Multiagent Systems, University of Messina
Student(s): _your name(s)_

## How to run

Windows PowerShell (create the environment only on first setup):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python check_setup.py
```

Exercise 1.2, in the activated environment:

```powershell
$env:LAB_DTYPE = "bfloat16"
python chat_demo.py
python -m pytest -q tests/test_llm.py
```

The dtype override applies to this terminal session. The default float32 run
failed with a memory allocation error on this machine; bfloat16 completed with
the same 1.5B model. On Linux/macOS, activate with `source .venv/bin/activate`
and run `LAB_DTYPE=bfloat16 python chat_demo.py`.

After implementing Exercises 1.3-1.5, run the original lab tests and agent:

```powershell
python -m pytest -q tests/test_tools_and_parser.py
python react_agent.py "How many kilometres can robot Atlas travel on a full battery?"
python evaluate.py
python smol_agent.py
```

`smol_agent.py` additionally requires Exercise 1.7. The original lab tests are
expected to report 11 failures and 1 pass until the corresponding TODOs are
implemented. The two additional Exercise 1.2 tests check the model wrapper
without downloading or loading model weights.

## Exercise 1.2: local model experiments

Run on 2026-11-17 with Python 3.12.10, torch 2.15.0+cpu, transformers 5.23.0,
and Qwen/Qwen2.5-1.5B-Instruct on CPU using torch.bfloat16.
The setup check passed. Full responses and timings are in
[the experiment output](results/exercise_1_2_chat_demo.txt).

| Experiment | Observation | Tokens/s |
|------------|-------------|----------|
| A: intelligent agent definition | Described perception, actions, goals and reasoning | 8.0 |
| B: temperature 0, three runs | `RoboBite.` every time | 7.1, 7.4, 7.5 |
| B: temperature 1, three runs | `"ZephyrBot"`, `RoboBuddy`, `RoboBuddy` | 6.9, 6.2, 6.3 |
| C: Atlas battery capacity | Approximately 100 Wh; incorrect (1200 Wh in the data) | 7.7 |
| C: arithmetic | 1906; incorrect (37 * 48 + 112 = 1888) | 7.7 |

## Results (Exercise 1.6)

Not run yet; requires the agent implementation in Exercises 1.3-1.5.

| Mode   | Accuracy | Avg. time (s) | Avg. tool calls |
|--------|----------|---------------|-----------------|
| Direct |          |               | 0               |
| Agent  |          |               |                 |

## Answers to the lab questions

### Q1. Device and generation speed

The model ran on CPU with bfloat16 weights. Measured generation speed ranged
from 6.2 to 8.0 tokens/s across the nine replies. Timings cover `generate()`,
including prompt processing, but exclude loading the model, applying the chat
template and decoding the output. No comparison with classmates is available.

### Q2. Temperature 0 versus 1.0

At temperature 0, greedy decoding returned `RoboBite.` on all three runs.
At temperature 1.0 with top_p=0.9, sampling returned `"ZephyrBot"` once and
`RoboBuddy` twice. Sampling can vary the reply but does not guarantee unique
answers. Greedy decoding is useful for an agent because it makes repeated
decisions more reproducible and easier to debug; it does not guarantee that
answers or tool calls are correct.

### Q3. Atlas's battery and hallucination

The model claimed that Atlas has approximately 100 Wh of battery capacity.
The fictional fleet data in `data/fleet.json` says 1200 Wh. The model was not
given that file, so its confident, unsupported claim is a hallucination. An
agent acting on this claim could plan an incorrect route or make a wrong
charging decision. Tools must retrieve the actual fleet data rather than
relying on the model's apparent knowledge. The arithmetic experiment also
returned 1906 instead of 1888, illustrating the need for a calculator tool.

### Q4. Why decode only the new tokens?

`generate()` returns the input prompt tokens followed by newly generated
tokens. Slicing `output[0, prompt_len:]` selects only the assistant's response.
Decoding the whole output would repeat the system prompt and conversation,
and could confuse the later ReAct parser with text from earlier messages.
