from openai import OpenAI
import os
import json

client = None

def get_client():
    global client
    if client is None:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return client

MODEL = "gpt-4o-mini"

def call_llm(prompt: str) -> str:
    response = get_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a structured reasoning AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def clean_json_string(raw_str: str) -> str:
    raw_str = raw_str.strip()
    if raw_str.startswith("```"):
        if raw_str.startswith("```json"):
            raw_str = raw_str[7:]
        else:
            raw_str = raw_str[3:]
        if raw_str.endswith("```"):
            raw_str = raw_str[:-3]
        raw_str = raw_str.strip()
    start = raw_str.find("{")
    end = raw_str.rfind("}")
    if start != -1 and end != -1 and end > start:
        raw_str = raw_str[start:end+1]
    return raw_str

def call_llm_json(prompt: str, max_attempts: int = 2) -> dict:
    current_prompt = prompt
    last_error = None
    for attempt in range(max_attempts):
        raw_response = call_llm(current_prompt)
        cleaned_response = clean_json_string(raw_response)
        if not cleaned_response or cleaned_response.startswith("I cannot") or "sorry" in cleaned_response.lower():
            raise ValueError(f"LLM Refusal: {raw_response}")
        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            last_error = e
            if attempt < max_attempts - 1:
                current_prompt = f"""{prompt}

CRITICAL: Your previous response was invalid JSON.
Error: {str(e)}
Previous response: {raw_response}

Return ONLY valid JSON. No markdown, no backticks, no extra text.
"""
    raise RuntimeError(f"Failed after {max_attempts} attempts. Last error: {str(last_error)}")

def check_safety(user_input: str) -> bool:
    response = get_client().moderations.create(input=user_input)
    return response.results[0].flagged