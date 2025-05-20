import streamlit as st
import time # For progress simulation if needed

# Import modules
from modules.context_extract import url_extract, additional_extract, magnet_extract
from modules.context_sum import url_sum, additional_sum, magnet_sum
from modules.transparency_report import create_transparency_report
from modules.excel_processing import create_excel_report
from modules.openai_utils import init_openai_client, generate_ad_content_openai # summarize is used by context_sum modules

from prompts import email_prompt, linkedin_prompt, facebook_prompt, search_prompt, display_prompt

# --- Page Configuration ---
st.set_page_config(page_title="M_AI", layout="wide")

# --- App Title and Footer ---
st.title("M_AI")

# --- Initialize OpenAI Client ---
# This should ideally be done once.
# init_openai_client() will set a global 'client' variable in openai_utils
# and return True/False. We can check its status.
if 'openai_client_initialized' not in st.session_state:
    st.session_state.openai_client_initialized = init_openai_client()

if not st.session_state.openai_client_initialized:
    st.error("OpenAI client could not be initialized. Please check your API key in secrets.toml.")
    st.stop()


# --- Session State for Outputs ---
if "transparency_report_bytes" not in st.session_state:
    st.session_state.transparency_report_bytes = None
if "lead_gen_excel_bytes" not in st.session_state:
    st.session_state.lead_gen_excel_bytes = None
if "current_company_name" not in st.session_state:
    st.session_state.current_company_name = ""


# --- Frontend Inputs ---
st.header("Extract Company Context")
company_name_input = st.text_input("Company Name", key="company_name")
url_raw_input = st.text_input("Client’s URL (e.g., example.com)", key="url_raw")
additional_raw_file = st.file_uploader("Upload Additional Company Context (PDF or PPTX)", type=["pdf", "pptx"], key="additional_raw")
magnet_raw_file = st.file_uploader("Upload Lead Magnet (PDF)", type=["pdf"], key="magnet_raw")

st.header("Other Options")
lead_objective_input = st.selectbox("Lead Objective", ["Demo Booking", "Sales Meeting"], key="lead_objective")
learn_more_link_input = st.text_input("Link to “Learn More” page", key="learn_more_link")
magnet_link_input = st.text_input("Link to lead magnet download", key="magnet_link")
book_link_input = st.text_input("Link to Demo or Sales booking page", key="book_link")
count_input = st.slider("Content Count (variations per ad type/stage)", 1, 20, 10, key="count")

generate_button = st.button("Generate Content")

# --- Backend Flow ---
if generate_button:
    # Clear previous outputs from session state
    st.session_state.transparency_report_bytes = None
    st.session_state.lead_gen_excel_bytes = None
    st.session_state.current_company_name = company_name_input

    # Clear all Streamlit cache before starting a new generation
    st.cache_data.clear()
    st.cache_resource.clear() # Though we are not using cache_resource explicitly here.
    
    # Validate required inputs
    if not company_name_input:
        st.error("Company Name is required.")
        st.stop()
    if not url_raw_input:
        st.error("Client's URL is required.")
        st.stop()
    if not learn_more_link_input or not magnet_link_input or not book_link_input:
        st.error("All link inputs (Learn More, Lead Magnet, Booking) are required.")
        st.stop()

    with st.status("Generating content...", expanded=True) as status_ui:
        # 1. Extract Context
        status_ui.write("Step 1/6: Extracting context from sources...")
        url_raw_text = url_extract.extract_text_from_url(url_raw_input)
        additional_raw_text = additional_extract.extract_text_from_additional(additional_raw_file) if additional_raw_file else ""
        magnet_raw_text = magnet_extract.extract_text_from_magnet(magnet_raw_file) if magnet_raw_file else ""
        
        if not url_raw_text: # If URL extraction failed or returned empty
            status_ui.update(label="URL extraction failed or returned no content. Please check the URL.", state="error")
            st.stop()

        # 2. Summarize Context (AI)
        status_ui.write("Step 2/6: Summarizing extracted context (AI)...")
        # The client_ref (None) is a placeholder as summarize_text_openai uses the global client
        url_sum_text = url_sum.get_url_summary(None, url_raw_text, company_name_input)
        additional_sum_text = additional_sum.get_additional_summary(None, additional_raw_text, company_name_input) if additional_raw_text else ""
        magnet_sum_text = magnet_sum.get_magnet_summary(None, magnet_raw_text, company_name_input) if magnet_raw_text else ""

        # 3. Generate Transparency Report (DOCX)
        status_ui.write("Step 3/6: Generating Transparency Report...")
        report_bytes = create_transparency_report(
            company_name_input, url_raw_text, url_sum_text,
            additional_raw_text, additional_sum_text,
            magnet_raw_text, magnet_sum_text
        )
        st.session_state.transparency_report_bytes = report_bytes
        st.session_state.current_company_name = company_name_input


        # 4. Prepare Prompts and Generate Ad Content (AI)
        status_ui.write("Step 4/6: Generating Email ad content (AI)...")
        email_ads_data = []
        email_gen_prompt = email_prompt.get_email_prompt(
            company_name_input, url_sum_text, additional_sum_text,
            lead_objective_input, book_link_input, count_input
        )
        email_json_output = generate_ad_content_openai(None, email_gen_prompt, company_name_input)
        if email_json_output and "emails" in email_json_output:
            email_ads_data = email_json_output["emails"]
        else:
            st.warning("Could not generate or parse Email ad data.")

        linkedin_ads_data = []
        facebook_ads_data = []
        funnel_stages = ["Brand Awareness", "Demand Gen", "Demand Capture"]

        for stage in funnel_stages:
            status_ui.write(f"Step 4/6: Generating LinkedIn ads for {stage} (AI)...")
            linkedin_gen_prompt = linkedin_prompt.get_linkedin_prompt_for_stage(
                company_name_input, url_sum_text, additional_sum_text, magnet_sum_text,
                lead_objective_input, learn_more_link_input, magnet_link_input, book_link_input,
                count_input, stage
            )
            linkedin_json_output = generate_ad_content_openai(None, linkedin_gen_prompt, company_name_input)
            if linkedin_json_output and "linkedin_ads" in linkedin_json_output:
                linkedin_ads_data.extend(linkedin_json_output["linkedin_ads"])
            else:
                st.warning(f"Could not generate or parse LinkedIn ({stage}) ad data.")

            status_ui.write(f"Step 4/6: Generating Facebook ads for {stage} (AI)...")
            facebook_gen_prompt = facebook_prompt.get_facebook_prompt_for_stage(
                company_name_input, url_sum_text, additional_sum_text, magnet_sum_text,
                lead_objective_input, learn_more_link_input, magnet_link_input, book_link_input,
                count_input, stage
            )
            facebook_json_output = generate_ad_content_openai(None, facebook_gen_prompt, company_name_input)
            if facebook_json_output and "facebook_ads" in facebook_json_output:
                facebook_ads_data.extend(facebook_json_output["facebook_ads"])
            else:
                st.warning(f"Could not generate or parse Facebook ({stage}) ad data.")
        
        status_ui.write("Step 4/6: Generating Google Search ad content (AI)...")
        search_ads_data = []
        search_gen_prompt = search_prompt.get_search_prompt(company_name_input, url_sum_text, additional_sum_text)
        search_json_output = generate_ad_content_openai(None, search_gen_prompt, company_name_input)
        if search_json_output and "search_ads" in search_json_output:
            search_ads_data = search_json_output["search_ads"]
        else:
            st.warning("Could not generate or parse Google Search ad data.")

        status_ui.write("Step 4/6: Generating Google Display ad content (AI)...")
        display_ads_data = []
        display_gen_prompt = display_prompt.get_display_prompt(company_name_input, url_sum_text, additional_sum_text)
        display_json_output = generate_ad_content_openai(None, display_gen_prompt, company_name_input)
        if display_json_output and "display_ads" in display_json_output:
            display_ads_data = display_json_output["display_ads"]
        else:
            st.warning("Could not generate or parse Google Display ad data.")

        # 5. Parse and Format into XLSX
        status_ui.write("Step 5/6: Generating Excel report...")
        excel_bytes = create_excel_report(
            company_name_input, email_ads_data, linkedin_ads_data,
            facebook_ads_data, search_ads_data, display_ads_data
        )
        st.session_state.lead_gen_excel_bytes = excel_bytes
        
        status_ui.update(label="Step 6/6: All content generated!", state="complete", expanded=False)
        st.success("Content generation complete! You can now download the files.")

# --- Download Buttons ---
if st.session_state.transparency_report_bytes and st.session_state.current_company_name:
    st.download_button(
        label=f"Download {st.session_state.current_company_name}_transparency_report.docx",
        data=st.session_state.transparency_report_bytes,
        file_name=f"{st.session_state.current_company_name}_transparency_report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

if st.session_state.lead_gen_excel_bytes and st.session_state.current_company_name:
    st.download_button(
        label=f"Download {st.session_state.current_company_name}_lead.xlsx",
        data=st.session_state.lead_gen_excel_bytes,
        file_name=f"{st.session_state.current_company_name}_lead.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- Footer ---
st.markdown("---")
st.markdown("Made by M. Version 0.7")