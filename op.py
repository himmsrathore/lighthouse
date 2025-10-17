import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image

# Remove or comment out the following line
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_greeks(image):
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    text = pytesseract.image_to_string(thresh).lower()
    greeks = {}
    lines = text.split('\n')
    for line in lines:
        if 'delta' in line:
            greeks['delta'] = float(line.split()[-1])
        elif 'gamma' in line:
            greeks['gamma'] = float(line.split()[-1])
        elif 'rho' in line:
            greeks['rho'] = float(line.split()[-1])
        elif 'theta' in line:
            greeks['theta'] = float(line.split()[-1])
        elif 'vega' in line:
            greeks['vega'] = float(line.split()[-1])
        elif 'impvol' in line:
            greeks['impvol'] = float(line.split()[-1])
    return greeks

def should_buy_option(greeks):
    if (greeks.get('delta', 0) > 0.3 and 
        greeks.get('theta', 0) > -0.5 and 
        greeks.get('vega', 0) > 0.2):
        return "Yes, consider buying this option. Positive Delta, manageable Theta decay, and good Vega suggest potential profit."
    else:
        return "No, avoid buying this option. The Greek values suggest high risk or low profitability."

def op_function():
    st.write("Drag and drop an image or upload one containing Greek values.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        greeks = extract_greeks(image)
        st.write("Extracted Greeks:", greeks)
        recommendation = should_buy_option(greeks)
        st.write(recommendation)