import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
import io

def create_excel_report(company_name, email_data, linkedin_data, facebook_data, search_data, display_data):
    wb = Workbook()
    
    # Define styles
    header_font = Font(color="FFFFFF", bold=True)
    header_fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    content_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(left=Side(style='thin'), 
                         right=Side(style='thin'), 
                         top=Side(style='thin'), 
                         bottom=Side(style='thin'))

    def style_sheet(ws, df_columns):
        # Style headers
        for col_idx, column_name in enumerate(df_columns, 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.value = column_name
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = thin_border
        
        # Style content cells and set column widths
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column), 2):
            for cell in row:
                cell.alignment = content_alignment
                cell.border = thin_border
        
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter # Get the column name
            for cell in col:
                try: # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[column].width = min(max(adjusted_width, 15), 50) # Min/max width

    # Email Page
    ws_email = wb.active
    ws_email.title = "Email"
    email_cols = ["Ad Name", "Funnel Stage", "Headline", "Subject Line", "Body", "CTA"]
    if email_data:
        email_df = pd.DataFrame(email_data, columns=email_cols)
        for r in dataframe_to_rows(email_df, index=False, header=False): # data only
             ws_email.append(r)
    style_sheet(ws_email, email_cols)


    # LinkedIn Page
    ws_linkedin = wb.create_sheet("LinkedIn")
    linkedin_cols = ["Ad Name", "Funnel Stage", "Introductory Text", "Image Copy", "Headline", "Destination", "CTA Button"]
    if linkedin_data:
        linkedin_df = pd.DataFrame(linkedin_data, columns=linkedin_cols)
        for r in dataframe_to_rows(linkedin_df, index=False, header=False):
            ws_linkedin.append(r)
    style_sheet(ws_linkedin, linkedin_cols)

    # FaceBook Page
    ws_facebook = wb.create_sheet("FaceBook")
    facebook_cols = ["Ad Name", "Funnel Stage", "Primary Text", "Image Copy", "Headline", "Link Description", "Destination", "CTA Button"]
    if facebook_data:
        facebook_df = pd.DataFrame(facebook_data, columns=facebook_cols)
        for r in dataframe_to_rows(facebook_df, index=False, header=False):
            ws_facebook.append(r)
    style_sheet(ws_facebook, facebook_cols)

    # Google Search Page
    ws_search = wb.create_sheet("Google Search")
    search_cols = ["Headline", "Description"]
    if search_data:
        search_df = pd.DataFrame(search_data, columns=search_cols)
        for r in dataframe_to_rows(search_df, index=False, header=False):
            ws_search.append(r)
    style_sheet(ws_search, search_cols)
    
    # Google Display Page
    ws_display = wb.create_sheet("Google Display")
    display_cols = ["Headline", "Description"]
    if display_data:
        display_df = pd.DataFrame(display_data, columns=display_cols)
        for r in dataframe_to_rows(display_df, index=False, header=False):
            ws_display.append(r)
    style_sheet(ws_display, display_cols)

    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)
    return file_stream