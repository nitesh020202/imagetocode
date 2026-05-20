import streamlit as st
import base64
from PIL import Image
import io
import json

# Page Configuration
st.set_page_config(page_title="Image to Base64 Converter", page_icon="🖼️", layout="centered")

st.title("🖼️ Image to Base64 Encoder")
st.write("Apni image upload kijiye aur JSON ya HTML ke liye ready-made code copy kijiye.")

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
    
    # 4. HTML Img Tag taiyar karna (With inline styling)
    img_tag = f'<img src="data:image/{file_extension};base64,{base64_encoded}" style="max-width:340px;width:100%;height:auto;display:block;margin:8px auto;border-radius:2px" />'
    
    # 5. JSON ke andar PASTE karne ke liye string (Quotes ko escape kiya gaya hai)
    # Isko aap direct JSON ke "" ke beech mein paste kar sakte hain
    escaped_string = img_tag.replace('"', '\\"')
    
    # 6. Poora ready-made JSON block
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
            st.markdown(img_tag, unsafe_allow_html=True)

    with col2:
        st.subheader("Outputs")
        
        # A. SABSE ZAROORI: JSON Ke Beech Mein Paste Karne Ke Liye
        st.write("🎯 **JSON ke `\"\"` ke andar paste karne ke liye isko copy karein:**")
        st.code(escaped_string, language="plaintext")
        
        st.divider() # Ek line separation ke liye
        
        # B. Poora Ready JSON Block
        st.write("**Poora Ready JSON Block:**")
        st.code(json_output, language="json")
        
        # C. Pure HTML Img Tag
        st.write("**Normal HTML `<img />` Tag:**")
        st.code(img_tag, language="html")

    st.success("🎉 Code taiyar hai! Upar wale pahle box se copy kijiye.")
