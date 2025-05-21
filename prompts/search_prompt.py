def get_search_prompt(company_name, url_sum, additional_sum):
    # Fixed 15 rows. Headline for all 15. Description for first 4.
    prompt = f"""
You are an expert advertising copywriter for {company_name} creating Google Search ads.
Your task is to generate 15 ad components for Google Search Ads.

Context:
URL Summary: {url_sum if url_sum else "Not provided."}
Additional Context Summary: {additional_sum if additional_sum else "Not provided."}

Requirements:
- Generate 15 items in total.
- Each item must have a "headline" (around 30 characters).
- For the first 4 items, also generate a "description" (around 90 characters).
- For items 5 through 15, the "description" should be an empty string.

Output Format:
Return a single JSON object with one key "search_ads". The value of "search_ads" should be a JSON list of 15 objects.
Each object must have two keys: "Headline" and "Description".

Example of the expected JSON structure (showing first 5 items):
{{
  "search_ads": [
    {{ "Headline": "Generated Headline 1 (max 30 chars)", "Description": "Generated Description 1 (max 90 chars)" }},
    {{ "Headline": "Generated Headline 2 (max 30 chars)", "Description": "Generated Description 2 (max 90 chars)" }},
    {{ "Headline": "Generated Headline 3 (max 30 chars)", "Description": "Generated Description 3 (max 90 chars)" }},
    {{ "Headline": "Generated Headline 4 (max 30 chars)", "Description": "Generated Description 4 (max 90 chars)" }},
    {{ "Headline": "Generated Headline 5 (max 30 chars)" }},
    // ... and so on, up to 15 items
  ]
}}
"""
    return prompt