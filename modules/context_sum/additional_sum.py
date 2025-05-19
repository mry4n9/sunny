from ..openai_utils import summarize_text_openai

def get_additional_summary(client_ref, additional_raw_text, company_name):
    if not additional_raw_text:
        return ""
    return summarize_text_openai(client_ref, additional_raw_text, company_name)