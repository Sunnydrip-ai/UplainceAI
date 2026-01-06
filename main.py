#!/usr/bin/env python3
"""
Rock-Paper-Scissors-Plus Game
AI Referee using Hugging Face Mistral-7B
"""

import os
from dotenv import load_dotenv
from agent.referee_agent import RefereeAgent


def main():
    """Main game loop."""
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        print("❌ Error: HUGGINGFACE_API_KEY not found in .env file")
        print("\nTo get a FREE Hugging Face API key:")
        print("1. Visit: https://huggingface.co/settings/tokens")
        print("2. Click 'New token'")
        print("3. Name it (e.g., 'rock-paper-scissors')")
        print("4. Select 'read' access")
        print("5. Copy the token and add to .env file:")
        print("   HUGGINGFACE_API_KEY=hf_your_token_here")
        return
    
    # Initialize agent
    print("🎮 Initializing AI Referee...")
    agent = RefereeAgent(api_key)
    
    # Welcome message
    print("\n" + agent.get_welcome_message())
    
    # Game loop
    while True:
        try:
            # Get user input
            user_input = input("\n> ").strip()
            
            if not user_input:
                continue
            
            # Handle new game
            if user_input.lower() in ["new game", "restart", "reset"]:
                print("\n" + agent.reset_game())
                continue
            
            # Handle quit
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("\n👋 Thanks for playing! Goodbye!")
                break
            
            # Process move
            response = agent.process_move(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Game interrupted. Thanks for playing!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")


if __name__ == "__main__":
    main()
