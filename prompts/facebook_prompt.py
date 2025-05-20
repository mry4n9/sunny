def get_facebook_prompt_for_stage(company_name, url_sum, additional_sum, magnet_sum,
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
        - **Primary Text**:
            - Length: 300-400 characters.
            - Hook: Capture attention and convey the main message within the first 125 characters (visible before 'See More').
            - Structure: Split into 2-3 short paragraphs for readability on mobile.
            - Tone: Engaging, friendly, and informative.
            - Emojis: Use 1-2 relevant and professional emojis (e.g., ✨, 👍, 👀, 🌍) to add personality and visual appeal.
            - Focus: Introduce {company_name}, its mission, or a key unique selling proposition.
        - **Image Copy**: Very short, catchy text for the image/video (3-7 words).
        - **Headline**: Around 27 characters. Make it punchy and attention-grabbing.
        - **Link Description**: Around 27 characters. Provide a brief additional context or benefit.
        """
    elif funnel_stage == 'Demand Gen':
        cta_button = 'Download'
        destination_link = magnet_link
        context_priority = f"Prioritize the Lead Magnet Summary: '{magnet_sum if magnet_sum else 'Not provided.'}' for generating ad copy. The goal is to get downloads of the lead magnet available at {magnet_link}."
        specific_instructions = f"""
        - **Primary Text**:
            - Length: 300-400 characters.
            - Hook: Clearly state the value/benefit of the lead magnet within the first 125 characters.
            - Structure: Split into 2-3 short paragraphs.
            - Tone: Persuasive, highlighting the value of the download.
            - Emojis: Use 1-2 emojis (e.g., 📖, 💡, 🔗, 🎯) relevant to the lead magnet.
            - Focus: Explain what the lead magnet is and why someone should download it.
        - **Image Copy**: Text reinforcing the download offer (e.g., "Free PDF Guide").
        - **Headline**: Around 27 characters. Clear call to download (e.g., "Get Your Free Guide").
        - **Link Description**: Around 27 characters. Briefly mention a key benefit or content of the magnet.
        """
    elif funnel_stage == 'Demand Capture':
        cta_button = 'Book Now' # As specified for Facebook
        destination_link = book_link
        context_priority = f"Focus on the lead objective: '{lead_objective}'. The goal is to get bookings at {book_link}."
        specific_instructions = f"""
        - **Primary Text**:
            - Length: 300-400 characters.
            - Hook: Directly address the audience and the '{lead_objective}' within the first 125 characters.
            - Structure: Split into 2-3 short paragraphs.
            - Tone: Direct, urgent (but polite), and benefit-driven.
            - Emojis: Use 1-2 emojis (e.g., 📅, ⏰, 👉, ✅) that encourage action.
            - Focus: Clearly explain the benefits of taking the action ({lead_objective}) and make it easy to do so.
        - **Image Copy**: Text that supports the booking action (e.g., "Reserve Your Slot!").
        - **Headline**: Around 27 characters. Strong call to action (e.g., "Book Your Demo").
        - **Link Description**: Around 27 characters. Reinforce the value of booking (e.g., "Limited Spots Available").
        """

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

Specific Content Instructions for this stage:
{specific_instructions}

Output Format:
Return a single JSON object with one key "facebook_ads". The value of "facebook_ads" should be a JSON list, where each item is an object representing one Facebook ad.
Each ad object must have the following keys: "ad_name", "funnel_stage", "primary_text", "image_copy", "headline", "link_description", "destination", "cta_button".
Ensure "funnel_stage" is "{funnel_stage}".
Ensure "cta_button" is "{cta_button}".
Ensure "destination" is "{destination_link}".
Ad names should be unique and follow the format: "{company_name}_Facebook_{funnel_stage.replace(' ', '')}_V[N]".

Example of the expected JSON structure (content will vary based on stage):
{{
  "facebook_ads": [
    {{
      "ad_name": "{company_name}_Facebook_{funnel_stage.replace(' ', '')}_V1",
      "funnel_stage": "{funnel_stage}",
      "primary_text": "Generated primary text (300-400 chars, hook in first 125, paragraphs, maybe an emoji ✨).",
      "image_copy": "Short image text.",
      "headline": "Catchy FB Headline (~27c)",
      "link_description": "FB Link Desc. (~27c)",
      "destination": "{destination_link}",
      "cta_button": "{cta_button}"
    }}
  ]
}}
"""
    return prompt