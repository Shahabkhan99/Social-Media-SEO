import streamlit as st
import json
import os
import google.generativeai as genai
from openai import OpenAI
from huggingface_hub import InferenceClient

# --- Configuration ---
PROFILE_FILE = "user_profiles.json"

# --- Data Management Functions ---
def load_data():
    """Loads all profiles from JSON."""
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_profile(name, platform, api_key):
    """Saves a specific profile to the JSON dictionary."""
    data = load_data()
    data[name] = {
        "platform": platform,
        "api_key": api_key
    }
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    return data

def get_profile_names():
    data = load_data()
    return list(data.keys())

# --- AI Generation Logic ---
def generate_seo_content(platform, social_media, description, api_key):
    system_prompt = f"""
    You are an expert Social Media Manager.
    Platform: {social_media}
    User Description: {description}
    
    Task: Create a high-performing post (95+ SEO score).
    
    REQUIRED OUTPUT FORMAT (Do not change headings):
    
    ### TITLE
    (Write the title here)
    
    ### DESCRIPTION
    (Write the description here minmum 2000 words)
    
    ### HASHTAGS
    (Write hashtags here)
    
    ### KEYWORDS
    (Write keywords here)
    """

    try:
        content = ""
        # --- GEMINI ---
        if platform == "Gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(system_prompt)
            content = response.text

        # --- CHATGPT ---
        elif platform == "ChatGPT":
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o", 
                messages=[{"role": "user", "content": system_prompt}]
            )
            content = response.choices[0].message.content
        
        # --- HUGGING FACE ---
        elif platform == "Hugging Face":
            client = InferenceClient(api_key=api_key)
            messages = [{"role": "user", "content": system_prompt}]
            response = client.chat_completion(
                model="Qwen/Qwen2.5-7B-Instruct", 
                messages=messages, 
                max_tokens=1000
            )
            content = response.choices[0].message.content

        return content

    except Exception as e:
        return f"Error: {str(e)}"

# --- Main App Interface ---
def main():
    # 1. FIXED: Changed layout to "centered" to prevent super-wide lines
    st.set_page_config(page_title="AI SEO Pro", page_icon="⚡", layout="centered")

    # 2. FIXED: Custom CSS to force text wrapping (makes boxes taller, not wider)
    st.markdown("""
    <style>
        /* Force text inside code blocks to wrap */
        code {
            white-space: pre-wrap !important;
            word-break: break-word !important;
        }
        /* Make the text area look cleaner */
        .stTextArea textarea {
            font-size: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Load all profiles
    profiles = get_profile_names()
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.header("👤 User Management")
        if profiles:
            selected_user = st.selectbox("Switch Profile", profiles)
            current_data = load_data()[selected_user]
            st.success(f"Active: {selected_user}")
        else:
            selected_user = None
            st.warning("No profiles found.")

        st.divider()
        if st.button("➕ Create New Profile"):
            st.session_state.page = "setup"
            st.rerun()
        
        if profiles and st.button("Go to Generator"):
            st.session_state.page = "generator"
            st.rerun()

    # Initialize Page State
    if "page" not in st.session_state:
        st.session_state.page = "setup" if not profiles else "generator"

    # --- PAGE 1: SETUP ---
    if st.session_state.page == "setup":
        st.title("🛠️ Profile Setup")
        with st.form("profile_form"):
            new_name = st.text_input("Profile Name (e.g., 'Personal', 'Client A')")
            new_platform = st.selectbox("AI Platform", ["Hugging Face", "Gemini", "ChatGPT"])
            new_key = st.text_input("API Key", type="password")
            
            if st.form_submit_button("Save Profile"):
                if new_name and new_key:
                    save_profile(new_name, new_platform, new_key)
                    st.success(f"Profile '{new_name}' saved!")
                    st.session_state.page = "generator"
                    st.rerun()
                else:
                    st.error("Missing name or key.")

    # --- PAGE 2: GENERATOR ---
    elif st.session_state.page == "generator":
        if not selected_user:
            st.error("Please create a profile first.")
            return

        st.title(f"🚀 Generator")
        st.caption(f"Generating for **{selected_user}** on **{current_data['platform']}**")
        
        # Stacked Inputs (Cleaner look)
        social = st.selectbox("Platform", ["YouTube", "Instagram", "TikTok", "Facebook", "LinkedIn", "Twitter/X"])
        desc = st.text_area("Content Description", height=150, placeholder="Describe your content here...")
        
        if st.button("✨ Generate Content", type="primary", use_container_width=True):
            if not desc:
                st.warning("Please enter a description.")
            else:
                with st.spinner("AI is thinking..."):
                    active_key = current_data['api_key']
                    active_platform = current_data['platform']
                    full_result = generate_seo_content(active_platform, social, desc, active_key)
                    st.session_state['last_result'] = full_result

        # --- RESULTS DISPLAY ---
        if 'last_result' in st.session_state:
            res = st.session_state['last_result']
            
            try:
                parts = res.split("### ")
                st.divider()
                st.subheader("📝 Generated Results")
                
                for part in parts:
                    if part.strip():
                        lines = part.split("\n", 1)
                        if len(lines) >= 2:
                            header = lines[0].strip()
                            body = lines[1].strip()
                            
                            st.markdown(f"**{header}**")
                            # The CSS above will force this box to be TALLER and wrap text
                            st.code(body, language="markdown") 
                
                st.divider()
                st.download_button(
                    label="📥 Download Results as .txt",
                    data=res,
                    file_name=f"{social}_seo_content.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except:
                st.write("Raw Output:")
                st.code(res, language="markdown")

if __name__ == "__main__":
    main()