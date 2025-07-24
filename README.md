# 📄 GSTR File Merger (Streamlit App)

A simple and efficient web-based tool built using **Streamlit** to merge **GSTR-1** and **GSTR-2A** Excel files from multiple suppliers into a single consolidated and cleaned Excel report.

---

## 🚀 Features

- 🔍 **Auto-detection of relevant GSTR sheets:**
  - Detects and processes sheets like `B2B`, `IMPG`, `EXPORT`, `EXP`, `B2B,SEZ,DE`, etc.

- 📂 **Batch processing:**
  - Automatically reads and processes all `.xlsx` and `.xls` files in a selected folder.

- 🧹 **Smart data cleaning (for GSTR-2A B2B):**
  - Automatically removes rows where any of the following fields are missing:
    - `Invoice Date`
    - `GSTIN of Supplier`
    - `Trade/Legal name of the supplier`

- 📎 **Metadata tracking:**
  - Adds columns like:
    - `Source File`
    - `Sheet Name`

- 💾 **One-click download:**
  - Final merged Excel file is available for immediate download.

- ✅ **Built with Python, Pandas, Streamlit, and OpenPyXL**

---

## 📁 Input

- A folder containing multiple Excel files received from vendors/suppliers.
- Each Excel file should contain sheets with GSTR formats such as `B2B`, `IMPG`, `EXPORT`, etc.

---

## 📤 Output

- A single, cleaned Excel file containing:
  - ✅ `B2B` (Merged from all relevant sheets)
  - ✅ `IMPG` (If available)
  - ✅ `EXPORT` (If available)
- The **B2B sheet is cleaned** (for GSTR-2A only) to remove rows with missing key fields.

---

## 🧰 Tech Stack

- 🐍 Python 3.x  
- 📊 Pandas  
- ⚙️ OpenPyXL  
- 🌐 Streamlit

---

## 💻 How to Run Locally

```bash
# Step 1: Clone the repository
git clone https://github.com/your-username/gstr-file-merger.git
cd gstr-file-merger

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run the Streamlit app
streamlit run app.py
