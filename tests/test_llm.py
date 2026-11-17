"""Exercise 1.2 checks without loading model weights."""
from unittest.mock import Mock

import torch

from llm import LocalLLM


def make_llm():
    llm = LocalLLM.__new__(LocalLLM)
    llm.device = "cpu"
    llm.tokenizer = Mock()
    inputs = {"input_ids": torch.tensor([[1, 2, 3]])}
    llm.tokenizer.apply_chat_template.return_value.to.return_value = inputs
    llm.model = Mock()
    llm.model.generate.return_value = torch.tensor([[1, 2, 3, 4, 5]])
    llm.tokenizer.decode.return_value = "  Hello  "
    return llm


def test_greedy_decodes_only_new_tokens_and_records_stats():
    llm = make_llm()
    assert llm.chat([{"role": "user", "content": "Hi"}], max_new_tokens=8) == "Hello"
    options = llm.model.generate.call_args.kwargs
    assert options["do_sample"] is False
    assert options["max_new_tokens"] == 8
    assert "temperature" not in options
    assert "top_p" not in options
    assert llm.tokenizer.decode.call_args.args[0].tolist() == [4, 5]
    assert llm.last_stats["prompt_tokens"] == 3
    assert llm.last_stats["new_tokens"] == 2
    assert llm.last_stats["seconds"] >= 0


def test_sampling_and_stop_strings():
    llm = make_llm()
    llm.tokenizer.decode.return_value = "Answer\nObservation: invented result"
    assert llm.chat([], temperature=1.0, stop=["Observation:"]) == "Answer"
    options = llm.model.generate.call_args.kwargs
    assert options["do_sample"] is True
    assert options["temperature"] == 1.0
    assert options["top_p"] == 0.9
    assert options["stop_strings"] == ["Observation:"]
    assert options["tokenizer"] is llm.tokenizer
