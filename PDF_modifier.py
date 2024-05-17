import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image

def modify_pdf(file, text_to_add, page_num, x, y, image_file=None, img_x=None, img_y=None):
    # Open PDF file in memory
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    
    # Check if page exists
    if page_num < 0 or page_num >= len(pdf_document):
        st.error("Page number out of range")
        return None
    
    # Get the specific page
    page = pdf_document.load_page(page_num)
    
    # Add text in specified coordinates
    if text_to_add:
        page.insert_text((x, y), text_to_add, fontsize=12, color=(0, 0, 0))
    
    # Add image in specified coordinates
    if image_file and img_x is not None and img_y is not None:
        img = Image.open(image_file)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        rect = fitz.Rect(img_x, img_y, img_x + img.width, img_y + img.height)
        page.insert_image(rect, stream=img_byte_arr)
    
    # Save the modified PDF to a byte object
    output_stream = io.BytesIO()
    pdf_document.save(output_stream)
    pdf_document.close()
    
    output_stream.seek(0)
    return output_stream

st.title("PDF Modifier")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
text_to_add = st.text_input("Text to add")
page_num = st.number_input("Page number", min_value=0, step=1)
x_coord = st.number_input("X coordinate for text", min_value=0, step=1)
y_coord = st.number_input("Y coordinate for text", min_value=0, step=1)

image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
img_x_coord = st.number_input("X coordinate for the image", min_value=0, step=1)
img_y_coord = st.number_input("Y coordinate for the image", min_value=0, step=1)

if uploaded_file:
    modified_pdf = modify_pdf(
        uploaded_file, 
        text_to_add, 
        page_num, 
        x_coord, 
        y_coord, 
        image_file, 
        img_x_coord, 
        img_y_coord
    )
    if modified_pdf:
        st.download_button(
            label="Download Modified PDF",
            data=modified_pdf,
            file_name="modified_pdf.pdf",
            mime="application/pdf"
        )
