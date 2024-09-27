import streamlit as st
import qrcode
from PIL import Image, ImageDraw
import cv2
import numpy as np

# Function to generate a QR code
def generate_qr_code(data, fill_color="black", back_color="white"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')
    return qr_img

# Function to blend image into the QR code matrix
def blend_image_with_qr(qr_img, user_img):
    qr_img = qr_img.convert("RGBA")
    user_img = user_img.convert("RGBA")

    # Resize user image to fit into the QR code
    user_img = user_img.resize(qr_img.size)

    # Blend the images together (adjust the alpha for balance)
    blended = Image.blend(qr_img, user_img, alpha=0.4)
    return blended

# Streamlit app
st.title("Custom QR Code with Integrated Image")

# Input for QR code data
qr_data = st.text_input("Enter the URL or text for the QR code:", "https://example.com")

# Upload image
uploaded_image = st.file_uploader("Upload an image to integrate", type=["png", "jpg", "jpeg"])

# Set colors
fill_color = st.color_picker("QR Code Color", "#000000")
back_color = st.color_picker("Background Color", "#FFFFFF")

# Generate QR code when data and image are provided
if st.button("Generate QR Code") and qr_data and uploaded_image:
    # Generate the QR code
    qr_img = generate_qr_code(qr_data, fill_color=fill_color, back_color=back_color)
    
    # Open the uploaded image
    user_img = Image.open(uploaded_image)

    # Blend the image with the QR code
    final_qr = blend_image_with_qr(qr_img, user_img)

    # Display the QR code with integrated image
    st.image(final_qr, caption="QR Code with Integrated Image")

    # Provide download option
    buf = BytesIO()
    final_qr.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download QR Code",
        data=byte_im,
        file_name="custom_qr_code.png",
        mime="image/png"
    )
