import streamlit as st
import os
from basic.gstr_merger import GstrMerger

st.set_page_config(page_title="GSTR Merger Tool", layout="centered")

st.title("📄 GSTR Merger Web App")

# Operation Selection
operation = st.selectbox("Select GSTR Type:", ["GSTR-1", "GSTR-2A"])

# Folder path input
folder_path = st.text_input("Enter the folder path containing GSTR Excel files:")

# Output file name input
output_file_name = st.text_input("Enter the output file name (e.g., merged_gstr.xlsx):")
# os.makedirs("output", exist_ok=True)

# Merge button
if st.button("🔄 Merge GSTR Files"):
    if not folder_path or not output_file_name:
        st.warning("⚠️ Please provide both folder path and output file name.")
    else:
        try:
            merger = GstrMerger()
            output_path = os.path.join(os.getcwd(), output_file_name)

            if operation == "GSTR-1":
                merger.merge_gstr_1(folder_path, output_path)
            else:
                merger.merge_gstr_2A(folder_path, output_path)

            st.success(f"✅ Merged file created successfully: {output_path}")
        except Exception as e:
            st.error(f"❌ Error: {e}")


# merger.merge_gstr_1(
#     folder_path=input("Enter the folder path: "),
#     output_file=os.path.join(os.getcwd(), "merged_gstr_1.xlsx")
# )

# # # Merge GSTR-2A data
# merger.merge_gstr_2A(
#     folder_path=os.path.join(os.getcwd(), "gstr_files"),
#     output_file=os.path.join(os.getcwd(), "merged_gstr_2A.xlsx")


