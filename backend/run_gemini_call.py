# This script demonstrates how to call the Gemini API using the google-generativeai library.

import os
import google.generativeai as genai

# Configure the API key
# It's best practice to load your API key from environment variables
# Replace 'YOUR_GOOGLE_API_KEY' with your actual API key or set the GOOGLE_API_KEY environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # Fallback to a placeholder if environment variable is not set (for demonstration/testing)
    # In a real application, you should handle the missing key more robustly.
    GEMINI_API_KEY = "YOUR_PLACEHOLDER_GOOGLE_API_KEY"
    print("Warning: GEMINI_API_KEY environment variable not set. Using a placeholder.")


genai.configure(api_key=GEMINI_API_KEY)

# Choose a Gemini model (check available models in your region)
# You can list models using genai.list_models()
MODEL_NAME = 'gemini-2.0-flash' # Example model name

# Define the prompt
user_prompt = "Tell me a short story about a brave knight."

print(f"Attempting to call Gemini model: {MODEL_NAME}")
print(f"Prompt: {user_prompt}")

try:
    # Initialize the generative model
    model = genai.GenerativeModel(MODEL_NAME)

    # Generate content
    response = model.generate_content(user_prompt)

    # Print the response
    print("\nGemini API Response:")
    print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure your GOOGLE_API_KEY is correct and the model name is valid and available in your region.") 