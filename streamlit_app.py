import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO

# Function to generate a transparent QR code
def generate_qr_code(data, box_size=10, border=4):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Make the QR code transparent
    qr_img = qr.make_image(fill_color="black", back_color="transparent").convert('RGBA')
    return qr_img

# Function to overlay QR code onto the background image
def overlay_qr_on_image(background_img, qr_img):
    # Resize the QR code to fit the background image (adjust as needed)
    qr_img = qr_img.resize((background_img.size[0] // 3, background_img.size[1] // 3))

    # Calculate position to place the QR code (center of the background image)
    position = (
        (background_img.size[0] - qr_img.size[0]) // 2,
        (background_img.size[1] - qr_img.size[1]) // 2
    )

    # Overlay the QR code onto the background image
    background_img.paste(qr_img, position, qr_img)

    return background_img

# Streamlit app
st.title('Custom QR Code Generator with Background Image')

# Input for QR code data (e.g., link)
qr_data = st.text_input('Enter the URL or text for the QR code:', 'https://example.com')

# Upload the background image
uploaded_image = st.file_uploader("Upload a background image", type=["png", "jpg", "jpeg"])

# Set QR code options
box_size = st.slider('QR Code Box Size', min_value=5, max_value=20, value=10)
border_size = st.slider('QR Code Border Size', min_value=1, max_value=10, value=4)

# Generate QR code when button is clicked
if st.button('Generate QR Code') and qr_data and uploaded_image:
    # Open the background image
    background_img = Image.open(uploaded_image).convert("RGBA")

    # Generate transparent QR code
    qr_img = generate_qr_code(qr_data, box_size, border_size)

    # Overlay QR code onto the background image
    final_image = overlay_qr_on_image(background_img, qr_img)

    # Display the final image with QR code
    st.image(final_image)

    # Prepare the image for download
    buf = BytesIO()
    final_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # Download button
    st.download_button(
        label="Download QR Code with Background",
        data=byte_im,
        file_name="custom_qr_with_background.png",
        mime="image/png"
    )
