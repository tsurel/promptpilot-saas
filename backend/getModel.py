# notes: add user context and previous messages in this conversation to the prompt

import openai
from openai import OpenAI
import os
from supabase import create_client, Client


def get_model_recommendation(user_prompt: str, user_id: str | None = None, conversation_id: str | None = None, models_list_path: str = 'models_list.txt') -> str | None:
    try:
        # Initialize openai client
        # Ensure API key is read from environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        client = OpenAI(api_key=openai.api_key)

        # Initialize Supabase client
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        if not supabase_url or not supabase_key:
            print("Supabase URL or Key environment variable not set. Proceeding without Supabase data.")
            supabase = None
        else:
            supabase: Client = create_client(supabase_url, supabase_key)

        # Read the models list
        with open(models_list_path, 'r') as f:
            models_list = f.read()
        if not models_list:
            raise ValueError("Models list is empty")
        
        # Get user context and conversation history from Supabase if IDs are provided
        user_context = "" # Default empty
        conversation_history = "" # Default empty

        if supabase:
            if user_id:
                try:
                    response = supabase.from_('user_profile_context').select('context_data').eq('user_id', user_id).single().execute()
                    if response.data and response.data.get('context_data'):
                        user_context = response.data['context_data']
                    else:
                        print(f"No user context found for user_id: {user_id}")
                except Exception as e:
                    print(f"Error fetching user context for user_id {user_id}: {e}")

            if conversation_id:
                try:
                    # Fetch metadata from conversation table
                    conv_response = supabase.from_('conversation').select('metadata').eq('id', conversation_id).single().execute()
                    if conv_response.data and conv_response.data.get('metadata'):
                        conversation_history += f"Conversation Metadata: {conv_response.data['metadata']}\n"
                    else:
                         print(f"No conversation metadata found for conversation_id: {conversation_id}")

                    # Fetch context from conversation_context table
                    context_response = supabase.from_('conversation_context').select('context').eq('conversation_id', conversation_id).execute()
                    if context_response.data:
                         # Assuming context is a list of messages or similar, join them
                        conversation_history += "\n".join([item['context'] for item in context_response.data if item.get('context')])
                    else:
                        print(f"No conversation context found for conversation_id: {conversation_id}")

                except Exception as e:
                    print(f"Error fetching conversation data for conversation_id {conversation_id}: {e}")

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
    
    
