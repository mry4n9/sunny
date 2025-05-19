from ..openai_utils import summarize_text_openai

def get_url_summary(client_ref, url_raw_text, company_name):
    if not url_raw_text:
        return ""
    return summarize_text_openai(client_ref, url_raw_text, company_name)