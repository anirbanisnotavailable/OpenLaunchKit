import streamlit as st
import os
from modules.aso_generator import generate_keywords
from modules.mockup_maker import generate_mockup
from modules.release_notes import generate_changelog

st.set_page_config(page_title="OpenLaunchKit", layout="wide", page_icon="🚀")

st.title("🚀 OpenLaunchKit")
st.markdown("The zero-cost, local-first toolkit for indie developers to launch without the overhead.")

# Configuration utilities
st.sidebar.header("⚙️ Engine Control")
gemini_key = st.sidebar.text_input("Gemini API Key (Optional Override)", type="password", placeholder="Paste cloud key here...")
st.sidebar.markdown("[Get a lifetime free-tier key here ↗](https://aistudio.google.com/)")

tab1, tab2, tab3 = st.tabs(["App Store Optimization", "Mockup Generator", "Git Release Notes"])

with tab1:
    st.header("ASO & Keyword Extractor")
    st.markdown("Optimize listings instantly using native local text processing or intelligent AI hooks.")
    
    app_desc = st.text_area("App Core Mechanics / Competitor Descriptions", height=180, placeholder="Type layout structure here...")
    
    if st.button("Extract Production Metadata"):
        if app_desc:
            with st.spinner("Analyzing text distributions..."):
                keywords, engine_used = generate_keywords(app_desc, gemini_key=gemini_key)
                st.info(f"Active Processing Unit: **{engine_used}**")
                st.markdown(keywords)
        else:
            st.warning("Please supply descriptive target reference text.")

with tab2:
    st.header("Mockup Canvas Tool")
    st.markdown("Instantly turn raw viewport snaps into polished promotional layouts.")
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Select Viewport File Source", type=["png", "jpg", "jpeg"])
        banner_text = st.text_input("Marketing Action Text Headline", value="Design Better Software Faster")
        bg_color = st.color_picker("Choose Background Palette Accent Color", "#4F46E5")
        
    with col2:
        if uploaded_file:
            output_file = os.path.join("output", "promo_mockup.png")
            generate_mockup(uploaded_file, banner_text, bg_color, output_file)
            st.success("Asset configuration rendered successfully.")
            st.image(output_file, caption="Export Preview Asset", use_container_width=True)

with tab3:
    st.header("Automated Release Notes")
    st.markdown("Translate technical Git commits into user-friendly changelogs.")
    repo_path = st.text_input("Local Git Repository Path", value="./")
    
    if st.button("Generate Changelog"):
        with st.spinner("Parsing commits..."):
            notes = generate_changelog(repo_path)
            st.markdown(notes)
