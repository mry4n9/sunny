import requests
from bs4 import BeautifulSoup
import streamlit as st

@st.cache_data(show_spinner=False)
def extract_text_from_url(url_raw):
    """Extracts all text content from a given URL."""
    if not url_raw:
        return ""
    
    url = url_raw
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        
        text = soup.get_text(separator=' ', strip=True)
        return text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL ({url_raw}): {e}")
        return ""
    except Exception as e:
        st.error(f"Error parsing URL content ({url_raw}): {e}")
        return ""