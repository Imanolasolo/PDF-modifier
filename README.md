# PDF Modifier with Streamlit and PyMuPDF

This project is a Streamlit application that allows users to upload a PDF file, add text and images to specified coordinates on a specified page, and then download the modified PDF. It uses the PyMuPDF library to handle PDF modifications and Pillow for image processing.

## Features

- Upload a PDF file
- Add text to a specified page and coordinates
- Add an image to a specified page and coordinates
- Download the modified PDF

## Installation

To run this application, you need to have Python installed. Follow the steps below to set up and run the application.

### Prerequisites

- Python 3.6 or later
- Streamlit
- PyMuPDF (also known as `fitz`)
- Pillow

### Install required libraries

```sh
pip install streamlit pymupdf pillow
```

## Usage

1. Clone the repository or download the `app.py` file to your local machine.
2. Open a terminal and navigate to the directory containing the `app.py` file.
3. Run the following command to start the Streamlit application:
   ```sh
   streamlit run app.py
   ```
4. A new tab will open in your default web browser displaying the application.

### Application Interface

1. **Upload a PDF file**: Click on "Browse files" and select a PDF file from your local machine.
2. **Text to add**: Enter the text you want to add to the PDF.
3. **Page number**: Specify the page number where you want to add the text. Page numbers start from 0.
4. **X coordinate for text**: Specify the X coordinate for the text.
5. **Y coordinate for text**: Specify the Y coordinate for the text.
6. **Upload an image**: Click on "Browse files" and select an image file (PNG, JPG, JPEG) from your local machine.
7. **X coordinate for the image**: Specify the X coordinate for the image.
8. **Y coordinate for the image**: Specify the Y coordinate for the image.
9. **Download Modified PDF**: After making the necessary modifications, click on the "Download Modified PDF" button to download the updated PDF file.

## Code Overview

The main function `modify_pdf` takes in several parameters to handle the PDF modifications:

- `file`: The uploaded PDF file.
- `text_to_add`: The text to be added to the PDF.
- `page_num`: The page number where the text/image will be added.
- `x`, `y`: Coordinates for the text.
- `image_file`: The uploaded image file.
- `img_x`, `img_y`: Coordinates for the image.

The function opens the PDF file, checks if the specified page exists, and then adds the text and/or image to the specified coordinates. The modified PDF is saved to a byte stream, which is then used to generate a download link in the Streamlit interface.

## Example

Here's the complete code for the `app.py` file:

```python
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
```

## Contributing

Feel free to fork the repository, create a new branch, and submit a pull request if you have any improvements or feature additions. Contributions are always welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.