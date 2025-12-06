# 🚀 Social Media AI SEO Generator V25.12
A powerful, local Python web application that uses advanced AI (Google Gemini, ChatGPT, or Hugging Face) to generate viral, SEO-optimized content for social media platforms.

This app creates a seamless workflow for Social Media Managers and Content Creators by generating Titles, Descriptions, Hashtags, Keywords, and Backend Tags in a single click, complete with your specific social media links and icons.

# ✨ Features
Multi-Profile Management: Create separate profiles for different clients or brands (e.g., "Personal", "Business", "Client A").

3-Box Smart Output:

Title: High CTR, click-optimized title.

Main Content: Description + Active Social Links + Hashtags + Keywords (Ready to Copy).

Backend Tags: Comma-separated tags specifically for YouTube Studio/Platform settings.

AI Flexibility: Supports Google Gemini (Free), Hugging Face (Free), and OpenAI ChatGPT (Paid).

Smart Link Integration: Automatically appends your social media links (with correct emojis 📺, 📸, 🎵) to the bottom of every description.

Local Privacy: All API keys and profiles are stored locally in JSON files on your machine. Nothing is sent to a third-party server (other than the AI provider).

Export: Download results as .txt files.

# 🛠️ Installation & Prerequisites
You need Python installed on your computer.

Clone or Download this repository.

Install the required libraries by opening your terminal/command prompt and running:

Bash

pip install streamlit openai google-generativeai huggingface_hub
# 🔑 Getting Your API Keys
To use the app, you need an API key from one of the following providers:

Google Gemini (Recommended/Free): Get Key Here

Hugging Face (Free): Get Token Here (Select "Read" permission).

OpenAI (Paid): Get Key Here

# 🚀 How to Use the App
1. Run the Application
Open your terminal in the project folder and run:

Bash

python -m streamlit run app.py
(Or use the Run_App.vbs script if you created the one-click launcher).

2. Profile Setup (First Time)
When you launch the app, you will be taken to the Setup Page:

Profile Name: Enter a name (e.g., "My Cooking Channel").

AI Platform: Select Gemini, Hugging Face, or ChatGPT.

API Key: Paste your key.

Social Links: Enter your URLs for YouTube, Instagram, Website, etc.

Click Save: This creates a secure .json file in the profiles/ folder.

3. Generate Content
Select your profile from the sidebar dropdown.

Choose the target Platform (YouTube, Instagram, LinkedIn, etc.).

Type a description of your content (e.g., "A 10-minute tutorial on how to bake soft chocolate chip cookies").

Click ✨ Generate.

4. The Result
The app provides three distinct sections:

# 📌 Title: 
Optimized for high click-through rate.

# 📝 Main Content: 
The full body text including your description, your social links (with icons), hashtags, and keywords. Copy and paste this directly into your post.

# 🏷️ Backend Tags: 
Copy these comma-separated tags into your YouTube Studio tags section.

# 📂 File Structure
app.py: The main application logic.

# ☕ Support

If you find this tool useful, you can buy me a coffee!

# [![Support via PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=NU8U7YL5PR96S)

profiles/: A folder automatically created to store your user data (.json files).

📄 License
This project is open source. Feel free to modify and distribute.
