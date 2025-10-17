import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image
import pandas as pd

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
    
    # Option 2: Manual Input
    st.write("OR enter Greek values manually:")
    col1, col2, col3 = st.columns(3)
    with col1:
        delta = st.number_input("Delta", value=0.0000, step=0.0001, format="%.4f")
        gamma = st.number_input("Gamma", value=0.0000, step=0.0001, format="%.4f")
    with col2:
        rho = st.number_input("Rho", value=0.0000, step=0.0001, format="%.4f")
        theta = st.number_input("Theta", value=0.0000, step=0.0001, format="%.4f")
    with col3:
        vega = st.number_input("Vega", value=0.0000, step=0.0001, format="%.4f")
        impvol = st.number_input("Impvol", value=0.0000, step=0.0001, format="%.4f")
    
    if st.button("Analyze Manual Input"):
        manual_greeks = {'delta': delta, 'gamma': gamma, 'rho': rho, 'theta': theta, 'vega': vega, 'impvol': impvol}
        st.write("Entered Greeks:", manual_greeks)
        call_rec, put_rec = analyze_option(manual_greeks)
        st.write("Call Option Recommendation:", call_rec)
        st.write("Put Option Recommendation:", put_rec)

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

    # Update values if manual input is analyzed
    if 'manual_greeks' in locals():
        df.loc[df["Greek"] == "Delta", "Value"] = manual_greeks.get('delta', 0.0000)
        df.loc[df["Greek"] == "Theta", "Value"] = manual_greeks.get('theta', 0.0000)
        df.loc[df["Greek"] == "Vega", "Value"] = manual_greeks.get('vega', 0.0000)
        df.loc[df["Greek"] == "Impvol", "Value"] = manual_greeks.get('impvol', 0.0000)
    elif greeks:  # Update with extracted values if image is processed
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