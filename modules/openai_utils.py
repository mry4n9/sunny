import streamlit as st
from openai import OpenAI
import json

# This will be initialized in app.py once API key is confirmed
client = None

def init_openai_client():
    global client
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("OpenAI API key not found in secrets.toml.")
        return False
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        return True
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {e}")
        return False

@st.cache_data(show_spinner=False)
def summarize_text_openai(_client_ref, text_to_summarize, company_name):
    """Summarizes text using OpenAI API, aiming for ~2500 chars."""
    global client # Use the globally initialized client
    if not client:
        st.error("OpenAI client not initialized.")
        return "Error: OpenAI client not initialized."
    if not text_to_summarize:
        return ""

    # Simple prompt for summarization, user will refine later
    prompt_instruction = f"""
    Summarize the following text for the company '{company_name}'.
    The summary should be comprehensive yet concise, capturing the key information.
    Aim for a summary of approximately 2500 characters.
    Do not start with "This text is about..." or similar phrases. Go straight into the summary.

    Text to summarize:
    ---
    {text_to_summarize[:15000]} 
    ---
    Summary:
    """ # Limiting input text to avoid excessive token usage for summarization

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are an skilled expert in text summarization."},
                {"role": "user", "content": prompt_instruction}
            ],
            temperature=0.5,
            max_tokens=700, # Approx 2500 chars / 4 chars_per_token
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return f"Error during summarization: {e}"

@st.cache_data(show_spinner=False)
def generate_ad_content_openai(_client_ref, prompt, company_name):
    """Generates ad content using OpenAI API, expecting JSON output."""
    global client # Use the globally initialized client
    if not client:
        st.error("OpenAI client not initialized.")
        return None
        
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": f"You are an expert advertising copywriter for {company_name}. You always output valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}, # Enforce JSON mode if model supports
            temperature=0.7,
        )
        content = response.choices[0].message.content
        # The response content should be a JSON string.
        # Try to parse it. If it's not valid JSON, it might be an issue with the prompt or model.
        try:
            # Sometimes the model wraps the JSON in ```json ... ```
            if content.strip().startswith("```json"):
                content = content.strip()[7:-3].strip()
            
            json_output = json.loads(content)
            return json_output
        except json.JSONDecodeError as je:
            st.error(f"OpenAI returned non-JSON content for an ad type. Error: {je}")
            st.text_area("Problematic AI Output:", content, height=200)
            return None # Or some error indicator
            
    except Exception as e:
        st.error(f"Error generating ad content: {e}")
        return None