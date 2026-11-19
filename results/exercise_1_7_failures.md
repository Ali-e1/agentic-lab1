# Exercise 1.7 failure log

- **ToolCallingAgent, default limits.** Qwen repeatedly emitted missing or malformed JSON. All three questions reached the ten-step cap and invoked a fallback. The answers were 18,000 km for Atlas, Atlas for largest payload, and no estimate for Borea.
- **CodeAgent, default limits.** Stopped during the first question after eight completed steps. Qwen called an unavailable Wikipedia tool, emitted replies without the required code block, and attempted an import of `requests` that the interpreter rejected.
- **CodeAgent, two steps and 64 tokens per reply.** Atlas and Borea ran out of steps after replies with missing or incomplete code. Payload listed the fleet, then generated an unterminated string. All three fallback replies gave no usable answer.

Raw transcripts are saved locally in `results/exercise_1_7_*.txt`.
