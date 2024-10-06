import streamlit as st
from PIL import Image
import pytesseract
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from utils import clean_text  # Assuming this is your text cleaning utility


# Load environment variables (GROQ_API_KEY)
load_dotenv()


# HealthProfile class to store user health data
class HealthProfile:
    def __init__(self):
        self.allergies = []
        self.dietary_restrictions = []

    def load_profile(self):
        # Example static profile; this could be replaced by user inputs
        self.allergies = ["gluten"]
        self.dietary_restrictions = ["low sugar", "high protein"]


# Chain class for LLM-based nutrient analysis and recommendation
class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0, 
            groq_api_key=os.getenv("GROQ_API_KEY"), 
            model_name="llama-3.1-70b-versatile"
        )

    def analyze_nutrients(self, cleaned_data, health_profile):
        prompt_analysis = PromptTemplate.from_template(
            """
            ### NUTRIENT DATA:
            {nutrient_data}

            ### HEALTH PROFILE:
            Allergies: {allergies}
            Dietary restrictions: {restrictions}

            ### INSTRUCTION:
            Based on the nutrient data and the health profile, provide personalized recommendations
            including potential benefits and risks. If relevant, suggest alternatives or usage limitations.
            ### RECOMMENDATION (NO PREAMBLE):
            """
        )
        chain_analysis = prompt_analysis | self.llm
        res = chain_analysis.invoke({
            "nutrient_data": cleaned_data,
            "allergies": ', '.join(health_profile.allergies),
            "restrictions": ', '.join(health_profile.dietary_restrictions)
        })
        return res.content

    def handle_user_query(self, cleaned_data, health_profile, user_query):
        prompt_query = PromptTemplate.from_template(
            """
            ### NUTRIENT DATA:
            {nutrient_data}

            ### HEALTH PROFILE:
            Allergies: {allergies}
            Dietary restrictions: {restrictions}

            ### USER QUERY:
            {user_query}

            ### INSTRUCTION:
            Based on the above information, answer the user's query about the product.
            """
        )
        query_analysis = prompt_query | self.llm
        res = query_analysis.invoke({
            "nutrient_data": cleaned_data,
            "allergies": ', '.join(health_profile.allergies),
            "restrictions": ', '.join(health_profile.dietary_restrictions),
            "user_query": user_query
        })
        return res.content


# Function to perform OCR on the image and extract nutrient data
def extract_nutrient_data(image):
    return pytesseract.image_to_string(image)  # Extracted text


# Streamlit app setup
def create_streamlit_app(llm, health_profile, clean_text):
    # Set the background image
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://png.pngtree.com/thumb_back/fw800/background/20231228/pngtree-view-from-above-a-delectable-bowl-of-pasta-with-kitchen-tools-image_13855598.png');  /* Replace with a direct image URL */
            background-size: cover;  /* Adjust to your preference */
            background-repeat: no-repeat;
            background-position: center;
            min-height: 100vh;  /* Ensure it covers the full height */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
   

   

    st.title("🥗 Personalized Health Recommendation Generator")

    # Image uploader instead of URL input
    uploaded_image = st.file_uploader("Upload a product nutrient page image", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        try:
            # Extract nutrient data from image using OCR
            image = Image.open(uploaded_image)
            raw_nutrient_data = extract_nutrient_data(image)
            cleaned_data = clean_text(raw_nutrient_data)

            # Load health profile (e.g., allergies, restrictions)
            health_profile.load_profile()

            # Generate recommendations
            recommendations = llm.analyze_nutrients(cleaned_data, health_profile)

            # Display personalized recommendations
            st.markdown("### Personalized Recommendations:")
            st.write(recommendations)

            # User query input
            user_query = st.text_input("Ask a question about the product or share your personal concerns:")
            
            if st.button("Submit"):
                if user_query:
                    # Process user query and generate response
                    response = llm.handle_user_query(cleaned_data, health_profile, user_query)
                    st.markdown("### Response to Your Query:")
                    st.write(response)
                else:
                    st.error("Please enter a question or concern.")

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    health_profile = HealthProfile()

    # Streamlit configuration
    st.set_page_config(layout="wide", page_title="Health Recommendation Generator", page_icon="🥗")

    # Run the app
    create_streamlit_app(chain, health_profile, clean_text)
