"""
Demonstration script showing the LangGraph workflow visualization
"""
from typing import Dict, Any
import json


def visualize_workflow():
    """Visualize the CRM Agent workflow"""
    
    workflow = """
╔══════════════════════════════════════════════════════════════════════════════╗
║           CUSTOMER RELATIONSHIP AI AGENT - LANGGRAPH WORKFLOW                ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│  START                                                                       │
│    ↓                                                                         │
│  INPUT NODE                                                                 │
│  ├─ Receives customer message                                               │
│  ├─ Initializes memory namespace                                            │
│  └─ Validates input                                                         │
│    ↓                                                                         │
│  MEMORY RETRIEVE NODE                                                       │
│  ├─ Queries Supermemory.ai / Local Storage                                  │
│  ├─ Semantic search on customer query                                       │
│  ├─ Retrieves up to 5 most relevant memories                                │
│  └─ Returns: Retrieved memories, metadata, timestamps                       │
│    ↓                                                                         │
│  PROFILE BUILDER NODE                                                       │
│  ├─ Loads existing customer profile                                         │
│  ├─ Extracts preferences from message                                       │
│  ├─ Detects issues/complaints                                               │
│  ├─ Updates purchase history if mentioned                                   │
│  └─ Generates profile summary                                               │
│    ↓                                                                         │
│  LLM RESPONSE NODE                                                          │
│  ├─ Builds context from:                                                    │
│  │  ├─ Customer profile                                                     │
│  │  ├─ Purchase history                                                     │
│  │  ├─ Retrieved memories                                                   │
│  │  └─ Product recommendations                                              │
│  ├─ Calls ChatGPT with personalized prompt                                  │
│  └─ Returns: Personalized agent response                                    │
│    ↓                                                                         │
│  SENTIMENT ANALYSIS NODE                                                    │
│  ├─ Analyzes customer message sentiment                                     │
│  ├─ Classifies: POSITIVE / NEUTRAL / NEGATIVE                               │
│  ├─ Updates customer sentiment trend                                        │
│  └─ Stores sentiment in profile                                             │
│    ↓                                                                         │
│  MEMORY STORE NODE                                                          │
│  ├─ Stores customer message in memory:                                      │
│  │  ├─ Type: customer_query                                                 │
│  │  ├─ Metadata: sentiment, timestamp                                       │
│  │  └─ Namespace: customer_ID                                               │
│  ├─ Stores agent response in memory:                                        │
│  │  ├─ Type: agent_response                                                 │
│  │  └─ Metadata: timestamp                                                  │
│  ├─ Updates last interaction in profile                                     │
│  └─ Increments interaction count                                            │
│    ↓                                                                         │
│  END                                                                         │
│    ↓                                                                         │
│  RETURN RESPONSE TO USER                                                    │
└─────────────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════════════╗
║                        DATA FLOW IN EACH NODE                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

INPUT NODE STATE:
{
  "customer_id": "cust_001",
  "customer_name": "John Doe",
  "user_message": "I'm interested in electronics",
  "retrieved_memories": [],
  "customer_profile": null,
  "profile_summary": "",
  "llm_response": "",
  "memory_stored": false,
  "sentiment_analysis": "neutral"
}
         ↓ (after INPUT)
         ✓ Memory namespace initialized

MEMORY RETRIEVE NODE STATE:
{
  "retrieved_memories": [
    {
      "content": "Customer purchased iPhone 15 last month",
      "type": "purchase",
      "timestamp": "2024-01-10T15:30:00",
      "id": "mem_abc123"
    },
    ...
  ]
}

PROFILE BUILDER NODE STATE:
{
  "customer_profile": {
    "customer_id": "cust_001",
    "name": "John Doe",
    "preferences": ["electronics", "gadgets"],
    "purchase_history": [...],
    "issues_reported": [...],
    "sentiment_trend": "neutral",
    "interaction_count": 5,
    "total_spent": 2500.00
  },
  "profile_summary": "CUSTOMER PROFILE: John Doe..."
}

LLM RESPONSE NODE STATE:
{
  "llm_response": "Thank you for your interest, John! Based on your love 
                   for electronics and your recent iPhone 15 purchase, 
                   I'd like to recommend..."
}

SENTIMENT ANALYSIS NODE STATE:
{
  "sentiment_analysis": "positive"  # Updated from user message analysis
}

MEMORY STORE NODE STATE:
{
  "memory_stored": true,
  "last_interaction_summary": "Customer interested in electronics"
}

╔══════════════════════════════════════════════════════════════════════════════╗
║                       CUSTOMER PROFILE STRUCTURE                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

{
  "customer_id": "cust_001",
  "name": "John Doe",
  "email": "john@example.com",
  "preferences": ["electronics", "gadgets", "tech"],
  "purchase_history": [
    {
      "product_name": "iPhone 15",
      "amount": 999.00,
      "category": "electronics",
      "date": "2024-01-15T10:30:00",
      "details": {}
    }
  ],
  "issues_reported": [
    {
      "description": "Screen occasionally unresponsive",
      "category": "technical",
      "severity": "medium",
      "date": "2024-01-20T14:15:00",
      "resolved": false,
      "resolution": null
    }
  ],
  "sentiment_trend": "positive",
  "last_interaction_summary": "Asked about new tech products",
  "interaction_count": 5,
  "total_spent": 2500.00,
  "tags": ["VIP_Customer", "Tech_Enthusiast"],
  "created_at": "2024-01-10T08:00:00",
  "updated_at": "2024-01-25T16:45:00"
}

╔══════════════════════════════════════════════════════════════════════════════╗
║                   MEMORY SYSTEM OPERATIONS                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

SUPERMEMORY.AI INTEGRATION:
┌─────────────────────────────────┐
│  Create Namespace               │
│  POST /namespaces               │
│  → customer_001                 │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  Store Memory                   │
│  POST /memories                 │
│  ├─ namespace_id: customer_001  │
│  ├─ content: user message       │
│  ├─ type: customer_query        │
│  └─ metadata: {...}             │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  Retrieve Memories              │
│  POST /memories/search          │
│  ├─ namespace_id: customer_001  │
│  ├─ query: "electronics"        │
│  └─ limit: 5                    │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  Update Memory                  │
│  PUT /memories/{memory_id}      │
│  ├─ content: new content        │
│  └─ metadata: {...}             │
└─────────────────────────────────┘

LOCAL MEMORY FALLBACK:
{
  "customer_001": [
    {
      "id": 0,
      "content": "Customer message",
      "type": "customer_query",
      "metadata": {"timestamp": "2024-01-25T16:45:00", ...}
    },
    ...
  ]
}

╔══════════════════════════════════════════════════════════════════════════════╗
║                    EXAMPLE INTERACTION FLOW                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

STEP 1: User Input
┌────────────────────────────┐
│ Customer: "I need help     │
│ with my iPhone"            │
└────────────────────────────┘
         ↓
STEP 2: Memory Retrieval
┌────────────────────────────────────────┐
│ Retrieved Memories:                    │
│ • "Purchased iPhone 15 last month"     │
│ • "Complaint about screen"             │
│ • "Interested in tech support"         │
└────────────────────────────────────────┘
         ↓
STEP 3: Profile Building
┌────────────────────────────────────────┐
│ Profile Updated:                       │
│ • Add issue: "iPhone help needed"      │
│ • Tag: "technical_support"             │
│ • Sentiment: Extract from message      │
└────────────────────────────────────────┘
         ↓
STEP 4: LLM Response Generation
┌─────────────────────────────────────────────┐
│ Prompt Context:                             │
│ Customer Info: John Doe                     │
│ Purchase: iPhone 15 ($999)                  │
│ Issue: Screen unresponsive                  │
│ History: Prefers electronic products        │
│                                             │
│ ChatGPT Response:                           │
│ "Hi John! I see you purchased an iPhone 15  │
│ last month. I'm sorry to hear about the    │
│ screen issue. Let's troubleshoot..."       │
└─────────────────────────────────────────────┘
         ↓
STEP 5: Sentiment Analysis
┌────────────────────────────┐
│ Message Sentiment: NEGATIVE │
│ Issue: Complaint detected   │
│ Action: Update profile      │
└────────────────────────────┘
         ↓
STEP 6: Memory Storage
┌───────────────────────────────────────┐
│ Stored in Memory:                     │
│ • Customer Query                      │
│ • Agent Response                      │
│ • Sentiment: NEGATIVE                 │
│ • Timestamp: 2024-01-25T16:45:00     │
│ • Update: Interaction Count +1        │
└───────────────────────────────────────┘
         ↓
STEP 7: Return to User
┌─────────────────────────────────────────────┐
│ Agent: "Hi John! I see you purchased...     │
│ Let's help solve your screen issue..."      │
└─────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════════════╗
║                      PRODUCT RECOMMENDATION ENGINE                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

ALGORITHM:
1. Analyze purchase_history by category
2. Find most purchased categories
3. Retrieve complementary products
4. Add preference-based suggestions
5. Return top 5 unique recommendations

EXAMPLE:
Purchase History:
├─ iPhone 15 (electronics)
├─ AirPods Pro (electronics)  
└─ Lightning Cable (electronics)

Most Purchased: electronics (3 items)

Complementary Products:
├─ Phone cases
├─ Screen protectors
├─ Charging docks
├─ Headphone stands
└─ Tech accessories

Recommendations Output:
1. Phone accessories
2. Screen protectors
3. Charging stations
4. Tech gadgets
5. Wireless accessories

╔══════════════════════════════════════════════════════════════════════════════╗
║                         SYSTEM CAPABILITIES                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

✓ Multi-customer support with isolated memory namespaces
✓ Long-term memory with semantic search
✓ Automatic sentiment tracking
✓ Dynamic preference extraction
✓ Purchase pattern analysis
✓ Intelligent product recommendations
✓ Issue/complaint tracking
✓ Personalized response generation
✓ Real-time profile updates
✓ Conversation history management
✓ VIP/tagging system
✓ Analytics and insights
✓ Scalable architecture

"""
    
    return workflow


if __name__ == "__main__":
    print(visualize_workflow())
    
    # Save to file
    with open("WORKFLOW_DIAGRAM.txt", "w") as f:
        f.write(visualize_workflow())
    
    print("\n✅ Workflow diagram saved to WORKFLOW_DIAGRAM.txt")
