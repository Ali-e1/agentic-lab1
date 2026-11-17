# Lab 1: Local LLM agents

Agentic AI and Multiagent Systems, University of Messina.
Student(s): _your name(s)_

## Run (PowerShell)

```powershell
py -3.12 -m venv .venv                 # first setup only
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python check_setup.py
$env:LAB_DTYPE = "bfloat16"            # set in each new terminal
python chat_demo.py
python -m pytest -q tests/test_llm.py
```

Float32 ran out of memory; bfloat16 worked. Exercise 1.2 tests: **2 passed**.
The original lab tests still have 11 expected failures until Exercises 1.3–1.5 are implemented.

## Exercise 1.2 — results and answers

2026-11-17: Qwen2.5-1.5B-Instruct, Python 3.12.10, torch 2.15.0+cpu,
transformers 5.23.0. [Full experiment output](results/exercise_1_2_chat_demo.txt).

- **Q1 — Speed:** CPU, bfloat16, **6.2–8.0 tokens/s**. Timing covers generation, excluding model loading and text decoding. No classmate comparison available.
- **Q2 — Temperature:** At 0, all three replies were `RoboBite.`; at 1.0, `ZephyrBot`, `RoboBuddy`, `RoboBuddy`. Greedy decoding improves repeatability for agents, but does not guarantee correctness.
- **Q3 — Hallucination:** Atlas's battery was claimed to be about **100 Wh**, versus **1200 Wh** in `data/fleet.json`. Acting on invented data could cause incorrect route or charging decisions. The model also answered **1906** for arithmetic whose correct result is **1888**, motivating a calculator tool.
- **Q4 — Decoding:** `output[0, prompt_len:]` selects only new tokens; decoding everything would repeat the prompt and could confuse the agent's parser.

## Remaining work

1. Exercises 1.3–1.5: calculator, parser, agent loop; pass all 12 original tests.
2. Exercise 1.6: run `python evaluate.py`; record accuracy, timing and Q5–Q8.
3. Exercise 1.7: complete the tools; compare `python smol_agent.py` with `python smol_agent.py --code`; answer Q9–Q10.
