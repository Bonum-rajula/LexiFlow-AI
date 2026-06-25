# src/lexiflow/orchestration/graph.py
from langgraph.graph import StateGraph, START, END

from ..core.state import AgentState
from ..agents import RetrieverAgent, CriticAgent, SynthesizerAgent
from .router import should_continue


class Orchestrator:
    """
    The Cerebrum: Builds and compiles the LangGraph workflow.
    
    DIP Compliance: Depends on Agent classes (which themselves depend on abstractions).
    Does NOT depend on infrastructure (OpenAI, ChromaDB, etc.).
    """

    def __init__(
        self,
        retriever: RetrieverAgent,
        critic: CriticAgent,
        synthesizer: SynthesizerAgent,
        max_retries: int = 2,
    ):
        """
        Args:
            retriever: Instance of RetrieverAgent.
            critic: Instance of CriticAgent.
            synthesizer: Instance of SynthesizerAgent.
            max_retries: Maximum number of retrieval loops before forcing synthesis.
        """
        self.retriever = retriever
        self.critic = critic
        self.synthesizer = synthesizer
        self.max_retries = max_retries

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Construct the StateGraph with nodes and edges."""
        # 1. Initialize the graph with the AgentState schema
        workflow = StateGraph(AgentState)

        # 2. Define the nodes (each node is an async function that updates state)
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("critique", self._critique_node)
        workflow.add_node("synthesize", self._synthesize_node)

        # 3. Define the edges
        # Start -> retrieve
        workflow.add_edge(START, "retrieve")

        # retrieve -> critique (always)
        workflow.add_edge("retrieve", "critique")

        # critique -> conditional router -> synthesize OR back to retrieve
        workflow.add_conditional_edges(
            "critique",
            self._route_decision,  # Function that returns "continue" or "retry"
            {
                "continue": "synthesize",
                "retry": "retrieve",
            }
        )

        # synthesize -> END
        workflow.add_edge("synthesize", END)

        return workflow.compile()

    # ------------------------------------------------------------------
    # Node Wrappers (coordinate agent execution with state updates)
    # ------------------------------------------------------------------

    async def _retrieve_node(self, state: AgentState) -> dict:
        """Wrapper for RetrieverAgent."""
        # Increment retry count before retrieval
        state["retry_count"] = state.get("retry_count", 0)
        state["max_retries"] = self.max_retries
        
        result = await self.retriever.retrieve(state)
        # Ensure retry_count persists (incremented by router when looping)
        result["retry_count"] = state["retry_count"]
        result["max_retries"] = self.max_retries
        return result

    async def _critique_node(self, state: AgentState) -> dict:
        """Wrapper for CriticAgent."""
        result = await self.critic.critique(state)
        # Preserve retry count and max retries
        result["retry_count"] = state.get("retry_count", 0)
        result["max_retries"] = self.max_retries
        return result

    async def _synthesize_node(self, state: AgentState) -> dict:
        """Wrapper for SynthesizerAgent."""
        result = await self.synthesizer.synthesize(state)
        return result

    # ------------------------------------------------------------------
    # Router Wrapper (injects retry increment logic)
    # ------------------------------------------------------------------

    def _route_decision(self, state: AgentState) -> str:
        """
        Wrapper around the router that increments retry_count before looping.
        """
        decision = should_continue(state)
        if decision == "retry":
            # Increment the retry count in the state for the next loop
            state["retry_count"] = state.get("retry_count", 0) + 1
            logger.debug(f"🔄 Retry count incremented to {state['retry_count']}")
            return "retry"
        return "continue"

    # ------------------------------------------------------------------
    # Public API: Invoke the graph
    # ------------------------------------------------------------------

    async def run(self, question: str) -> dict:
        """
        Execute the full agent workflow.
        
        Args:
            question: The user's query string.
            
        Returns:
            The final state dictionary containing the answer, chunks, critique, etc.
        """
        initial_state: AgentState = {
            "question": question,
            "chunks": [],
            "critique": None,
            "final_answer": None,
            "error": None,
            "retry_count": 0,
            "max_retries": self.max_retries,
        }
        
        # Invoke the compiled graph
        final_state = await self.graph.ainvoke(initial_state)
        return final_state