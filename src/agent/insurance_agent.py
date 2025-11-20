from typing import TypedDict, Annotated, Sequence
from operator import add

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

from src.vector_store.faiss_store import InsuranceVectorStore


class AgentState(TypedDict):
    """State definition for the insurance agent workflow."""
    messages: Annotated[Sequence[BaseMessage], add]  # Conversation history
    context: str  
    user_query: str  


class LifeInsuranceAgent:
    """LangGraph-based agent for life insurance inquiries."""

    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        embedding_model: str = "text-embedding-3-small",
        vector_store_path: str = "./data/vector_store",
        top_k_results: int = 3
    ):
        """
        Initialize the Life Insurance Agent.

        Args:
            model_name: OpenAI model to use
            embedding_model: Embedding model for vector store
            vector_store_path: Path to FAISS index
            top_k_results: Number of context chunks to retrieve
        """
        self.llm = ChatOpenAI(model=model_name, temperature=0.7)
        self.vector_store = InsuranceVectorStore(
            embedding_model=embedding_model,
            persist_directory=vector_store_path
        )
        self.top_k_results = top_k_results


        self.vector_store.initialize_store()

        # Build the workflow graph
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()

    def _build_workflow(self) -> StateGraph:
        """
        Build the LangGraph workflow.

        Returns:
            Compiled StateGraph
        """
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("retrieve_context", self._retrieve_context)
        workflow.add_node("generate_response", self._generate_response)

        # Define edges
        workflow.set_entry_point("retrieve_context")
        workflow.add_edge("retrieve_context", "generate_response")
        workflow.add_edge("generate_response", END)

        return workflow

    def _retrieve_context(self, state: AgentState) -> dict:
        """
        Node: Retrieve relevant context from vector store.

        Args:
            state: Current agent state

        Returns:
            Updated state with context
        """
        user_query = state["user_query"]

        # Search vector store and get top K relevant documents
        relevant_docs = self.vector_store.search(user_query, top_k=self.top_k_results)

        # Format context
        context = "\n\n".join([
            f"[Category: {doc.metadata.get('category', 'general')}]\n{doc.page_content}"
            for doc in relevant_docs
        ])

        return {"context": context}

    def _generate_response(self, state: AgentState) -> dict:
        """
        Node: Generate response using LLM with retrieved context.

        Args:
            state: Current agent state

        Returns:
            Updated state with AI response
        """
        context = state["context"]
        user_query = state["user_query"]
        conversation_history = state.get("messages", [])

        # Build system prompt
        system_prompt = f"""You are a knowledgeable and friendly life insurance support assistant.
Your role is to help users understand life insurance policies, coverage, benefits, eligibility, and claims.

Use the following knowledge base context to answer the user's question accurately:

{context}

Guidelines:
- Provide clear, helpful, and accurate information based on the context provided
- If the question is outside the scope of life insurance, politely redirect to life insurance topics
- Be conversational and maintain context from previous messages
- If you don't have enough information to answer fully, acknowledge limitations
- Use simple language and explain technical terms when necessary
"""

        # Build messages for LLM
        messages = [SystemMessage(content=system_prompt)]

        # Add conversation history (last 5 messages for context)
        messages.extend(conversation_history[-5:])

        # Add current query
        messages.append(HumanMessage(content=user_query))

        # Generate response
        response = self.llm.invoke(messages)

        # Return updated state with new messages
        return {
            "messages": [
                HumanMessage(content=user_query),
                AIMessage(content=response.content)
            ]
        }

    def chat(self, user_query: str, conversation_history: list[BaseMessage] = None) -> str:
        """
        Process a user query and return a response.

        Args:
            user_query: User's question
            conversation_history: Previous conversation messages

        Returns:
            AI response string
        """
        # Initialize state
        initial_state = {
            "messages": conversation_history or [],
            "context": "",
            "user_query": user_query
        }

        # Run the workflow
        result = self.app.invoke(initial_state)

        # Extract and return the latest AI message
        ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
        return ai_messages[-1].content if ai_messages else "I apologize, but I couldn't generate a response."

    async def achat(self, user_query: str, conversation_history: list[BaseMessage] = None) -> str:
        """
        Async version of chat method.

        Args:
            user_query: User's question
            conversation_history: Previous conversation messages

        Returns:
            AI response string
        """
        # Initialize state
        initial_state = {
            "messages": conversation_history or [],
            "context": "",
            "user_query": user_query
        }

        # Run the workflow asynchronously
        result = await self.app.ainvoke(initial_state)

        # Extract and return the latest AI message
        ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
        return ai_messages[-1].content if ai_messages else "I apologize, but I couldn't generate a response."
