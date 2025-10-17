import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image

# Set the path to tesseract executable (update based on your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows example

def extract_greeks(image):
    # Convert PIL image to OpenCV format
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # Convert to grayscale and apply threshold for better OCR
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Extract text using OCR
    text = pytesseract.image_to_string(thresh).lower()
    
    # Parse the text to find Greek values (simplified parsing)
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
    # Simple decision logic based on Greek values
    # Example: Buy if Delta > 0.3, Theta > -0.5, and Vega > 0.2
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
        # Convert uploaded file to PIL image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Extract Greek values
        greeks = extract_greeks(image)
        st.write("Extracted Greeks:", greeks)
        
        # Decision based on Greeks
        recommendation = should_buy_option(greeks)
        st.write(recommendation)