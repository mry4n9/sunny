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

Specific Instructions for Email Content:
- **Subject Line**: Make it compelling and concise.
- **Body**:
    - Start with "Hi [Name]," (use this exact placeholder).
    - Consist of 2-3 paragraphs.
    - Maintain a professional and persuasive tone.
    - Clearly articulate the value proposition related to the '{lead_objective}'.
    - Naturally lead to the Call to Action (CTA).
- **CTA**: Should be a clear call to action related to the '{lead_objective}' and '{book_link}'. For example, if the objective is 'Demo Booking', CTA could be 'Book Your Demo' or 'Schedule a Demo'.

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
      "headline": "Generated Headline 1 (often similar to subject or a pre-header)",
      "subject_line": "Generated Subject Line 1",
      "body": "Hi [Name],\\n\\nThis is the first paragraph of the email body, clearly stating the purpose and value.\\n\\nThis is the second paragraph, perhaps elaborating on benefits or addressing a pain point. It leads to the call to action.\\n\\nThis could be a brief third paragraph if needed.",
      "cta": "Book Your Demo Now"
    }},
    {{
      "ad_name": "{company_name}_Email_V2",
      "funnel_stage": "Demand Capture",
      "headline": "Generated Headline 2",
      "subject_line": "Generated Subject Line 2",
      "body": "Hi [Name],\\n\\nAnother variation of the email body, following the 2-3 paragraph structure and professional tone.",
      "cta": "Schedule a Meeting"
    }}
  ]
}}
"""
    return prompt
