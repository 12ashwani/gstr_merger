import pandas as pd
import os
import streamlit as st

st.set_page_config(page_title="GSTR File Merger", layout="centered")
st.title("📄 GSTR File Merger")

def clean_b2b_sheet(output_path):
    """
    Cleans the 'B2B' sheet by removing rows where key columns are missing.
    Only removes rows with NaN in:
    - 'Invoice Date'
    - 'GSTIN of Supplier'
    - 'Trade/Legal name of the supplier'
    """
    try:
        xls = pd.ExcelFile(output_path)
        if 'B2B' not in xls.sheet_names:
            return

        b2b_df = pd.read_excel(output_path, sheet_name='B2B')

        # Drop rows with missing values in these key columns
        key_columns = ['Invoice Date', 'GSTIN of Supplier', 'Trade/Legal name of the supplier']
        missing_cols = [col for col in key_columns if col not in b2b_df.columns]

        if missing_cols:
            st.warning(f"⚠️ Cannot clean B2B sheet. Missing columns: {', '.join(missing_cols)}")
            return

        b2b_df_cleaned = b2b_df.dropna(subset=key_columns, how='any')

        # Overwrite the B2B sheet
        with pd.ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            b2b_df_cleaned.to_excel(writer, sheet_name='B2B', index=False)

        st.info("🧹 Cleaned 'B2B' sheet by removing rows missing key fields.")
    except Exception as e:
        st.warning(f"⚠️ Failed to clean B2B sheet: {e}")


def merge_gstr_files(folder_path, gstr_type, rows_b2b_1, rows_b2b_2A, skip_impg, skip_export, output_file):
    b2b_data, impg_data, export_data = [], [], []
    os.makedirs("output", exist_ok=True)

    for file in os.listdir(folder_path):
        if (file.endswith(".xlsx") or file.endswith(".xls")) and not file.startswith('~$'):
            path = os.path.join(folder_path, file)
            try:
                xls = pd.ExcelFile(path)

                for sheet in xls.sheet_names:
                    sname = sheet.strip().lower()

                    if not any(key in sname for key in ["b2b", "export", "impg", "b2b,sez,de", "exp", "imps"]):
                        continue

                    # Read appropriate sheets
                    if ("b2b" in sname or "b2b,sez,de" in sname) and gstr_type == "1":
                        df = pd.read_excel(path, sheet_name=sheet, skiprows=rows_b2b_1)
                    elif "b2b" in sname and gstr_type == "2A":
                        df = pd.read_excel(path, sheet_name=sheet, skiprows=rows_b2b_2A)
                    elif "impg" in sname and gstr_type == "2A":
                        df = pd.read_excel(path, sheet_name=sheet, skiprows=skip_impg)
                    elif ("export" in sname or "exp" in sname) and gstr_type == "1":
                        df = pd.read_excel(path, sheet_name=sheet, skiprows=skip_export)
                    else:
                        continue

                    # Clean and tag the data
                    if gstr_type == "2A":
                        df.dropna(how='all', inplace=True)

                    if not df.empty:
                        df["Source File"] = file
                        df["Sheet Name"] = sheet

                        if "b2b" in sname:
                            b2b_data.append(df)
                        elif "impg" in sname:
                            impg_data.append(df)
                        elif "export" in sname or "exp" in sname:
                            export_data.append(df)

            except Exception as e:
                st.warning(f"⚠️ Failed to process '{file}' ({sheet}): {e}")

    output_path = os.path.join("output", output_file)

    # Write merged output
    wrote_data = False
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        if b2b_data:
            pd.concat(b2b_data, ignore_index=True).to_excel(writer, sheet_name='B2B', index=False)
            wrote_data = True
        if impg_data:
            pd.concat(impg_data, ignore_index=True).to_excel(writer, sheet_name='IMPG', index=False)
            wrote_data = True
        if export_data:
            pd.concat(export_data, ignore_index=True).to_excel(writer, sheet_name='EXPORT', index=False)
            wrote_data = True

    if gstr_type == "2A" and wrote_data and b2b_data:
        clean_b2b_sheet(output_path)

    if wrote_data:
        with open(output_path, "rb") as f:
            st.download_button("📥 Download Merged File", f, file_name=output_file)
    else:
        st.warning("⚠️ No relevant sheets were found in the selected folder.")

# === Streamlit UI ===
folder_path = st.text_input("📁 Enter folder path of GSTR files:")
gstr_type = st.selectbox("📌 Select GSTR Type:", ["1", "2A"])
rows_b2b_1 = 3  # Skip rows for B2B in GSTR-1
rows_b2b_2A = 5  # Skip rows for B2B in GSTR-2A
skip_impg = 5    # Skip rows for IMPG in GSTR-2A
skip_export = 3  # Skip rows for Export in GSTR-1
output_file = st.text_input("📄 Output filename (e.g. merged_output.xlsx):", value="merged_output.xlsx")

if st.button("🚀 Start Merging"):
    if not os.path.exists(folder_path):
        st.error("❌ Folder not found!")
    else:
        with st.spinner("🔄 Merging files..."):
            try:
                merge_gstr_files(folder_path, gstr_type, rows_b2b_1, rows_b2b_2A, skip_impg, skip_export, output_file)
                st.success(f"✅ Merging done! File saved as: output/{output_file}")
            except Exception as e:
                st.error(f"❌ Failed: {e}")
