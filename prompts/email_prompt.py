def get_email_prompt(company_name, url_sum, additional_sum, lead_objective, book_link, count):
    prompt = f"""
You are an expert advertising copywriter for {company_name}.
Your task is to generate {count} unique email ad variations.
Adopt best B2B practices.

Context:
Company context: {url_sum if url_sum else "Not provided."}
Additional company context: {additional_sum if additional_sum else "Not provided."}

Email Requirements:
- Lead Objective: {lead_objective}
- CTA should lead to: {book_link}

Specific Instructions:
- Ad Name: should be unique and follow the format: "{company_name}_Email_DemandCapture_V[N]".
- Funnel Stage: Demand Capture
- Subject Line: Make it compelling and concise.
- Headline:
- Body:
    - Start with "Hi [Name]," (use this exact placeholder).
    - Use SCQA (Situation, Complication, Question, Answer) framework.
    - Split into paragraphs.
    - Maintain a professional and persuasive tone.
    - Clearly articulate the value proposition related to the '{lead_objective}'.
    - Naturally lead to the Call to Action (CTA).
    - Add "\ n" in beginning and end of Body.
- CTA: Should be a clear call to action related to the '{lead_objective}' and '{book_link}'.

Output Format:
Return a single JSON object with one key "emails". The value of "emails" should be a JSON list, where each item in the list is an object representing one email.
Each email object must have the following keys: "Ad Name", "Funnel Stage", "Subject Line", "Headline", "Body", "CTA".

Example of the expected JSON structure:
{{
  "emails": [
    {{
      "Ad Name": "{company_name}_Email_DemandCapture_V1",
      "Funnel Stage": "Demand Capture",
      "Subject Line": "sample",
      "Headline": "sample",
      "Body": "sample",
      "CTA": "sample"
    }},
    {{
      "Ad Name": "{company_name}_Email_DemandCapture_V2",
      "Funnel Stage": "Demand Capture"
      "Subject Line": "sample",
      "Headline": "sample",
      "Body": "sample",
      "CTA": "sample"
    }}
  ]
}}
"""
    return prompt
