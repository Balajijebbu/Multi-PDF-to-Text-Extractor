import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="Multi PDF to Text Extractor", layout="centered")

st.title("📄 Multi PDF to Text Extractor")
st.markdown("Upload one or more PDF files to extract and download their text.")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"📘 {uploaded_file.name}")
        
        try:
            # Read and extract text
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            
            if text.strip():
                # Show preview and download button
                st.success(f"✅ Extracted text from {uploaded_file.name}")
                st.text_area("Preview", text, height=200, key=uploaded_file.name)

                txt_file = io.BytesIO(text.encode("utf-8"))
                st.download_button(
                    label="⬇ Download .txt file",
                    data=txt_file,
                    file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.txt",
                    mime="text/plain",
                    key=f"download_{uploaded_file.name}"
                )
            else:
                st.warning("⚠️ No extractable text found in this file.")
        except Exception as e:
            st.error(f"❌ Failed to process {uploaded_file.name}: {e}")
