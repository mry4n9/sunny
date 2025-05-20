import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
import io

def create_excel_report(company_name, email_data, linkedin_data, facebook_data, search_data, display_data):
    wb = Workbook()

    # --- DEBUG: Print incoming data ---
    print("-" * 30)
    print("DEBUG: excel_processing.py - Incoming Data")
    print(f"Email Data Type: {type(email_data)}, Length: {len(email_data) if isinstance(email_data, list) else 'N/A'}")
    if email_data and isinstance(email_data, list): print(f"First Email Item: {email_data[0] if email_data else 'Empty List'}")
    print(f"LinkedIn Data Type: {type(linkedin_data)}, Length: {len(linkedin_data) if isinstance(linkedin_data, list) else 'N/A'}")
    if linkedin_data and isinstance(linkedin_data, list): print(f"First LinkedIn Item: {linkedin_data[0] if linkedin_data else 'Empty List'}")
    # Add similar prints for facebook_data, search_data, display_data if needed
    print("-" * 30)
    # --- END DEBUG ---

    header_font = Font(color="FFFFFF", bold=True)
    header_fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")

    content_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    def style_sheet(ws, df_columns, sheet_name_for_debug=""):
        for col_idx, column_name in enumerate(df_columns, 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.value = column_name
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = thin_border

        for row_idx, row_obj in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column), 2):
            # --- DEBUG: Print cell values before styling ---
            # print(f"DEBUG: excel_processing.py - Sheet '{sheet_name_for_debug}', Row {row_idx}, Cell Values before styling: {[cell.value for cell in row_obj]}")
            # --- END DEBUG ---
            for cell in row_obj:
                cell.alignment = content_alignment
                cell.border = thin_border

        for col in ws.columns:
            max_length = 0
            column_letter = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[column_letter].width = min(max(adjusted_width, 15), 50)

    # Email Page
    ws_email = wb.active
    ws_email.title = "Email"
    email_cols = ["Ad Name", "Funnel Stage", "Headline", "Subject Line", "Body", "CTA"]
    if email_data and isinstance(email_data, list) and len(email_data) > 0:
        try:
            # --- DEBUG: Before DataFrame creation ---
            print(f"DEBUG: excel_processing.py - Email Data before DF: {email_data}")
            # --- END DEBUG ---
            email_df = pd.DataFrame(email_data, columns=email_cols)
            # --- DEBUG: After DataFrame creation ---
            print(f"DEBUG: excel_processing.py - Email DataFrame:\n{email_df.head().to_string()}")
            # --- END DEBUG ---
            for r_idx, r in enumerate(dataframe_to_rows(email_df, index=False, header=False)):
                # --- DEBUG: Row being appended ---
                print(f"DEBUG: excel_processing.py - Appending to Email sheet, row {r_idx+2}: {r}")
                # --- END DEBUG ---
                ws_email.append(r)
        except Exception as e:
            print(f"ERROR creating Email DataFrame or appending rows: {e}")
            # Fallback: append raw data if DataFrame fails, to see if data itself is the issue
            for item_idx, item_dict in enumerate(email_data):
                 row_values = [item_dict.get(col, "MISSING_KEY") for col in email_cols]
                 print(f"DEBUG: excel_processing.py - Fallback append to Email sheet, row {item_idx+2}: {row_values}")
                 ws_email.append(row_values)

    else:
        print("DEBUG: excel_processing.py - No email_data to process or not a list/empty.")
    style_sheet(ws_email, email_cols, "Email")


    # LinkedIn Page
    ws_linkedin = wb.create_sheet("LinkedIn")
    linkedin_cols = ["Ad Name", "Funnel Stage", "Introductory Text", "Image Copy", "Headline", "Destination", "CTA Button"]
    if linkedin_data and isinstance(linkedin_data, list) and len(linkedin_data) > 0:
        try:
            print(f"DEBUG: excel_processing.py - LinkedIn Data before DF: {linkedin_data}")
            linkedin_df = pd.DataFrame(linkedin_data, columns=linkedin_cols)
            print(f"DEBUG: excel_processing.py - LinkedIn DataFrame:\n{linkedin_df.head().to_string()}")
            for r_idx, r in enumerate(dataframe_to_rows(linkedin_df, index=False, header=False)):
                print(f"DEBUG: excel_processing.py - Appending to LinkedIn sheet, row {r_idx+2}: {r}")
                ws_linkedin.append(r)
        except Exception as e:
            print(f"ERROR creating LinkedIn DataFrame or appending rows: {e}")
            for item_idx, item_dict in enumerate(linkedin_data):
                 row_values = [item_dict.get(col, "MISSING_KEY") for col in linkedin_cols]
                 print(f"DEBUG: excel_processing.py - Fallback append to LinkedIn sheet, row {item_idx+2}: {row_values}")
                 ws_linkedin.append(row_values)
    else:
        print("DEBUG: excel_processing.py - No linkedin_data to process or not a list/empty.")
    style_sheet(ws_linkedin, linkedin_cols, "LinkedIn")

    # FaceBook Page (apply similar debugging)
    ws_facebook = wb.create_sheet("FaceBook")
    facebook_cols = ["Ad Name", "Funnel Stage", "Primary Text", "Image Copy", "Headline", "Link Description", "Destination", "CTA Button"]
    if facebook_data and isinstance(facebook_data, list) and len(facebook_data) > 0:
        try:
            print(f"DEBUG: excel_processing.py - Facebook Data before DF: {facebook_data}")
            facebook_df = pd.DataFrame(facebook_data, columns=facebook_cols)
            print(f"DEBUG: excel_processing.py - Facebook DataFrame:\n{facebook_df.head().to_string()}")
            for r_idx, r in enumerate(dataframe_to_rows(facebook_df, index=False, header=False)):
                print(f"DEBUG: excel_processing.py - Appending to FaceBook sheet, row {r_idx+2}: {r}")
                ws_facebook.append(r)
        except Exception as e:
            print(f"ERROR creating FaceBook DataFrame or appending rows: {e}")
            for item_idx, item_dict in enumerate(facebook_data):
                 row_values = [item_dict.get(col, "MISSING_KEY") for col in facebook_cols]
                 print(f"DEBUG: excel_processing.py - Fallback append to FaceBook sheet, row {item_idx+2}: {row_values}")
                 ws_facebook.append(row_values)
    else:
        print("DEBUG: excel_processing.py - No facebook_data to process or not a list/empty.")
    style_sheet(ws_facebook, facebook_cols, "FaceBook")


    # Google Search Page (apply similar debugging)
    ws_search = wb.create_sheet("Google Search")
    search_cols = ["Headline", "Description"]
    if search_data and isinstance(search_data, list) and len(search_data) > 0:
        try:
            print(f"DEBUG: excel_processing.py - Search Data before DF: {search_data}")
            search_df = pd.DataFrame(search_data, columns=search_cols)
            print(f"DEBUG: excel_processing.py - Search DataFrame:\n{search_df.head().to_string()}")
            for r_idx, r in enumerate(dataframe_to_rows(search_df, index=False, header=False)):
                print(f"DEBUG: excel_processing.py - Appending to Search sheet, row {r_idx+2}: {r}")
                ws_search.append(r)
        except Exception as e:
            print(f"ERROR creating Search DataFrame or appending rows: {e}")
            for item_idx, item_dict in enumerate(search_data):
                 row_values = [item_dict.get(col, "MISSING_KEY") for col in search_cols]
                 print(f"DEBUG: excel_processing.py - Fallback append to Search sheet, row {item_idx+2}: {row_values}")
                 ws_search.append(row_values)
    else:
        print("DEBUG: excel_processing.py - No search_data to process or not a list/empty.")
    style_sheet(ws_search, search_cols, "Google Search")

    # Google Display Page (apply similar debugging)
    ws_display = wb.create_sheet("Google Display")
    display_cols = ["Headline", "Description"]
    if display_data and isinstance(display_data, list) and len(display_data) > 0:
        try:
            print(f"DEBUG: excel_processing.py - Display Data before DF: {display_data}")
            display_df = pd.DataFrame(display_data, columns=display_cols)
            print(f"DEBUG: excel_processing.py - Display DataFrame:\n{display_df.head().to_string()}")
            for r_idx, r in enumerate(dataframe_to_rows(display_df, index=False, header=False)):
                print(f"DEBUG: excel_processing.py - Appending to Display sheet, row {r_idx+2}: {r}")
                ws_display.append(r)
        except Exception as e:
            print(f"ERROR creating Display DataFrame or appending rows: {e}")
            for item_idx, item_dict in enumerate(display_data):
                 row_values = [item_dict.get(col, "MISSING_KEY") for col in display_cols]
                 print(f"DEBUG: excel_processing.py - Fallback append to Display sheet, row {item_idx+2}: {row_values}")
                 ws_display.append(row_values)
    else:
        print("DEBUG: excel_processing.py - No display_data to process or not a list/empty.")
    style_sheet(ws_display, display_cols, "Google Display")


    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)
    return file_stream