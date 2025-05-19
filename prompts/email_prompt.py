def get_email_prompt(company_name, url_sum, additional_sum, lead_objective, book_link, count):
    prompt = f"""
You are an expert advertising copywriter for {company_name}.
Your task is to generate {count} unique email ad variations.

Context:
URL Summary: {url_sum if url_sum else "Not provided."}
Additional Context Summary: {additional_sum if additional_sum else "Not provided."}

Email Requirements:
- Funnel Stage: Demand Capture
- Lead Objective: {lead_objective}
- CTA should lead to: {book_link}

Output Format:
Return a single JSON object with one key "emails". The value of "emails" should be a JSON list, where each item in the list is an object representing one email.
Each email object must have the following keys: "ad_name", "funnel_stage", "headline", "subject_line", "body", "cta".
Ensure "funnel_stage" is always "Demand Capture".
Ad names should be unique and follow the format: "{company_name}_Email_V[N]", e.g., "{company_name}_Email_V1".

Example of the expected JSON structure:
{{
  "emails": [
    {{
      "ad_name": "{company_name}_Email_V1",
      "funnel_stage": "Demand Capture",
      "headline": "Generated Headline 1",
      "subject_line": "Generated Subject Line 1",
      "body": "Generated email body text for variation 1.",
      "cta": "Book Your Demo Now"
    }},
    {{
      "ad_name": "{company_name}_Email_V2",
      "funnel_stage": "Demand Capture",
      "headline": "Generated Headline 2",
      "subject_line": "Generated Subject Line 2",
      "body": "Generated email body text for variation 2.",
      "cta": "Schedule a Meeting"
    }}
  ]
}}
"""
    return prompt