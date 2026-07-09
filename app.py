import streamlit as st
from deep_translator import GoogleTranslator
from datetime import datetime
from pathlib import Path

# ---------------- PAGE SETTINGS ---------------- #

st.set_page_config(
    page_title="AI Language Translation Tool",
    page_icon="🌍",
    layout="centered"
)

st.markdown("""
# 🌍 AI Language Translation Tool

### Translate text between **100+ languages** instantly.

Built using **Python • Streamlit • Google Translate API**
""")
st.markdown("""
<style>

/* Main App */
.stApp{
    background-color:#0E1117;
}

/* Buttons */
.stButton>button{
    border-radius:12px;
    height:50px;
    font-weight:bold;
    font-size:17px;
    width:100%;
}

/* Download Button */
.stDownloadButton>button{
    border-radius:12px;
    height:50px;
    font-weight:bold;
    width:100%;
}

/* Text Area */
textarea{
    border-radius:12px !important;
}

/* Success Box */
div[data-testid="stAlert"]{
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Main App */
.stApp{
    background-color:#0E1117;
}

/* Buttons */
.stButton>button{
    border-radius:12px;
    height:50px;
    font-weight:bold;
    font-size:17px;
    width:100%;
}

/* Download Button */
.stDownloadButton>button{
    border-radius:12px;
    height:50px;
    font-weight:bold;
    width:100%;
}

/* Text Area */
textarea{
    border-radius:12px !important;
}

/* Success Box */
div[data-testid="stAlert"]{
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LANGUAGES ---------------- #

languages = GoogleTranslator().get_supported_languages(as_dict=True)
language_names = ["auto"] + sorted(languages.keys())

# ---------------- HISTORY FILE ---------------- #

history_file = Path("history/translations.txt")
history_file.parent.mkdir(exist_ok=True)

# ---------------- SESSION STATE ---------------- #

if "source" not in st.session_state:
    st.session_state.source = "auto"

if "target" not in st.session_state:
    st.session_state.target = "hindi"

if "translated" not in st.session_state:
    st.session_state.translated = ""
# ---------------- INPUT ---------------- #

text = st.text_area(
    "📝 Enter text to translate",
    height=150,
    placeholder="Type something here..."
)

# ---------------- LANGUAGE SELECTORS ---------------- #

col1, col2 = st.columns([5, 1])

with col1:
    source = st.selectbox(
        "Source Language",
        language_names,
        index=language_names.index(st.session_state.source)
    )

with col2:
    st.write("")
    st.write("")
    if st.button("⇄", help="Swap Languages"):
        st.session_state.source, st.session_state.target = (
            st.session_state.target,
            st.session_state.source,
        )
        st.rerun()

target = st.selectbox(
    "Target Language",
    language_names,
    index=language_names.index(st.session_state.target)
)

st.session_state.source = source
st.session_state.target = target

st.divider()
# ---------------- TRANSLATE ---------------- #

if st.button("🚀 Translate", use_container_width=True):

    if text.strip() == "":
        st.warning("⚠ Please enter some text to translate.")
    else:
        try:
            translated = GoogleTranslator(
                source="auto" if source == "auto" else source,
                target=target
            ).translate(text)

            st.session_state.translated = translated

        except Exception as e:
            st.error(f"Translation failed: {e}")
# ---------------- OUTPUT ---------------- #

if st.session_state.translated:

    st.success("✅ Translation Completed!")

    st.text_area(
        "Translated Text",
        st.session_state.translated,
        height=150
    )

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "📥 Download Translation",
            data=st.session_state.translated,
            file_name="translation.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        if st.button("💾 Save to History", use_container_width=True):

            with open(history_file, "a", encoding="utf-8") as file:

                file.write(
                    f"""
----------------------------------------
Date : {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

Source : {source}
Target : {target}

Input :
{text}

Output :
{st.session_state.translated}

----------------------------------------

"""
                )

            st.success("Saved to history successfully! ✅")
            # ---------------- HISTORY ---------------- #

st.divider()

st.subheader("📜 Translation History")
col1, col2 = st.columns([4, 1])

with col2:
    if st.button("🗑️ Clear History"):
        history_file.write_text("", encoding="utf-8")
        st.success("History cleared successfully!")
        st.rerun()

if history_file.exists():

    history = history_file.read_text(encoding="utf-8")

    if history.strip():

        st.text_area(
            "Saved Translations",
            history,
            height=250
        )

    else:
        st.info("No translation history found.")

else:
    st.info("History file not found.")