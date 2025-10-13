import os
import logging
from typing import Any, Optional
from collections import namedtuple

import google.generativeai as genai
from dotenv import load_dotenv

# --- 1. Configuration and Initialization ---

# Set up basic logging to see the script's output and errors.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from your .env file.
load_dotenv()

# Define the model name as a global constant.
MODEL_NAME = "gemini-flash-latest"


def initialize_gemini_model() -> Optional[genai.GenerativeModel]:
    """
    Initializes and returns the Gemini GenerativeModel object.
    Returns None if the API key is not configured.
    """
    try:
        # Load the API key from the environment.
        # This will raise a KeyError if the variable is not found in your .env file.
        api_key = os.environ["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Create the model instance once and return it.
        model = genai.GenerativeModel(MODEL_NAME)
        logging.info("Gemini API configured and model initialized successfully.")
        return model
    except KeyError:
        logging.error("FATAL: GEMINI_API_KEY environment variable not set or found.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during Gemini initialization: {e}")
        return None

# Initialize the model a single time when the script starts.
# This is more efficient than creating a new model object for every function call.
gemini_model = initialize_gemini_model()


# --- 2. Core Logic ---

def generate_explanation(source_product: Any, recommended_product: Any) -> str:
    """
    Generates a short, one-sentence explanation for a product recommendation.
    """
    # Check if the model failed to initialize at startup.
    if not gemini_model:
        return "Similar in features and category. (API not configured)"

    prompt = (
        f"User viewed: {source_product.title} - {source_product.description}\n"
        f"Recommended: {recommended_product.title} - {recommended_product.description}\n"
        f"Explain briefly, in one concise sentence, why this recommendation is relevant for the user."
    )

    try:
        response = gemini_model.generate_content(prompt)
        
        # The response object has a .text attribute with the generated content.
        if response.text:
            explanation = response.text.strip()
            logging.info(f"Gemini generated explanation: {explanation}")
            return explanation
        else:
            # This case handles responses that might be blocked by safety settings.
            logging.warning("Gemini returned an empty or blocked response.")
            return "A great alternative choice."

    except Exception as e:
        logging.error(f"Gemini API call failed: {e}")
        return "Similar in features and category."


# --- 3. Testing Block ---

def run_tests():
    """
    Runs a series of tests to verify the Gemini connection and function logic.
    """
    if not gemini_model:
        print("\n❌ Cannot run tests: Gemini initialization failed. Check logs for details.")
        return

    print("\n--- 1. Testing Basic Gemini Connection ---")
    try:
        # A simple prompt to confirm the API connection is live.
        test_response = gemini_model.generate_content("Say hello!")
        print(f"✅ Connection Test Successful. Response: '{test_response.text.strip()}'")
    except Exception as e:
        print(f"❌ Connection Test Failed: {e}")
        return # Stop testing if the connection fails.

    print("\n--- 2. Testing the generate_explanation Function ---")
    
    # Create mock product objects to simulate real data.
    # `namedtuple` is a lightweight way to create simple objects for testing.
    Product = namedtuple("Product", ["title", "description"])
    source_prod = Product(
        title="Ergonomic Keyboard",
        description="A split keyboard designed to reduce wrist strain during long typing sessions."
    )
    rec_prod = Product(
        title="Vertical Mouse",
        description="A mouse that keeps your hand in a natural handshake position to prevent fatigue."
    )
    
    print(f"Source Product: '{source_prod.title}'")
    print(f"Recommended Product: '{rec_prod.title}'")
    
    # Call the actual function to get a real explanation.
    explanation = generate_explanation(source_prod, rec_prod)
    print(f"✅ Generated Explanation: {explanation}")
    print("--- All Tests Complete ---")


if __name__ == "__main__":
    run_tests()