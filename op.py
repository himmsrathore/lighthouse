import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image
import pandas as pd
import re

def extract_greeks(image):
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    text = pytesseract.image_to_string(thresh).lower()
    st.write("Extracted Text (Debug):", text)  # Debugging output
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

def parse_text_greeks(text):
    greeks = {}
    lines = text.strip().split('\n')
    for line in lines:
        match = re.match(r'(\w+)\s+(-?\d+\.\d+)', line)
        if match:
            greek, value = match.groups()
            if greek.lower() in ['delta', 'gamma', 'rho', 'theta', 'vega', 'impvol']:
                greeks[greek.lower()] = float(value)
    return greeks

def analyze_option(greeks):
    call_recommendation = ""
    if (greeks.get('delta', 0) > 0.3 and greeks.get('theta', 0) > -0.5 and greeks.get('vega', 0) > 0.2):
        call_recommendation = "Consider buying a Call option. Positive Delta, manageable Theta decay, and good Vega suggest potential profit."
    else:
        call_recommendation = "Avoid buying a Call option. The Greek values indicate high risk or low profitability."

    put_recommendation = ""
    if (greeks.get('delta', 0) < -0.3 and greeks.get('theta', 0) > -0.5 and greeks.get('vega', 0) > 0.2):
        put_recommendation = "Consider buying a Put option. Negative Delta, manageable Theta decay, and good Vega suggest potential profit."
    else:
        put_recommendation = "Avoid buying a Put option. The Greek values indicate high risk or low profitability."

    return call_recommendation, put_recommendation

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
            call_rec, put_rec = analyze_option(greeks)
            st.write("Call Option Recommendation:", call_rec)
            st.write("Put Option Recommendation:", put_rec)
        else:
            st.write("No valid Greek values extracted. Please try a clearer image or use manual input.")
    
    # Option 2: Text Area Input
    st.write("OR paste Greek values manually in the format (e.g., 'Delta 0.75502\nGamma 0.00663\n...'):")
    text_input = st.text_area("Enter Greek values", height=200)
    
    if st.button("Analyze Text Input"):
        if text_input:
            greeks = parse_text_greeks(text_input)
            st.write("Parsed Greeks:", greeks)
            if greeks:
                call_rec, put_rec = analyze_option(greeks)
                st.write("Call Option Recommendation:", call_rec)
                st.write("Put Option Recommendation:", put_rec)
            else:
                st.write("No valid Greek values parsed. Please check the format.")
        else:
            st.write("Please enter Greek values in the text area.")

    # Suggestions
    st.write("### Suggestions")
    st.write("1. Monitor Delta closely: A Delta above 0.3 indicates strong upward movement for Calls.")
    st.write("2. Watch Theta: Values closer to 0 or slightly negative (-0.5 or better) suggest slower time decay.")
    st.write("3. Use Vega to assess volatility: Higher Vega (above 0.2) is favorable in volatile markets.")
    st.write("4. Cross-check with Impvol: Low implied volatility (< 0.7) might signal undervaluation.")

    # Table of Perfect Ranges for Call Options with Color Bars
    st.write("### Perfect Range Analysis for Call Options")
    data = {
        "Greek": ["Delta", "Theta", "Vega", "Impvol"],
        "Perfect Range": ["> 0.3", "> -0.5", "> 0.2", "< 0.7"],
        "Value": [0.0000, 0.0000, 0.0000, 0.0000]  # Placeholder, will be updated with input if available
    }
    df = pd.DataFrame(data)

    # Update values if text input is analyzed or image is processed
    if 'greeks' in locals() and greeks:
        df.loc[df["Greek"] == "Delta", "Value"] = greeks.get('delta', 0.0000)
        df.loc[df["Greek"] == "Theta", "Value"] = greeks.get('theta', 0.0000)
        df.loc[df["Greek"] == "Vega", "Value"] = greeks.get('vega', 0.0000)
        df.loc[df["Greek"] == "Impvol", "Value"] = greeks.get('impvol', 0.0000)
    elif 'greeks' in locals() and text_input:
        df.loc[df["Greek"] == "Delta", "Value"] = greeks.get('delta', 0.0000)
        df.loc[df["Greek"] == "Theta", "Value"] = greeks.get('theta', 0.0000)
        df.loc[df["Greek"] == "Vega", "Value"] = greeks.get('vega', 0.0000)
        df.loc[df["Greek"] == "Impvol", "Value"] = greeks.get('impvol', 0.0000)

    # Define color conditions for bars
    def get_bar_color(value, greek):
        if greek == "Delta" and value > 0.3:
            return "green"
        elif greek == "Theta" and value > -0.5:
            return "green"
        elif greek == "Vega" and value > 0.2:
            return "green"
        elif greek == "Impvol" and value < 0.7:
            return "green"
        elif (greek == "Delta" and 0.2 <= value <= 0.3) or (greek == "Theta" and -0.7 <= value <= -0.5) or \
             (greek == "Vega" and 0.1 <= value <= 0.2) or (greek == "Impvol" and 0.7 <= value <= 0.9):
            return "orange"
        else:
            return "red"

    # Add colored bars to the table
    df["Bar"] = df.apply(lambda row: f'<span style="display:inline-block; width: 100px; height: 20px; background-color: {get_bar_color(row["Value"], row["Greek"])};"></span>', axis=1)
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)