def get_linkedin_prompt_for_stage(company_name, url_sum, additional_sum, magnet_sum,
                                  lead_objective, learn_more_link, magnet_link, book_link,
                                  count, funnel_stage):

    context_priority = ""
    cta_button = ""
    destination_link = ""
    specific_instructions = ""

    if funnel_stage == 'Brand Awareness':
        cta_button = 'Learn More'
        destination_link = learn_more_link
        context_priority = f"Prioritize general company information from URL Summary and Additional Context Summary for brand building and increasing awareness of {company_name}."
        specific_instructions = f"""
        Introductory Text:
            - Use BAB (Before-After-Bridge) framework.
            - Length: 300-400 characters.
            - Hook: Capture attention within the first 150 characters.
            - Structure: Split into paragraphs for readability.
            - Tone: Engaging and informative.
            - Emojis: Use 1-2 professional emojis where appropriate to enhance readability and engagement, but don't overdo it.
            - Focus: Introduce {company_name} and its core value proposition or a key aspect relevant to brand awareness.
        Image Copy: Text for acompanying image.
        Headline: Around 70 characters. Make it intriguing and relevant to the brand.
        """
    elif funnel_stage == 'Demand Gen':
        cta_button = 'Download'
        destination_link = magnet_link
        context_priority = f"Prioritize the Lead Magnet Summary: '{magnet_sum if magnet_sum else 'Not provided.'}' for generating ad copy. The goal is to get downloads of the lead magnet available at {magnet_link}."
        specific_instructions = f"""
        Introductory Text:
            - Use PAS (Problem-Agitate-Solution) framework.
            - Length: 300-400 characters.
            - Hook: Clearly state the benefit of the lead magnet within the first 150 characters.
            - Structure: Split into paragraphs.
            - Tone: Value-driven and persuasive.
            - Emojis: Use 1-2 professional emojis relevant to a downloadable resource.
            - Focus: Highlight the problems the lead magnet solves or the value it provides.
        Image Copy: Accompanying image text.
        Headline: Around 70 characters. Clearly state what the user will get.
        """
    elif funnel_stage == 'Demand Capture':
        # CTA button text for Demand Capture is dynamic based on lead_objective
        # Example: "Book Demo" -> "Book", "Request Sales Meeting" -> "Request"
        # The prompt asks for the literal 'Register/Request' as per original spec, let's stick to that for the button text.
        # However, the user's example for LinkedIn CTA was "Register/Request". Let's use that.
        # The original spec said: ‘CTA Button’ is literal ‘Register/Request’
        cta_button = "Register" if "Demo" in lead_objective else "Request" # Simplified logic, can be refined. Or stick to "Register/Request"
        if "Demo" in lead_objective:
            cta_button = "Register" # For "Demo Booking"
        elif "Meeting" in lead_objective:
            cta_button = "Request" # For "Sales Meeting"
        else:
            cta_button = "Book Now" # Fallback, or adjust as per precise wording desired.
                                        # The spec says: 'CTA Button’ is literal ‘Register/Request’
        cta_button = "Register/Request" # Sticking to the literal spec for LinkedIn

        destination_link = book_link
        context_priority = f"Focus on the lead objective: '{lead_objective}'. The goal is to get bookings/meetings at {book_link}."
        specific_instructions = f"""
        Introductory Text:
            - Use 4Ps (Promise-Picture-Proof-Push) framework.
            - Length: 300-400 characters.
            - Hook: Directly address the audience's need that your '{lead_objective}' fulfills within the first 150 characters.
            - Structure: Split into paragraphs.
            - Tone: Action-oriented and benefit-focused.
            - Emojis: Use 1-2 professional emojis relevant to booking or consultation.
            - Focus: Persuade users to take the next step ({lead_objective}).
        Image Copy: Accompanying image text.
        Headline: Around 70 characters. Clearly state the offer.
        """

    prompt = f"""
You are an expert advertising copywriter for {company_name} creating LinkedIn ads.
Your task is to generate {count} unique LinkedIn ad variations for the '{funnel_stage}' funnel stage.
Adopt best B2B practices.

Context:
URL Summary: {url_sum if url_sum else "Not provided."}
Additional Context Summary: {additional_sum if additional_sum else "Not provided."}
Lead Magnet Summary (if relevant for stage): {magnet_sum if magnet_sum and funnel_stage == 'Demand Gen' else "Not applicable for this stage or not provided."}
{context_priority}

Ad Requirements for '{funnel_stage}' stage:
- CTA Button Text: {cta_button}
- Destination Link: {destination_link}

Specific Content Instructions for this stage:
{specific_instructions}

Output Format:
Return a single JSON object with one key "linkedin_ads". The value of "linkedin_ads" should be a JSON list, where each item is an object representing one LinkedIn ad.
Each ad object must have the following keys: "Ad Name", "Funnel Stage", "Introductory Text", "Image Copy", "Headline", "Destination", "CTA Button".
Ensure "Funnel Stage" is "{funnel_stage}".
Ensure "CTA Button" is "{cta_button}".
Ensure "Destination" is "{destination_link}".
Ad names should be unique and follow the format: "{company_name}_LinkedIn_{funnel_stage.replace(' ', '')}_V[N]".
Add "\ n" in beginning and end of Introductory Text.

Example of the expected JSON structure (content will vary based on stage):
{{
  "linkedin_ads": [
    {{
      "Ad Name": "{company_name}_LinkedIn_{funnel_stage.replace(' ', '')}_V1",
      "Funnel Stage": "sample",
      "Introductory Text": "sample",
      "Image Copy": "sample",
      "Headline": "sample",
      "Destination": "sample",
      "CTA Button": "sample"
    }}
  ]
}}
"""
    return prompt