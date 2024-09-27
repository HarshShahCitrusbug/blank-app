import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO

# Function to generate a basic QR code without blending
def generate_qr_code(data, box_size=10, border=4):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    return qr_img

# Function to pixelate the background image
def pixelate_image(image, pixel_size=10):
    # Resize down and then resize back up to create a pixelated effect
    image_small = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        resample=Image.NEAREST
    )
    return image_small.resize(image.size, Image.NEAREST)

# Function to blend pixelated background with QR code
def blend_qr_with_background(qr_img, background_img, blend_alpha=0.6):
    # Resize the QR code to match the background size
    qr_img = qr_img.resize(background_img.size)

    # Blend the QR code and the background
    blended = Image.blend(background_img, qr_img, alpha=blend_alpha)
    
    return blended

# Streamlit app
st.title('Advanced QR Code Generator with Pixelated Background')

# Input for QR code data (e.g., link)
qr_data = st.text_input('Enter the URL or text for the QR code:', 'https://example.com')

# Upload the background image
uploaded_image = st.file_uploader("Upload a background image", type=["png", "jpg", "jpeg"])

# Set QR code options
box_size = st.slider('QR Code Box Size', min_value=5, max_value=20, value=10)
border_size = st.slider('QR Code Border Size', min_value=1, max_value=10, value=4)

# Set pixelation options
pixel_size = st.slider('Pixelation Level (lower is more pixelated)', min_value=5, max_value=50, value=10)

# Set blending options
blend_alpha = st.slider('QR Code Blending Alpha (0 = full image, 1 = full QR code)', min_value=0.0, max_value=1.0, value=0.6)

# Generate QR code when button is clicked
if st.button('Generate QR Code') and qr_data and uploaded_image:
    # Open the background image
    background_img = Image.open(uploaded_image).convert("RGBA")

    # Pixelate the background image
    pixelated_background = pixelate_image(background_img, pixel_size)

    # Generate QR code
    qr_img = generate_qr_code(qr_data, box_size, border_size)

    # Blend the pixelated background with the QR code
    final_image = blend_qr_with_background(qr_img, pixelated_background, blend_alpha)

    # Display the final image with QR code
    st.image(final_image)

    # Prepare the image for download
    buf = BytesIO()
    final_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # Download button
    st.download_button(
        label="Download QR Code with Pixelated Background",
        data=byte_im,
        file_name="pixelated_qr_code.png",
        mime="image/png"
    )
