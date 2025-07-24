import pandas as pd
import os

def merge_gstr_2A(self, folder_path, output_file):
    """
    Merges GSTR-2A data from multiple Excel files in a specified folder.

    Args:
        folder_path (str): Path to the folder containing GSTR-2A Excel files.
        output_file (str): Path to the output Excel file.
    """
    b2b_data = []
    impg_data = []
    rows_to_skip_b2b = 5
    skip_impg = 5
    first_file = True

    for file in os.listdir(folder_path):
        if (file.endswith(".xlsx") or file.endswith(".xls")) and not file.startswith('~$'):
            file_path = os.path.join(folder_path, file)

            try:
                xls = pd.ExcelFile(file_path)

                for sheet_name in xls.sheet_names:
                    sheet_lower = sheet_name.strip().lower()

                    # Process B2B sheets
                    if "b2b" in sheet_lower:
                        df_b2b = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=rows_to_skip_b2b)
                        if not first_file:
                            df_b2b = df_b2b.dropna(how='all')
                        if not df_b2b.empty:
                            df_b2b['Source File'] = file
                            df_b2b['Sheet Name'] = sheet_name
                            b2b_data.append(df_b2b)

                    # Process IMPG sheets
                    elif "impg" in sheet_lower:
                        df_impg = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skip_impg)
                        if not first_file:
                            df_impg = df_impg.dropna(how='all')
                        if not df_impg.empty:
                            df_impg['Source File'] = file
                            df_impg['Sheet Name'] = sheet_name
                            impg_data.append(df_impg)

                first_file = False

            except Exception as e:
                print(f"⚠️ Error reading file {file}: {e}")

    # Save results to Excel
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        if b2b_data:
            pd.concat(b2b_data, ignore_index=True).to_excel(writer, sheet_name="Merged B2B", index=False)
        if impg_data:
            pd.concat(impg_data, ignore_index=True).to_excel(writer, sheet_name="Merged IMPG", index=False)

    print(f"✅ Merged GSTR-2A data saved to: {output_file}")

    # Now clean the B2B sheet
    self.clean_b2b_sheet(output_file)


def clean_b2b_sheet(self, output_file):
    """
    Cleans the 'Merged B2B' sheet in the given Excel file by removing rows with null or incomplete data.

    Args:
        output_file (str): Path to the Excel file to be cleaned.
    """
    try:
        # Read the existing Excel file
        excel_data = pd.read_excel(output_file, sheet_name=None)
        
        # Check if "Merged B2B" exists
        if "Merged B2B" in excel_data:
            b2b_df = excel_data["Merged B2B"]

            # Remove rows with all null values or where important fields are missing
            b2b_df_cleaned = b2b_df.dropna(how='all')  # Drop rows where all values are NaN
            b2b_df_cleaned = b2b_df_cleaned.dropna(subset=b2b_df.columns[:-2], how='any')  # Drop rows missing any core data

            # Save back to Excel (overwrite B2B sheet only)
            with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                b2b_df_cleaned.to_excel(writer, sheet_name="Merged B2B", index=False)

            print("🧹 Cleaned 'Merged B2B' sheet by removing null rows.")
        else:
            print("⚠️ 'Merged B2B' sheet not found in output file.")

    except Exception as e:
        print(f"❌ Error cleaning 'Merged B2B' sheet: {e}")
