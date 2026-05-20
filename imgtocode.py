import streamlit as st
import base64
from PIL import Image
import io
import json

# Page Configuration
st.set_page_config(page_title="Image to Base64 Converter", page_icon="🖼️", layout="centered")

st.title("🖼️ Image to Base64 Encoder")
st.write("Apni image upload kijiye aur turant HTML `<img />` tag ya JSON format copy kijiye.")

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
    
    # 4. HTML Img Tag taiyar karna (Aapki inline styling ke sath)
    img_tag = f'<img src="data:image/{file_extension};base64,{base64_encoded}" style="max-width:340px;width:100%;height:auto;display:block;margin:8px auto;border-radius:2px" />'
    
    # 5. JSON Format taiyar karna ("question" key ke sath)
    json_data = {"question": img_tag}
    json_output = json.dumps(json_data, ensure_ascii=False)
    
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
        
        # 1. JSON Output (Jo aapko exact chahiye tha)
        st.write("**JSON Format:**")
        st.code(json_output, language="json")
        
        # 2. HTML Img Tag Code Block
        st.write("**HTML `<img />` Tag:**")
        st.code(img_tag, language="html")
        
        # 3. Raw Base64 Code Block
        st.write("**Pure Base64 String:**")
        st.code(base64_encoded, language="plaintext")

    st.success("🎉 Conversion Successful!")
