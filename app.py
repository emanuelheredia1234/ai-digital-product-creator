import os
from datetime import datetime

import openai
import streamlit as st

# ── 1. Set your OpenAI key ──────────────────────
openai.api_key = os.getenv("OPENAI_API_KEY")

# ── 2. Streamlit UI ───────────────────────────
st.set_page_config(page_title="AI Digital Product Creator", page_icon="🛍️")
st.title("🛍️ AI Digital Product Creator")
st.markdown(
    "Generate ready‑to‑sell digital products in seconds. "
    "Set your **OPENAI_API_KEY** as an environment variable before running."
)

product_type = st.selectbox(
    "Choose a product type",
    ["eBook", "Digital Planner", "Printable Art", "Social‑Media Templates"],
)

title = st.text_input("Theme / Title of your product", "")

if st.button("✨ Generate Product"):
    if not title.strip():
        st.warning("Please enter a title or theme.")
        st.stop()

    with st.spinner("Generating… this may take a moment"):
        # ── 3. Prompt engineering ──────────────────────
        prompt = (
            f"You are an expert digital‑product creator. "
            f"Create a complete {product_type} titled '{title}'. "
            f"Include all necessary sections, detailed content, and clear structure. "
            f"For any graphics, describe what should be illustrated."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
        )

        content = response.choices[0].message.content

    # ── 4. Save & offer download ──────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{product_type.replace(' ', '_')}_{timestamp}.txt"

    st.success("Product generated!")
    st.download_button(
        label="⬇️ Download your product",
        data=content,
        file_name=filename,
        mime="text/plain",
    )
    st.text_area("Preview", value=content, height=400)
