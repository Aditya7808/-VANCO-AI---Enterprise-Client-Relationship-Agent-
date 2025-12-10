"""
VANCO AI - Enterprise Client Relationship Agent
LangGraph workflow for managing enterprise client interactions
Manages the flow: Input -> MemoryRetrieve -> ProfileBuilder -> LLMResponse -> MemoryStore

Built for Vanco AI - Custom AI Development from Concept to Production
"""
import json
from typing import Any, Dict, Optional
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel

from memory import LocalMemoryManager, SupermemoryManager
from profiles import ProfileBuilder, CustomerProfile


class AgentState(BaseModel):
    """State for the agent workflow"""
    customer_id: str
    customer_name: str
    user_message: str
    retrieved_memories: list = []
    customer_profile: Optional[Dict[str, Any]] = None
    profile_summary: str = ""
    llm_response: str = ""
    memory_stored: bool = False
    sentiment_analysis: str = "neutral"


class CRMAgent:
    """Customer Relationship Management Agent with LangGraph workflow"""

    def __init__(
        self,
        openai_api_key: str,
        supermemory_api_key: Optional[str] = None,
        use_local_memory: bool = True
    ):
        """Initialize CRM Agent"""
        self.openai_api_key = openai_api_key
        self.llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4", temperature=0.7)

        # Initialize memory system
        if use_local_memory or not supermemory_api_key:
            self.memory_manager = LocalMemoryManager()
        else:
            self.memory_manager = SupermemoryManager(api_key=supermemory_api_key)

        # Initialize profile builder
        self.profile_builder = ProfileBuilder()

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("input_node", self._input_node)
        workflow.add_node("memory_retrieve_node", self._memory_retrieve_node)
        workflow.add_node("profile_builder_node", self._profile_builder_node)
        workflow.add_node("llm_response_node", self._llm_response_node)
        workflow.add_node("sentiment_analysis_node", self._sentiment_analysis_node)
        workflow.add_node("memory_store_node", self._memory_store_node)

        # Add edges
        workflow.add_edge(START, "input_node")
        workflow.add_edge("input_node", "memory_retrieve_node")
        workflow.add_edge("memory_retrieve_node", "profile_builder_node")
        workflow.add_edge("profile_builder_node", "llm_response_node")
        workflow.add_edge("llm_response_node", "sentiment_analysis_node")
        workflow.add_edge("sentiment_analysis_node", "memory_store_node")
        workflow.add_edge("memory_store_node", END)

        return workflow.compile()

    def _input_node(self, state: AgentState) -> AgentState:
        """Process input message"""
        print(f"[INPUT] Customer {state.customer_id}: {state.user_message}")
        # Ensure namespace exists
        self.memory_manager.create_memory_namespace(state.customer_id)
        return state

    def _memory_retrieve_node(self, state: AgentState) -> AgentState:
        """Retrieve relevant memories from customer history"""
        print(f"[MEMORY RETRIEVE] Fetching memories for customer {state.customer_id}")

        # Retrieve relevant memories
        memories = self.memory_manager.retrieve_memories(
            customer_id=state.customer_id,
            query=state.user_message,
            limit=5
        )

        state.retrieved_memories = memories
        print(f"[MEMORY RETRIEVE] Found {len(memories)} relevant memories")
        return state

    def _profile_builder_node(self, state: AgentState) -> AgentState:
        """Build or update customer profile"""
        print(f"[PROFILE BUILDER] Building profile for customer {state.customer_id}")

        # Get or create profile
        profile = self.profile_builder.get_profile(state.customer_id)
        if not profile:
            profile = self.profile_builder.create_profile(
                customer_id=state.customer_id,
                name=state.customer_name
            )

        # Extract information from message to update profile
        self._extract_and_update_profile(state.customer_id, state.user_message)

        # Get profile summary
        profile_summary = self.profile_builder.get_profile_summary(state.customer_id)
        state.profile_summary = profile_summary
        state.customer_profile = self.profile_builder.export_profile(state.customer_id)

        print("[PROFILE BUILDER] Profile updated successfully")
        return state

    def _llm_response_node(self, state: AgentState) -> AgentState:
        """Generate personalized response using ChatGPT"""
        print("[LLM RESPONSE] Generating personalized response")

        # Build context from memories and profile
        context = self._build_context(state)

        # Create prompt
        prompt_template = PromptTemplate(
            input_variables=["customer_name", "context", "user_message"],
            template="""You are a professional Enterprise Client Relationship Manager at VANCO AI - a leading AI development company that builds custom AI solutions for enterprises.

ABOUT VANCO AI:
- Custom AI development from concept to production
- Services: AI & Machine Learning, Full-Stack Product Engineering, Analytics & Data Engineering, Cloud & DevOps
- Capabilities: Generative AI (LLMs, VLMs), Computer Vision, NLP & Conversational AI, Predictive Analytics
- Offerings: Full-Stack AI Product Development, Workforce Augmentation, AI Consulting
- Trusted by 50+ enterprises including Toyota, Mahindra, Tata, and more
- Global offices in India, USA, UK, Dubai

Client Information:
{context}

Client Message: {user_message}

Based on the client's history, project interests, and current message, provide a personalized, professional response.
Remember to:
1. Address the client by name
2. Reference their past projects, interests, or industry when relevant
3. Suggest relevant Vanco AI services or solutions if appropriate
4. Show deep understanding of their enterprise AI needs
5. Provide actionable next steps or schedule consultation if needed
6. Maintain a consultative, expert tone befitting enterprise clients

Response:"""
        )

        # Generate response
        chain = prompt_template | self.llm
        response = chain.invoke({
            "customer_name": state.customer_name,
            "context": context,
            "user_message": state.user_message
        })

        state.llm_response = response.content
        print("[LLM RESPONSE] Response generated successfully")
        return state

    def _sentiment_analysis_node(self, state: AgentState) -> AgentState:
        """Analyze sentiment of customer message"""
        print("[SENTIMENT ANALYSIS] Analyzing customer sentiment")

        sentiment_prompt = PromptTemplate(
            input_variables=["message"],
            template="""Analyze the sentiment of this customer message and respond with only one word: positive, neutral, or negative.

Message: {message}

Sentiment:"""
        )

        chain = sentiment_prompt | self.llm
        sentiment = chain.invoke({"message": state.user_message})
        sentiment_text = sentiment.content.strip().lower()

        # Validate sentiment
        if sentiment_text not in ["positive", "neutral", "negative"]:
            sentiment_text = "neutral"

        state.sentiment_analysis = sentiment_text
        self.profile_builder.update_sentiment(state.customer_id, sentiment_text)

        print(f"[SENTIMENT ANALYSIS] Sentiment: {sentiment_text}")
        return state

    def _memory_store_node(self, state: AgentState) -> AgentState:
        """Store interaction in memory"""
        print("[MEMORY STORE] Storing interaction in memory")

        # Store customer message
        self.memory_manager.store_memory(
            customer_id=state.customer_id,
            content=state.user_message,
            memory_type="customer_query",
            metadata={
                "sentiment": state.sentiment_analysis,
                "timestamp": datetime.now().isoformat()
            }
        )

        # Store agent response
        self.memory_manager.store_memory(
            customer_id=state.customer_id,
            content=state.llm_response,
            memory_type="agent_response",
            metadata={
                "timestamp": datetime.now().isoformat()
            }
        )

        # Update interaction summary in profile
        self.profile_builder.update_last_interaction(
            state.customer_id,
            state.user_message[:100] + "..." if len(state.user_message) > 100 else state.user_message
        )

        state.memory_stored = True
        print("[MEMORY STORE] Interaction stored successfully")
        return state

    def _build_context(self, state: AgentState) -> str:
        """Build context from memories and profile"""
        context = ""

        # Add profile information
        if state.profile_summary:
            context += "Profile Summary:\n" + state.profile_summary + "\n\n"

        # Add relevant memories
        if state.retrieved_memories:
            context += "Relevant Past Interactions:\n"
            for memory in state.retrieved_memories[:3]:
                if isinstance(memory, dict):
                    content = memory.get("content", str(memory))
                else:
                    content = str(memory)
                context += f"- {content}\n"
            context += "\n"

        # Add product recommendations
        recommendations = self.profile_builder.recommend_products(state.customer_id)
        if recommendations:
            context += "Suggested Products to Recommend:\n"
            for rec in recommendations:
                context += f"- {rec}\n"

        return context or "No previous history available for this customer."

    def _extract_and_update_profile(self, customer_id: str, message: str) -> None:
        """Extract information from message using AI and update profile"""
        message_lower = message.lower()

        # Use LLM to extract structured information from the message
        extraction_prompt = PromptTemplate(
            input_variables=["message"],
            template="""Analyze this customer message and extract any relevant business information.
Return a JSON object with the following fields (use null if not found):

{{
    "company_name": "extracted company/organization name if mentioned",
    "company_type": "type like Hospital, Bank, Retail Store, Factory, etc.",
    "industry": "industry vertical like Healthcare, Finance, Retail, Manufacturing, etc.",
    "email": "email address if mentioned",
    "phone": "phone number if mentioned",
    "meeting_date": "meeting date if scheduling discussed (format: YYYY-MM-DD or as mentioned)",
    "meeting_time": "meeting time if mentioned",
    "project_name": "specific project name or description if discussed",
    "project_type": "type of project like Website, Mobile App, AI System, Chatbot, etc.",
    "project_description": "brief description of what they want to build",
    "requirements": ["list of specific requirements or features mentioned"],
    "budget": "budget range if mentioned",
    "timeline": "decision or project timeline if mentioned",
    "services_interested": ["list of services they seem interested in from: AI & Machine Learning, Full-Stack Development, Computer Vision, NLP, Analytics, Cloud & DevOps, Consulting"]
}}

Customer Message: {message}

JSON Response:"""
        )

        try:
            chain = extraction_prompt | self.llm
            result = chain.invoke({"message": message})
            
            # Parse JSON response
            import re
            json_match = re.search(r'\{[\s\S]*\}', result.content)
            if json_match:
                extracted = json.loads(json_match.group())
                
                # Update company info
                if extracted.get("company_name") or extracted.get("company_type") or extracted.get("industry"):
                    self.profile_builder.update_company_info(
                        customer_id,
                        company=extracted.get("company_name"),
                        company_type=extracted.get("company_type"),
                        industry=extracted.get("industry")
                    )
                
                # Update contact info
                if extracted.get("email") or extracted.get("phone"):
                    self.profile_builder.update_contact_info(
                        customer_id,
                        email=extracted.get("email"),
                        phone=extracted.get("phone")
                    )
                
                # Add scheduled meeting
                if extracted.get("meeting_date"):
                    self.profile_builder.add_scheduled_meeting(
                        customer_id,
                        meeting_date=extracted.get("meeting_date", "TBD"),
                        meeting_time=extracted.get("meeting_time", "TBD"),
                        purpose="Project Discussion"
                    )
                
                # Add proposed project
                if extracted.get("project_name") or extracted.get("project_type"):
                    self.profile_builder.add_proposed_project(
                        customer_id,
                        project_name=extracted.get("project_name") or extracted.get("project_type", "New Project"),
                        project_type=extracted.get("project_type", "AI Solution"),
                        description=extracted.get("project_description", "To be discussed")
                    )
                
                # Add requirements
                if extracted.get("requirements"):
                    for req in extracted.get("requirements", []):
                        if req:
                            self.profile_builder.add_key_requirement(customer_id, req)
                
                # Update service interests
                if extracted.get("services_interested"):
                    self.profile_builder.update_service_interests(
                        customer_id, 
                        extracted.get("services_interested", [])
                    )

        except Exception as e:
            print(f"[PROFILE EXTRACTION] Error extracting info: {e}")

        # Fallback: Simple keyword-based extraction
        # Detect service interests for Vanco AI
        service_keywords = {
            "ai_ml": ["ai", "machine learning", "ml", "deep learning", "neural", "model", "llm", "gpt", "generative"],
            "computer_vision": ["vision", "image", "video", "detection", "recognition", "ocr", "camera"],
            "nlp": ["nlp", "chatbot", "conversational", "language", "text", "sentiment", "speech"],
            "data_analytics": ["analytics", "dashboard", "data", "pipeline", "bi", "reporting", "insights"],
            "cloud_devops": ["cloud", "aws", "azure", "gcp", "devops", "infrastructure", "deployment"],
            "full_stack": ["web", "mobile", "app", "api", "frontend", "backend", "development", "website"],
            "consulting": ["consulting", "strategy", "roadmap", "assessment", "audit"],
            "automation": ["automation", "workflow", "process", "rpa", "automate"],
        }

        for category, keywords in service_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                self.profile_builder.update_preferences(customer_id, [category])

        # Detect industry
        industry_keywords = {
            "manufacturing": ["manufacturing", "factory", "production", "supply chain"],
            "retail": ["retail", "ecommerce", "store", "shopping"],
            "healthcare": ["healthcare", "medical", "hospital", "pharma"],
            "finance": ["finance", "banking", "fintech", "insurance"],
            "media": ["media", "entertainment", "content", "streaming"],
            "logistics": ["logistics", "shipping", "delivery", "transport"],
            "education": ["education", "university", "learning", "training"],
        }

        for industry, keywords in industry_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                self.profile_builder.add_tag(customer_id, f"industry:{industry}")

        # Detect project urgency
        urgency_keywords = ["urgent", "asap", "immediately", "deadline", "quick", "fast"]
        if any(keyword in message_lower for keyword in urgency_keywords):
            self.profile_builder.add_tag(customer_id, "high_priority")

        # Detect issues
        issue_keywords = ["problem", "issue", "bug", "broken", "not working", "complaint", "disappointed", "delayed", "failed"]
        if any(keyword in message_lower for keyword in issue_keywords):
            self.profile_builder.add_issue(
                customer_id,
                message[:100],
                "customer_reported",
                severity="medium"
            )

    def process_customer_message(
        self,
        customer_id: str,
        customer_name: str,
        message: str
    ) -> str:
        """Process a customer message through the entire workflow"""
        print(f"\n{'='*60}")
        print(f"Processing message from {customer_name} ({customer_id})")
        print(f"{'='*60}\n")

        initial_state = AgentState(
            customer_id=customer_id,
            customer_name=customer_name,
            user_message=message
        )

        # Run the graph - returns a dictionary
        final_state = self.graph.invoke(initial_state)

        # Handle both dict and object return types
        if isinstance(final_state, dict):
            return final_state.get("llm_response", "")
        return final_state.llm_response

    def get_customer_profile(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get customer profile"""
        return self.profile_builder.export_profile(customer_id)

    def get_customer_memories(self, customer_id: str) -> list:
        """Get all memories for a customer"""
        return self.memory_manager.get_all_memories(customer_id)

    def get_profile_summary(self, customer_id: str) -> str:
        """Get human-readable profile summary"""
        return self.profile_builder.get_profile_summary(customer_id)
