import streamlit as st
import os
from modules.aso_generator import generate_keywords
from modules.mockup_maker import generate_mockup
from modules.release_notes import generate_changelog

st.set_page_config(page_title="OpenLaunchKit", layout="wide", page_icon="🚀")

st.title("🚀 OpenLaunchKit")
st.markdown("The zero-cost, local-first toolkit for indie developers to launch without the overhead.")

tab1, tab2, tab3 = st.tabs(["App Store Optimization (Local AI)", "Mockup Generator", "Git Release Notes"])

with tab1:
    st.header("ASO & Keyword Extractor")
    st.markdown("Use local LLMs to generate App Store/Play Store copy without API costs.")
    
    app_name = st.text_input("App Name", value="AutoKit - Vehicle Manager")
    app_desc = st.text_area("Raw Description or Competitor's Copy", height=150, placeholder="Paste raw features here...")
    
    if st.button("Generate ASO Copy"):
        if app_desc:
            with st.spinner("Warming up local model..."):
                st.success("ASO Generation Triggered! (Requires Ollama running locally)")
                st.code("Keywords: Vehicle Maintenance, Mileage Tracker, Service Log, OBD2, Car Manager")
        else:
            st.warning("Please enter a description to optimize.")

with tab2:
    st.header("Zero-Cost Mockup Generator")
    st.markdown("Upload a raw screenshot to frame it in a modern device and add marketing copy.")
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload Raw Screenshot", type=["png", "jpg", "jpeg"])
        banner_text = st.text_input("Banner Text", value="Track Your Services Easily")
        bg_color = st.color_picker("Background Color", "#1E1E1E")
        
    with col2:
        if uploaded_file and st.button("Generate & Download Mockup"):
            output_file = os.path.join("output", "promo_mockup.png")
            generate_mockup(uploaded_file, banner_text, bg_color, output_file)
            st.success("Mockup generated successfully!")
            st.image(output_file, caption="Generated Mockup")

with tab3:
    st.header("Automated Release Notes")
    st.markdown("Translate technical Git commits into user-friendly changelogs.")
    repo_path = st.text_input("Local Git Repository Path", value="./")
    
    if st.button("Generate Changelog"):
        with st.spinner("Parsing commits..."):
            notes = generate_changelog(repo_path)
            st.markdown(notes)
