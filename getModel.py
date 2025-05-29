# notes: add user context and previous messages in this conversation to the prompt

import openai
from openai import OpenAI
import os


def get_model_recommendation(user_prompt: str, models_list_path: str = 'models_list.txt') -> str | None:
    try:
        # Initialize openai client
        # Ensure API key is read from environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        client = OpenAI(api_key=openai.api_key)

        # Read the models list
        with open(models_list_path, 'r') as f:
            models_list = f.read()
        if not models_list:
            raise ValueError("Models list is empty")
        
        # Get user context and conversation history
        # TODO: Implement getting user context and conversation history
        user_context = ""  # Placeholder for user context
        conversation_history = ""  # Placeholder for conversation history
        
        # Prepare the routing prompt
        routing_prompt = (
            "You are a routing agent deciding between AI models. "
            "Here is the list of models and their priorities:\n"
            f"{models_list}\n"
            f"User context:\n{user_context}\n"
            f"Previous conversation:\n{conversation_history}\n"
            f"User prompt: {user_prompt}\n"
            "Based on this list for technical considerations, "
            "the user's context, conversation history, "
            "and the user prompt, "
            "answer in one word: which model is more suitable? "
            "Respond with *only* the model name."
        )
        
        # Keeping original placeholder call for now
        print("all done until sending to gpt4")
        # Use the OpenAI client to get the model recommendation based on the routing prompt
        response = client.chat.completions.create(
            model="gpt-4o", # Using a capable model for routing
            messages=[{"role": "user", "content": routing_prompt}],
            max_tokens=30 # We only expect a short model name response
        )
        
        # Extract the model name from the response
        model_name = response.choices[0].message.content.strip()

        print("all done with sending to gpt4") # This print message is now misleading
        # Clean and return the response
        # model_name = response.strip() # This line is no longer needed
        return model_name
    except Exception as e:
        print(f"Error getting model recommendation: {e}")
        return None
    
    
