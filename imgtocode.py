import streamlit as st
import base64
from PIL import Image
import io

# Page Configuration
st.set_page_config(page_title="Image to Base64 Converter", page_icon="🖼️", layout="centered")

st.title("🖼️ Image to Base64 Encoder")
st.write("Apni image upload kijiye aur turant HTML `<img />` tag ya pure Base64 string copy kijiye.")

# File Uploader (Supports PNG, JPG, JPEG, SVG, WebP)
uploaded_file = st.file_uploader("Image select kijiye...", type=["png", "jpg", "jpeg", "svg", "webp"])

if uploaded_file is not None:
    # 1. Image ko bytes mein read karna
    bytes_data = uploaded_file.getvalue()
    
    # 2. File type/extension nikalna
    file_extension = uploaded_file.name.split(".")[-1].lower()
    if file_extension == "jpg":
        file_extension = "jpeg"  # HTML mime-type ke liye jpeg zaroori hai
        
    # 3. Base64 encode karna
    base64_encoded = base64.b64encode(bytes_data).decode("utf-8")
    
    # 4. HTML Img Tag taiyar karna
    img_tag = f'<img src="data:image/{file_extension};base64,{base64_encoded}" alt="{uploaded_file.name}" />'
    
    # Layout divisions for preview and output
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Preview")
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        except Exception:
            # SVG files PIL se direct open nahi hotin, unhe HTML se preview karenge
            st.markdown(img_tag, unsafe_allow_html=True)

    with col2:
        st.subheader("Outputs")
        
        # HTML Img Tag Code Block (Copy karne ke liye)
        st.write("**HTML `<img />` Tag:**")
        st.code(img_tag, language="html")
        
        # Raw Base64 Code Block
        st.write("**Pure Base64 String:**")
        st.code(base64_encoded, language="plaintext")

    st.success("🎉 Conversion Successful!")