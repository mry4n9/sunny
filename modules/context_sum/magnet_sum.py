from ..openai_utils import summarize_text_openai

def get_magnet_summary(client_ref, magnet_raw_text, company_name):
    if not magnet_raw_text:
        return ""
    return summarize_text_openai(client_ref, magnet_raw_text, company_name)