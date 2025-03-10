evaluate_system = """
You are an expert evaluator with extensive experience in evaluating response of given query.
""".strip()

evaluate_prompt = """
Evaluate the Response based on the Query and criteria provided.

** Criteria **
```{criteria}```

** Query **
```{query}```

** Response **
```{response}```

Provide your evaluation based on the criteria:

```{criteria}```

Provide reasons for each score, indicating where and why any strengths or deficiencies occur within the Response. Reference specific passages or elements from the text to support your justification.
Ensure that each reason is concrete, with explicit references to the text that aligns with the criteria requirements.

Scoring Range: Assign an integer score between 1 to 10

** Output format **
Return the results in the following JSON format, Only output this JSON format and nothing else:
```json
{{
    "score": an integer score between 1 to 10,
    "reason": "Specific and detailed justification for the score using text elements."
}}
```
""".strip()
