# Social-Media-SEO
Social Media SEO
This is a complete Python application using the standard tkinter library for the interface. It includes all the features you requested:

Page 1: User profile setup (Name, AI Platform, API Key) saving to a local JSON file.

Page 2: Social media content generator (Dropdown for platform, Description input).

AI Integration: Connects to either ChatGPT (OpenAI) or Gemini (Google) to generate SEO-optimized content.

Prerequisites
You need to install the libraries for OpenAI and Google Gemini. Open your command prompt (cmd) or terminal and run:

Bash
pip install openai google-generativeai

Bash
pip install streamlit openai google-generativeai

Bash
pip install huggingface_hub


How to use the App:
First Launch (Profile Page):

Enter your Name.

Select your AI provider (e.g., Gemini (Google)).

Paste your API Key. (You can get a free Gemini API key from Google AI Studio or a paid OpenAI key from their platform).

Click Save. This creates a user_profile.json file in the same folder.

Generator Page:

If you restart the app, it will auto-detect your saved profile and take you straight here.

Select the Social Media (YouTube, TikTok, etc.).

Type a description of your content (e.g., "A video tutorial on how to bake chocolate chip cookies").

Click Generate.

The Result:

The app sends your request to the AI and returns a formatted list with a Title, Description, Hashtags, and Keywords specifically tuned for the platform you selected.

