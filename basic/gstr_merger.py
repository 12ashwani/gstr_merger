import os
import pandas as pd
from openpyxl import Workbook

class GstrMerger:
    def __init__(self):
        self.b2b_data = []
        self.export_data = []
        

    def merge_gstr_1(self, folder_path, output_file):
        """
        Merges GSTR-1 data from multiple Excel files in a specified folder.
        
        Args:
            folder_path (str): Path to the folder containing GSTR-1 Excel files.
            output_file (str): Path to the output Excel file.
        """
        rows_to_skip_b2b = 3
        rows_to_skip_export = 3
        first_file = True

        for file in os.listdir(folder_path):
            if (file.endswith(".xlsx") or file.endswith(".xls")) and not file.startswith('~$'):
                file_path = os.path.join(folder_path, file)

                try:
                    xls = pd.ExcelFile(file_path)

                    for sheet_name in xls.sheet_names:
                        sheet_lower = sheet_name.strip().lower()

                        # Process B2B sheets
                        if "b2b" in sheet_lower or "b2b, sez, de" in sheet_lower:
                            df_b2b = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=rows_to_skip_b2b)
                            if not first_file:
                                df_b2b = df_b2b.dropna(how='all')
                            if not df_b2b.empty:
                                df_b2b['Source File'] = file
                                df_b2b['Sheet Name'] = sheet_name
                                self.b2b_data.append(df_b2b)

                        # Process Export sheets
                        elif "exp" in sheet_lower or "export" in sheet_lower:
                            df_exp = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=rows_to_skip_export)
                            if not first_file:
                                df_exp = df_exp.dropna(how='all')
                            if not df_exp.empty:
                                df_exp['Source File'] = file
                                df_exp['Sheet Name'] = sheet_name
                                self.export_data.append(df_exp)

                    first_file = False

                except Exception as e:
                    print(f"⚠️ Error reading file {file}: {e}")

        # Combine and save the results
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            if self.b2b_data:
                pd.concat(self.b2b_data, ignore_index=True).to_excel(writer, sheet_name="Merged B2B", index=False)
            if self.export_data:
                pd.concat(self.export_data, ignore_index=True).to_excel(writer, sheet_name="Merged Export", index=False)

        print(f"✅ Merged GSTR-1 data saved to: {output_file}")

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
