# notes: add user context and previous messages in this conversation to the prompt

from openai import gpt4  # Adjust import as needed

def get_model_recommendation(user_prompt: str, models_list_path: str = 'models_list.txt') -> str | None:
    try:
        # Read the models list
        with open(models_list_path, 'r') as f:
            models_list = f.read()
        
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
        
        # Send to GPT-4 (or the correct model) and get response
        response = gpt4.generate(routing_prompt)  # Replace with correct method if needed
        
        # Clean and return the response
        model_name = response.strip()
        return model_name
    except Exception as e:
        print(f"Error getting model recommendation: {e}")
        return None

