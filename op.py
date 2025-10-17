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
    option_type = "unknown"
    if lines and ('call' in lines[0].lower() or 'put' in lines[0].lower()):
        option_type = "call" if 'call' in lines[0].lower() else "put"
        lines = lines[1:]  # Remove the first line after identifying option type
    for line in lines:
        match = re.match(r'(\w+)\s+(-?\d+\.\d+)', line)
        if match:
            greek, value = match.groups()
            if greek.lower() in ['delta', 'gamma', 'rho', 'theta', 'vega', 'impvol']:
                greeks[greek.lower()] = float(value)
    return greeks, option_type

def analyze_option(greeks, option_type):
    if option_type == "call":
        recommendation = ""
        if (greeks.get('delta', 0) > 0.3 and greeks.get('theta', 0) > -0.5 and 
            greeks.get('vega', 0) > 0.2 and greeks.get('rho', 0) > 0.1):
            recommendation = "Consider buying this Call option. Positive Delta, manageable Theta decay, good Vega, and positive Rho suggest potential profit."
        else:
            recommendation = "Avoid buying this Call option. The Greek values (Delta, Theta, Vega, or Rho) indicate high risk or low profitability."
    elif option_type == "put":
        recommendation = ""
        if (greeks.get('delta', 0) < -0.3 and greeks.get('theta', 0) > -0.5 and 
            greeks.get('vega', 0) > 0.2 and greeks.get('rho', 0) < -0.1):
            recommendation = "Consider buying this Put option. Negative Delta, manageable Theta decay, good Vega, and negative Rho suggest potential profit."
        else:
            recommendation = "Avoid buying this Put option. The Greek values (Delta, Theta, Vega, or Rho) indicate high risk or low profitability."
    else:
        recommendation = "Option type not recognized. Please specify 'Call' or 'Put' in the first line."
    return recommendation

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
            call_rec = analyze_option(greeks, "call")  # Assume Call for image input
            put_rec = analyze_option(greeks, "put")    # Assume Put for image input
            st.write("Call Option Recommendation:", call_rec)
            st.write("Put Option Recommendation:", put_rec)
        else:
            st.write("No valid Greek values extracted. Please try a clearer image or use manual input.")
    
    # Option 2: Text Area Input
    st.write("OR paste Greek values manually in the format (e.g., 'Call (NDX ...)\nDelta 0.84474\n...'):")
    text_input = st.text_area("Enter Greek values", height=200, 
                             placeholder="Call (NDX 251017C22200000)\nDelta 0.84474\nGamma 0.00009\nRho 0.49179\nTheta -327.44135\nVega 3.06273\nImpvol 2.10361")
    
    if st.button("Analyze Text Input"):
        if text_input:
            greeks, option_type = parse_text_greeks(text_input)
            st.write(f"Option Type: {option_type.capitalize()}")
            st.write("Parsed Greeks:", greeks)
            if greeks:
                recommendation = analyze_option(greeks, option_type)
                st.write(f"{option_type.capitalize()} Option Recommendation:", recommendation)
            else:
                st.write("No valid Greek values parsed. Please check the format.")
        else:
            st.write("Please enter Greek values in the text area.")

    # Suggestions
    st.write("### Suggestions")
    st.write("1. Monitor Delta: > 0.3 (Call) or < -0.3 (Put) indicates strong directional movement.")
    st.write("2. Watch Theta: > -0.5 suggests slower time decay.")
    st.write("3. Use Vega: > 0.2 is favorable in volatile markets.")
    st.write("4. Check Rho: > 0.1 (Call) or < -0.1 (Put) aligns with interest rate trends.")
    st.write("5. Cross-check Impvol: < 0.7 might signal undervaluation.")

    # Table of Perfect Ranges for Call/Put Options with Color Bars
    st.write("### Perfect Range Analysis")
    data = {
        "Greek": ["Delta", "Theta", "Vega", "Rho", "Impvol"],
        "Perfect Range (Call)": ["> 0.3", "> -0.5", "> 0.2", "> 0.1", "< 0.7"],
        "Perfect Range (Put)": ["< -0.3", "> -0.5", "> 0.2", "< -0.1", "< 0.7"],
        "Value": [0.0000, 0.0000, 0.0000, 0.0000, 0.0000]  # Placeholder
    }
    df = pd.DataFrame(data)

    # Update values if text input is analyzed or image is processed
    if 'greeks' in locals() and greeks:
        df.loc[df["Greek"] == "Delta", "Value"] = greeks.get('delta', 0.0000)
        df.loc[df["Greek"] == "Theta", "Value"] = greeks.get('theta', 0.0000)
        df.loc[df["Greek"] == "Vega", "Value"] = greeks.get('vega', 0.0000)
        df.loc[df["Greek"] == "Rho", "Value"] = greeks.get('rho', 0.0000)
        df.loc[df["Greek"] == "Impvol", "Value"] = greeks.get('impvol', 0.0000)

    # Define color conditions for bars based on option type
    def get_bar_color(value, greek, option_type):
        if option_type == "call":
            if greek == "Delta" and value > 0.3:
                return "green"
            elif greek == "Theta" and value > -0.5:
                return "green"
            elif greek == "Vega" and value > 0.2:
                return "green"
            elif greek == "Rho" and value > 0.1:
                return "green"
            elif greek == "Impvol" and value < 0.7:
                return "green"
            elif (greek == "Delta" and 0.2 <= value <= 0.3) or (greek == "Theta" and -0.7 <= value <= -0.5) or \
                 (greek == "Vega" and 0.1 <= value <= 0.2) or (greek == "Rho" and 0.0 <= value <= 0.1) or \
                 (greek == "Impvol" and 0.7 <= value <= 0.9):
                return "orange"
            else:
                return "red"
        elif option_type == "put":
            if greek == "Delta" and value < -0.3:
                return "green"
            elif greek == "Theta" and value > -0.5:
                return "green"
            elif greek == "Vega" and value > 0.2:
                return "green"
            elif greek == "Rho" and value < -0.1:
                return "green"
            elif greek == "Impvol" and value < 0.7:
                return "green"
            elif (greek == "Delta" and -0.3 <= value <= -0.2) or (greek == "Theta" and -0.7 <= value <= -0.5) or \
                 (greek == "Vega" and 0.1 <= value <= 0.2) or (greek == "Rho" and -0.1 <= value <= 0.0) or \
                 (greek == "Impvol" and 0.7 <= value <= 0.9):
                return "orange"
            else:
                return "red"
        else:
            return "gray"  # Neutral if option type is unknown

    # Add colored bars to the table based on the detected option type
    option_type = "unknown" if 'option_type' not in locals() else option_type
    df["Bar"] = df.apply(lambda row: f'<span style="display:inline-block; width: 100px; height: 20px; background-color: {get_bar_color(row["Value"], row["Greek"], option_type)};"></span>', axis=1)
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)