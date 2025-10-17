import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image

def extract_greeks(image):
    # Convert PIL image to OpenCV format
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # Convert to grayscale and apply threshold for better OCR
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Extract text using OCR
    text = pytesseract.image_to_string(thresh).lower()
    greeks = {}
    lines = text.split('\n')
    for line in lines:
        parts = line.split()
        if not parts:
            continue
        last_part = parts[-1]
        if 'delta' in line and last_part.replace('.', '').replace('-', '').isdigit():
            greeks['delta'] = float(last_part)
        elif 'gamma' in line and last_part.replace('.', '').replace('-', '').isdigit():
            greeks['gamma'] = float(last_part)
        elif 'rho' in line and last_part.replace('.', '').replace('-', '').isdigit():
            greeks['rho'] = float(last_part)
        elif 'theta' in line and last_part.replace('.', '').replace('-', '').isdigit():
            greeks['theta'] = float(last_part)
        elif 'vega' in line and last_part.replace('.', '').replace('-', '').isdigit():
            greeks['vega'] = float(last_part)
        elif 'impvol' in line and last_part.replace('.', '').replace('-', '').isdigit():
            greeks['impvol'] = float(last_part)
    return greeks

def should_buy_option(greeks):
    if (greeks.get('delta', 0) > 0.3 and 
        greeks.get('theta', 0) > -0.5 and 
        greeks.get('vega', 0) > 0.2):
        return "Yes, consider buying this option. Positive Delta, manageable Theta decay, and good Vega suggest potential profit."
    else:
        return "No, avoid buying this option. The Greek values suggest high risk or low profitability."

def op_function():
    st.write("Choose an input method for Option Greeks:")
    
    # Option 1: Upload Image
    uploaded_file = st.file_uploader("Drag and drop an image or upload one containing Greek values", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        greeks = extract_greeks(image)
        st.write("Extracted Greeks (from image):", greeks)
        if greeks:
            recommendation = should_buy_option(greeks)
            st.write(recommendation)
        else:
            st.write("No valid Greek values extracted. Please try a clearer image or use manual input.")
    
    # Option 2: Manual Input
    st.write("OR enter Greek values manually:")
    col1, col2, col3 = st.columns(3)
    with col1:
        delta = st.number_input("Delta", value=0.0, step=0.01)
        gamma = st.number_input("Gamma", value=0.0, step=0.001)
    with col2:
        rho = st.number_input("Rho", value=0.0, step=0.01)
        theta = st.number_input("Theta", value=0.0, step=0.01)
    with col3:
        vega = st.number_input("Vega", value=0.0, step=0.01)
        impvol = st.number_input("Impvol", value=0.0, step=0.01)
    
    if st.button("Analyze Manual Input"):
        manual_greeks = {'delta': delta, 'gamma': gamma, 'rho': rho, 'theta': theta, 'vega': vega, 'impvol': impvol}
        st.write("Entered Greeks:", manual_greeks)
        recommendation = should_buy_option(manual_greeks)
        st.write(recommendation)