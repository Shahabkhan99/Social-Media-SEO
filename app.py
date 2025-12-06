import streamlit as st
import json
import os
import glob
import google.generativeai as genai
from openai import OpenAI
from huggingface_hub import InferenceClient

# --- Configuration ---
PROFILES_DIR = "profiles"

# --- Data Functions ---
def ensure_profiles_dir():
    if not os.path.exists(PROFILES_DIR):
        os.makedirs(PROFILES_DIR)

def get_all_profile_names():
    ensure_profiles_dir()
    files = glob.glob(os.path.join(PROFILES_DIR, "*.json"))
    return sorted([os.path.splitext(os.path.basename(f))[0] for f in files])

def load_profile_data(profile_name):
    filepath = os.path.join(PROFILES_DIR, f"{profile_name}.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_profile_data(name, platform, api_key, links_dict):
    ensure_profiles_dir()
    data = {"platform": platform, "api_key": api_key, "links": links_dict}
    safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c in (' ', '-', '_')]).strip()
    with open(os.path.join(PROFILES_DIR, f"{safe_name}.json"), "w") as f:
        json.dump(data, f, indent=4)


# --- AI Logic ---
def generate_seo_content(platform, social_media, description, api_key, social_links):
    # 1. Icons for Social Platforms
    emoji_map = {
        "YouTube": "📺", 
        "Instagram": "📸", 
        "TikTok": "🎵", 
        "Facebook": "📘",
        "Pinterest": "📌", 
        "LinkedIn": "💼", 
        "X (Twitter)": "🐦",
        "Tumblr": "📝", 
        "Website": "🌍", 
        "Digital Card": "🪪"
    }
    
    # 2. Convert links into formatted text
    links_text = "\n".join(
        f"{emoji_map.get(site, '🔗')} {site}: {link}"
        for site, link in social_links.items() if link
    )

    # 3. Final AI Prompt — Optimized for Strict Output Structure
    system_prompt = f"""
    Act as a Social Media SEO Expert.

    Platform: {social_media}
    Topic / Content Focus: {description}

    Your Task:
    Create a high-performing social post with an SEO score of 95+.

    You MUST follow these rules:
    1. Use the exact section labels shown below — no extra decoration or headers around them.
    2. Complete every section fully. Do NOT stop until all 30 hashtags are written.
    3. If text becomes long, shorten the content — NEVER reduce hashtags (must be 30).
    4. In SECTION_BODY you must follow the structure silently (no titles, no headings, no list syntax).
       The structure should be applied naturally inside the writing.

    My Links:
    {links_text}

    ========================
    ===SECTION_TITLE===
    (Write a compelling title — short, powerful, high click-thru potential)

    The structure for SECTION_BODY must be followed **without announcing it**:
       - Begin with an attention-grabbing hook sentence.
       - Continue naturally into an in-depth body with value-based insight or steps.
       - Smoothly insert "My Links" exactly where relevant in the flow.
       - After the content, generate 30 SEO keywords (comma separated).
       - Immediately after keywords, generate 30 SEO hashtags.
    
    ===SECTION_TAGS===
    (Provide a comma-separated list of tags for backend settings. e.g. tag1, tag2, tag3)
    """

    try:
        content = ""
        if platform == "Gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(system_prompt)
            content = response.text
        elif platform == "ChatGPT":
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o", messages=[{"role": "user", "content": system_prompt}]
            )
            content = response.choices[0].message.content
        elif platform == "Hugging Face":
            client = InferenceClient(api_key=api_key)
            response = client.chat_completion(
                model="Qwen/Qwen2.5-7B-Instruct", 
                messages=[{"role": "user", "content": system_prompt}],
                max_tokens=3500 
            )
            content = response.choices[0].message.content
        return content
    except Exception as e:
        return f"Error: {str(e)}"

# --- App GUI ---
def main():
    st.set_page_config(page_title="AI SEO Pro", page_icon="⚡", layout="centered")
    st.markdown("""<style>code { white-space: pre-wrap !important; word-break: break-word !important; } .stTextArea textarea { font-size: 16px; }</style>""", unsafe_allow_html=True)

    profiles = get_all_profile_names()
    
    if "page" not in st.session_state: st.session_state.page = "setup" if not profiles else "generator"
    if "edit_mode" not in st.session_state: st.session_state.edit_mode = False
    if "selected_user_key" not in st.session_state: st.session_state.selected_user_key = profiles[0] if profiles else None

    # Sidebar
    with st.sidebar:
        st.header("👤 User Management")
        if profiles:
            curr_idx = profiles.index(st.session_state.selected_user_key) if st.session_state.selected_user_key in profiles else 0
            sel_user = st.selectbox("Switch Profile", profiles, index=curr_idx)
            st.session_state.selected_user_key = sel_user
            current_data = load_profile_data(sel_user)
            st.success(f"Loaded: {sel_user}")
            if st.button("✏️ Edit Profile"):
                st.session_state.page, st.session_state.edit_mode = "setup", True
                st.rerun()
        else:
            sel_user, current_data = None, {}
            st.warning("No profiles found.")
        st.divider()
        if st.button("➕ Create New"):
            st.session_state.page, st.session_state.edit_mode = "setup", False
            st.rerun()
        if profiles and st.button("Go to Generator"):
            st.session_state.page = "generator"
            st.rerun()

    # Page 1: Setup
    if st.session_state.page == "setup":
        is_edit = st.session_state.edit_mode
        if is_edit and sel_user:
            st.title(f"✏️ Edit: {sel_user}")
            u_data = load_profile_data(sel_user)
            d_name, d_plat, d_key, d_links = sel_user, u_data.get("platform", "Gemini"), u_data.get("api_key", ""), u_data.get("links", {})
        else:
            st.title("🛠️ New Profile")
            d_name, d_plat, d_key, d_links = "", "Gemini", "", {}

        with st.form("pf"):
            st.subheader("1. Settings")
            name = st.text_input("Profile Name", value=d_name, disabled=is_edit)
            plat = st.selectbox("Platform", ["Hugging Face", "Gemini", "ChatGPT"], index=["Hugging Face", "Gemini", "ChatGPT"].index(d_plat) if d_plat in ["Hugging Face", "Gemini", "ChatGPT"] else 1)
            key = st.text_input("API Key", value=d_key, type="password")
            
            st.subheader("2. Social Links")
            c1, c2 = st.columns(2)
            with c1:
                l_yt = st.text_input("YouTube", value=d_links.get("YouTube", ""))
                l_ig = st.text_input("Instagram", value=d_links.get("Instagram", ""))
                l_tt = st.text_input("TikTok", value=d_links.get("TikTok", ""))
                l_fb = st.text_input("Facebook", value=d_links.get("Facebook", ""))
                l_pi = st.text_input("Pinterest", value=d_links.get("Pinterest", ""))
            with c2:
                l_li = st.text_input("LinkedIn", value=d_links.get("LinkedIn", ""))
                l_x = st.text_input("X (Twitter)", value=d_links.get("X (Twitter)", ""))
                l_tu = st.text_input("Tumblr", value=d_links.get("Tumblr", ""))
                l_wb = st.text_input("Website", value=d_links.get("Website", ""))
                l_dc = st.text_input("Digital Card", value=d_links.get("Digital Card", ""))

            if st.form_submit_button("Save"):
                if name and key:
                    links = {"YouTube": l_yt, "Instagram": l_ig, "TikTok": l_tt, "Facebook": l_fb, "Pinterest": l_pi, "LinkedIn": l_li, "X (Twitter)": l_x, "Tumblr": l_tu, "Website": l_wb, "Digital Card": l_dc}
                    save_profile_data(name, plat, key, links)
                    st.session_state.selected_user_key = name
                    st.session_state.page = "generator"
                    st.rerun()

    # Page 2: Generator
    elif st.session_state.page == "generator":
        if not sel_user: return st.error("Create a profile first.")
        st.title("🚀 Generator")
        st.caption(f"Profile: **{sel_user}** | Platform: **{current_data.get('platform')}**")
        
        # Show Links
        active_links = current_data.get('links', {})
        with st.expander("👀 View Active Social Links"):
            if any(active_links.values()):
                for platform, link in active_links.items():
                    if link: st.write(f"**{platform}:** {link}")
            else:
                st.write("No links set.")

        social = st.selectbox("Target Platform", ["YouTube", "Instagram", "TikTok", "Facebook", "LinkedIn", "Twitter/X", "Pinterest", "Tumblr"])
        desc = st.text_area("Content Description", height=150)
        
        if st.button("✨ Generate", type="primary", use_container_width=True):
            if not desc: st.warning("Enter description.")
            else:
                with st.spinner("Generating..."):
                    res = generate_seo_content(current_data['platform'], social, desc, current_data['api_key'], current_data['links'])
                    st.session_state['last_result'] = res

        # Results
        if 'last_result' in st.session_state:
            res = st.session_state['last_result']
            
            title_text = ""
            main_text = ""
            tags_text = ""

            try:
                # 1. Split Title
                if "===SECTION_TITLE===" in res:
                    temp = res.split("===SECTION_TITLE===")[1]
                    title_text = temp.split("===SECTION_BODY===")[0].strip()
                
                # 2. Split Body
                if "===SECTION_BODY===" in res:
                    temp = res.split("===SECTION_BODY===")[1]
                    main_text = temp.split("===SECTION_TAGS===")[0].strip()
                
                # 3. Split Tags
                if "===SECTION_TAGS===" in res:
                    tags_text = res.split("===SECTION_TAGS===")[1].strip()

                # Fallback
                if not title_text and not main_text:
                    main_text = res
                    st.warning("AI formatting failed. Showing raw output:")

                st.divider()
                st.subheader("📌 Title (95% SEO)")
                st.code(title_text, language="markdown")
                
                st.subheader("📝 Main Content (Desc + Links + Hashtags + Keywords)")
                st.code(main_text, language="markdown")
                
                st.subheader("🏷️ Backend Tags")
                st.code(tags_text, language="text")
                
                st.divider()
                st.download_button("📥 Download .txt", res, f"{social}_seo.txt", "text/plain", use_container_width=True)

            except Exception as e:
                st.error(f"Display Error: {e}")
                st.code(res, language="markdown")

if __name__ == "__main__":
    main()