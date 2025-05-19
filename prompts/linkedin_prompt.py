def get_linkedin_prompt_for_stage(company_name, url_sum, additional_sum, magnet_sum, 
                                  lead_objective, learn_more_link, magnet_link, book_link, 
                                  count, funnel_stage):
    
    context_priority = ""
    cta_button = ""
    destination_link = ""

    if funnel_stage == 'Brand Awareness':
        cta_button = 'Learn More'
        destination_link = learn_more_link
        context_priority = f"Prioritize general company information from URL Summary and Additional Context Summary for brand building."
    elif funnel_stage == 'Demand Gen':
        cta_button = 'Download'
        destination_link = magnet_link
        context_priority = f"Prioritize the Lead Magnet Summary: '{magnet_sum if magnet_sum else 'Not provided.'}' for generating ad copy. The goal is to get downloads of the lead magnet."
    elif funnel_stage == 'Demand Capture':
        cta_button = f"{lead_objective.split(' ')[0]}" # e.g., 'Book' or 'Request' from 'Book Demo' or 'Request Sales Meeting'
        destination_link = book_link
        context_priority = f"Focus on the lead objective: '{lead_objective}'. The goal is to get bookings/meetings."

    prompt = f"""
You are an expert advertising copywriter for {company_name} creating LinkedIn ads.
Your task is to generate {count} unique LinkedIn ad variations for the '{funnel_stage}' funnel stage.

Context:
URL Summary: {url_sum if url_sum else "Not provided."}
Additional Context Summary: {additional_sum if additional_sum else "Not provided."}
Lead Magnet Summary (if relevant for stage): {magnet_sum if magnet_sum and funnel_stage == 'Demand Gen' else "Not applicable for this stage or not provided."}
{context_priority}

Ad Requirements for '{funnel_stage}' stage:
- CTA Button Text: {cta_button}
- Destination Link: {destination_link}

Output Format:
Return a single JSON object with one key "linkedin_ads". The value of "linkedin_ads" should be a JSON list, where each item is an object representing one LinkedIn ad.
Each ad object must have the following keys: "ad_name", "funnel_stage", "introductory_text", "image_copy", "headline", "destination", "cta_button".
Ensure "funnel_stage" is "{funnel_stage}".
Ensure "cta_button" is "{cta_button}".
Ensure "destination" is "{destination_link}".
Ad names should be unique and follow the format: "{company_name}_LinkedIn_{funnel_stage.replace(' ', '')}_V[N]".

Example of the expected JSON structure:
{{
  "linkedin_ads": [
    {{
      "ad_name": "{company_name}_LinkedIn_{funnel_stage.replace(' ', '')}_V1",
      "funnel_stage": "{funnel_stage}",
      "introductory_text": "Generated introductory text for LinkedIn ad.",
      "image_copy": "Short text for image/video overlay.",
      "headline": "Compelling LinkedIn Ad Headline",
      "destination": "{destination_link}",
      "cta_button": "{cta_button}"
    }}
  ]
}}
"""
    return prompt