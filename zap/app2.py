import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# Custom CSS for UI enhancements
def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Main title styling */
        h1 {
            color: #4F8BF9;
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 20px;
        }

        /* Subheader styling */
        h2 {
            color: #2E86C1;
            font-size: 1.8rem;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        /* Input field styling */
        .stTextInput input {
            border: 2px solid #4F8BF9;
            border-radius: 5px;
            padding: 10px;
            font-size: 1rem;
        }

        /* Button styling */
        .stButton button {
            background-color: #4F8BF9;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 1rem;
            border: none;
            transition: background-color 0.3s;
        }

        .stButton button:hover {
            background-color: #2E86C1;
        }

        /* Dropdown styling */
        .stSelectbox select {
            border: 2px solid #4F8BF9;
            border-radius: 5px;
            padding: 10px;
            font-size: 1rem;
        }

        /* Response box styling */
        .stMarkdown {
            background-color: #F4F6F6;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #D0D3D4;
            margin-top: 20px;
        }

        /* Footer styling */
        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 0.9rem;
            color: #7F8C8D;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to scrape documentation
def scrape_documentation(url):
    """
    Scrape documentation from a given URL.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract relevant content (e.g., text from <p>, <h1>, <h2>, etc.)
        content = ""
        for tag in soup.find_all(["h1", "h2", "h3", "p", "li"]):
            content += tag.get_text() + "\n"
        
        return content
    except Exception as e:
        return f"Error scraping documentation: {e}"

# Function to generate response using Gemini
def generate_response(prompt, context):
    """
    Generate a response using the Gemini model.
    """
    try:
        # Load the correct Gemini model
        model = genai.GenerativeModel("models/gemini-1.5-pro")
        
        # Generate response
        response = model.generate_content(f"{context}\n\nQuestion: {prompt}\nAnswer:")
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

# Streamlit app
def main():
    # Inject custom CSS
    inject_custom_css()

    st.title("CDP Support Agent Chatbot")
    st.write("Ask me how-to questions about Segment, mParticle, Lytics, or Zeotap!")

    # Dropdown to select CDP
    cdp_options = ["Segment", "mParticle", "Lytics", "Zeotap"]
    selected_cdp = st.selectbox("Select a CDP:", cdp_options)

    # Map CDP to documentation URL
    cdp_docs = {
        "Segment": "https://segment.com/docs/?ref=nav",
        "mParticle": "https://docs.mparticle.com/",
        "Lytics": "https://docs.lytics.com/",
        "Zeotap": "https://docs.zeotap.com/home/en-us/"
    }

    # Input field for user question
    user_question = st.text_input("Enter your question:")

    if user_question:
        # Check for irrelevant questions
        irrelevant_keywords = ["movie", "weather", "sports", "music", "food"]
        if any(keyword in user_question.lower() for keyword in irrelevant_keywords):
            st.write("Sorry, I can only answer questions related to CDPs.")
        else:
            # Scrape documentation for the selected CDP
            docs_url = cdp_docs[selected_cdp]
            st.write(f"Fetching documentation from {docs_url}...")
            docs_content = scrape_documentation(docs_url)

            # Generate response using Gemini
            st.write("Generating response...")
            response = generate_response(user_question, docs_content)

            # Display response
            st.write("### Answer:")
            st.write(response)

    # Footer
    st.markdown(
        '<div class="footer">Powered by Gemini and Streamlit</div>',
        unsafe_allow_html=True,
    )

# Run the app
if __name__ == "__main__":
    # Configure Gemini API (replace with your API key)
    genai.configure(api_key="AIzaSyB_Sfa6qt63_Ap-Qjd86Tavmmg2iiSLgn4")
    main()