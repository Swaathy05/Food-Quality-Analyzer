
# Food Quality Analyzer

## Overview
The Food Quality Analyzer is an interactive web application designed to help users understand the nutritional content of packaged food items. It allows users to upload images of food labels, extracts the text using OCR, and provides personalized health recommendations based on user queries and dietary restrictions.

## Problem Statement
With the growing concern over health and nutrition, many consumers struggle to understand food labels and may be unaware of allergens, hidden chemicals, and nutritional breakdowns. This application aims to bridge that gap, empowering users to make informed food choices.

## Proposed Solution
The Food Quality Analyzer leverages Optical Character Recognition (OCR) and AI to analyze food labels, providing users with clear, concise information about the contents and health implications of their food choices.

## Tech Stack
- **Frontend:**
  - HTML/CSS/JavaScript: For building the user interface.
  - CSS Animations & Transitions: To enhance user experience with interactive elements.
  - JavaScript: For managing UI interactions and redirection to the Streamlit app.

- **Backend:**
  - Python: For core chatbot logic and AI analysis.
  - Streamlit: To build the interactive web-based UI.
  - Pytesseract: For OCR to extract text from uploaded images.
  - Langchain: For conversational logic.
  - ChatGroq: For generating personalized health recommendations.

- **APIs & Libraries:**
  - dotenv: To manage environment variables securely.
  - Pillow (PIL): For image processing.

- **Infrastructure:**
  - Streamlit Cloud (or similar service): For deployment.
  - Git/GitHub: For version control.


