import os
import sys
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from app.agent.insurance_agent import LifeInsuranceAgent

load_dotenv()

console = Console()


class ChatCLI:
    """Command-line interface for the insurance agent."""

    def __init__(self):
        """Initialize the CLI."""
        self.conversation_history: List[BaseMessage] = []
        self.agent: LifeInsuranceAgent = None

    def initialize_agent(self):
        """Initialize the agent with configuration from environment."""
        console.print("\n[bold cyan]Initializing Life Insurance Support Agent...[/bold cyan]")

        try:
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
            vector_store_path = os.getenv("VECTOR_STORE_PATH", "./data/vector_store")
            top_k_results = int(os.getenv("TOP_K_RESULTS", "3"))

            self.agent = LifeInsuranceAgent(
                model_name=model_name,
                embedding_model=embedding_model,
                vector_store_path=vector_store_path,
                top_k_results=top_k_results
            )

            console.print("[bold green]✓ Agent initialized successfully![/bold green]\n")
            return True

        except Exception as e:
            console.print(f"[bold red]✗ Error initializing agent: {str(e)}[/bold red]")
            console.print("\n[yellow]Please ensure:[/yellow]")
            console.print("  1. OPENAI_API_KEY is set in your .env file")
            console.print("  2. All dependencies are installed (pip install -r requirements.txt)")
            return False

    def display_welcome(self):
        """Display welcome message."""
        welcome_text = """
# Life Insurance Support Assistant

Welcome! I'm here to help you with questions about:
- **Policy Types**: Term, Whole, Universal, and Variable Life Insurance
- **Coverage & Benefits**: Death benefits, cash value, living benefits
- **Eligibility**: Age, health, occupation requirements
- **Claims**: Filing process, contestability, payment options
- **Costs**: Premium factors, ways to save money
- **Policy Management**: Beneficiaries, conversions, reinstatement

Type your question or use these commands:
- **clear**: Clear conversation history
- **quit** or **exit**: Exit the application
"""
        console.print(Panel(Markdown(welcome_text), border_style="cyan"))

    def display_assistant_response(self, response: str):
        """
        Display the assistant's response in a formatted panel.

        Args:
            response: Response text from the agent
        """
        console.print(
            Panel(
                Markdown(response),
                title="[bold blue]Assistant[/bold blue]",
                border_style="blue",
                padding=(1, 2)
            )
        )

    def display_user_message(self, message: str):
        """
        Display the user's message.

        Args:
            message: User's input message
        """
        console.print(f"\n[bold green]You:[/bold green] {message}")

    def handle_command(self, user_input: str) -> bool:
        """
        Handle special commands.

        Args:
            user_input: User input to check for commands

        Returns:
            True if command was handled, False otherwise
        """
        command = user_input.lower().strip()

        if command in ["quit", "exit"]:
            console.print("\n[bold cyan]Thank you for using Life Insurance Support Assistant![/bold cyan]")
            console.print("Have a great day! 👋\n")
            return True

        if command == "clear":
            self.conversation_history.clear()
            console.clear()
            self.display_welcome()
            console.print("[yellow]Conversation history cleared.[/yellow]\n")
            return False

        return False

    def run(self):
        """Run the CLI chat loop."""
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            console.print("[bold red]Error: OPENAI_API_KEY not found![/bold red]")
            console.print("Please create a .env file with your OpenAI API key.")
            console.print("See .env.example for reference.\n")
            sys.exit(1)


        if not self.initialize_agent():
            sys.exit(1)

        # Display welcome message
        self.display_welcome()

        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold green]You[/bold green]").strip()

                if not user_input:
                    continue

                # Handle commands
                if self.handle_command(user_input):
                    break

                # Display user message
                self.display_user_message(user_input)

                # Show thinking indicator
                with console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots"):
                    # Get response from agent
                    response = self.agent.chat(
                        user_query=user_input,
                        conversation_history=self.conversation_history
                    )

                    # Update conversation history
                    self.conversation_history.extend([
                        HumanMessage(content=user_input),
                        AIMessage(content=response)
                    ])

                # Display response
                self.display_assistant_response(response)

            except KeyboardInterrupt:
                console.print("\n\n[yellow]Interrupted by user.[/yellow]")
                console.print("[bold cyan]Thank you for using Life Insurance Support Assistant![/bold cyan]\n")
                break

            except Exception as e:
                console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
                console.print("[yellow]Please try again or type 'quit' to exit.[/yellow]\n")


def main():
    """Main entry point for the CLI."""
    cli = ChatCLI()
    cli.run()


if __name__ == "__main__":
    main()
