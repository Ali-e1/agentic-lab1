"""Exercise 1.7: the same tools in smolagents, the Hugging Face agent library.

Run:  python smol_agent.py                      (ToolCallingAgent on three questions)
      python smol_agent.py --code               (CodeAgent instead)
      python smol_agent.py "your own question"
"""
from __future__ import annotations

import argparse
import time

import torch
from smolagents import CodeAgent, ToolCallingAgent, TransformersModel, tool

import tools as T
from config import DTYPE, MODEL_ID
from llm import pick_device


# smolagents builds the tool description for the model from the type hints and the docstring,
# so both are required: every argument needs a type hint and a line in the "Args:" section.
@tool
def calculator(expression: str) -> str:
    """Evaluates an arithmetic expression and returns the result as text.

    Args:
        expression: The expression to evaluate, for example "(1200 - 720) / 1200 * 100".
    """
    return T.calculator(expression)


@tool
def get_robot(name: str) -> str:
    """Returns the specification of one robot of the fleet as JSON: battery_wh, consumption_wh_per_km,
    max_payload_kg, speed_kmh and depot.

    Args:
        name: The name of the robot, for example "Borea".
    """
    return T.get_robot(name)


@tool
def list_robots() -> str:
    """Returns the names of all robots in the fleet as comma-separated text."""
    return T.list_robots()


@tool
def get_distance(origin: str, destination: str) -> str:
    """Returns the distance between two depots in kilometres as text.

    Args:
        origin: The starting depot name, for example "Campus".
        destination: The destination depot name, for example "Port".
    """
    return T.get_distance(origin, destination)


QUESTIONS = [
    "How many kilometres can robot Atlas travel on a full battery?",
    "Which robot has the largest maximum payload?",
    "Robot Borea drives from the Campus depot to the Port depot and back. How many Wh of energy does it use?",
]


def build_model(max_new_tokens: int = 512) -> TransformersModel:
    device, dtype = pick_device()
    if DTYPE:
        dtype = getattr(torch, DTYPE)
    return TransformersModel(model_id=MODEL_ID, device_map=device, model_kwargs={"dtype": dtype},
                             max_new_tokens=max_new_tokens)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--code", action="store_true", help="use CodeAgent")
    parser.add_argument("--max-steps", type=int, default=10)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("questions", nargs="*")
    args = parser.parse_args()
    if args.max_steps < 1 or args.max_new_tokens < 1:
        parser.error("step and token limits must be positive")
    model = build_model(args.max_new_tokens)
    my_tools = [calculator, get_robot, list_robots, get_distance]
    if args.code:
        # get_robot returns JSON text, so the generated code may need the json module:
        # smolagents only allows imports that you authorise explicitly.
        agent = CodeAgent(tools=my_tools, model=model, max_steps=args.max_steps, additional_authorized_imports=["json"])
    else:
        agent = ToolCallingAgent(tools=my_tools, model=model, max_steps=args.max_steps)

    for q in args.questions or QUESTIONS:
        start = time.perf_counter()
        answer = agent.run(q)
        steps = len([s for s in agent.memory.steps if type(s).__name__ == "ActionStep"])
        print(f"\nQ: {q}\nA: {answer}   ({steps} steps, {time.perf_counter() - start:.1f} s)\n" + "=" * 70)


if __name__ == "__main__":
    main()
