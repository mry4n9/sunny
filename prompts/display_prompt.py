def get_display_prompt(company_name, url_sum, additional_sum):
    # Fixed 5 rows. Headline and Description for all 5.
    prompt = f"""
You are an expert advertising copywriter for {company_name} creating Google Display ads.
Your task is to generate 5 ad components for Google Display Ads.

Context:
URL Summary: {url_sum if url_sum else "Not provided."}
Additional Context Summary: {additional_sum if additional_sum else "Not provided."}

Requirements:
- Generate 5 items in total.
- Each item must have a "Headline" (around 30 characters).
- Each item must have a "Description" (around 90 characters).

Output Format:
Return a single JSON object with one key "isplay_ads". The value of "display_ads" should be a JSON list of 5 objects.
Each object must have two keys: "Headline" and "Description".

Example of the expected JSON structure:
{{
  "display_ads": [
    {{ "Headline": "Display Ad Headline 1 (max 30 chars)", "Description": "Display Ad Description 1 (max 90 chars)" }},
    {{ "Headline": "Display Ad Headline 2 (max 30 chars)", "Description": "Display Ad Description 2 (max 90 chars)" }},
    {{ "Headline": "Display Ad Headline 3 (max 30 chars)", "Description": "Display Ad Description 3 (max 90 chars)" }},
    {{ "Headline": "Display Ad Headline 4 (max 30 chars)", "Description": "Display Ad Description 4 (max 90 chars)" }},
    {{ "Headline": "Display Ad Headline 5 (max 30 chars)", "description": "Display Ad Description 5 (max 90 chars)" }}
  ]
}}
"""
    return prompt