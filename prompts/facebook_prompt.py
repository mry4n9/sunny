def get_facebook_prompt_for_stage(company_name, url_sum, additional_sum, magnet_sum,
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
        cta_button = 'Book Now' # As specified
        destination_link = book_link
        context_priority = f"Focus on the lead objective: '{lead_objective}'. The goal is to get bookings."

    prompt = f"""
You are an expert advertising copywriter for {company_name} creating Facebook ads.
Your task is to generate {count} unique Facebook ad variations for the '{funnel_stage}' funnel stage.

Context:
URL Summary: {url_sum if url_sum else "Not provided."}
Additional Context Summary: {additional_sum if additional_sum else "Not provided."}
Lead Magnet Summary (if relevant for stage): {magnet_sum if magnet_sum and funnel_stage == 'Demand Gen' else "Not applicable for this stage or not provided."}
{context_priority}

Ad Requirements for '{funnel_stage}' stage:
- CTA Button Text: {cta_button}
- Destination Link: {destination_link}

Output Format:
Return a single JSON object with one key "facebook_ads". The value of "facebook_ads" should be a JSON list, where each item is an object representing one Facebook ad.
Each ad object must have the following keys: "ad_name", "funnel_stage", "primary_text", "image_copy", "headline", "link_description", "destination", "cta_button".
Ensure "funnel_stage" is "{funnel_stage}".
Ensure "cta_button" is "{cta_button}".
Ensure "destination" is "{destination_link}".
Ad names should be unique and follow the format: "{company_name}_Facebook_{funnel_stage.replace(' ', '')}_V[N]".

Example of the expected JSON structure:
{{
  "facebook_ads": [
    {{
      "ad_name": "{company_name}_Facebook_{funnel_stage.replace(' ', '')}_V1",
      "funnel_stage": "{funnel_stage}",
      "primary_text": "Engaging primary text for Facebook ad.",
      "image_copy": "Text for image/video creative.",
      "headline": "Catchy Facebook Ad Headline",
      "link_description": "Brief description appearing below headline.",
      "destination": "{destination_link}",
      "cta_button": "{cta_button}"
    }}
  ]
}}
"""
    return prompt