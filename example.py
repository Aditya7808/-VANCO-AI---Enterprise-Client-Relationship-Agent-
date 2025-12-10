"""
Example script demonstrating the CRM Agent
"""
import os
from dotenv import load_dotenv

from src.agent import CRMAgent
from src.profiles import ProfileBuilder

load_dotenv()


def main():
    """Run example customer interactions"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not set in .env")
        print("Please copy .env.example to .env and add your OpenAI API key")
        return

    print("🚀 Initializing Customer Relationship AI Agent...\n")
    
    # Initialize agent
    agent = CRMAgent(openai_api_key=api_key, use_local_memory=True)

    # Example customers
    customers = [
        ("cust_001", "Alice Johnson", "alice@example.com"),
        ("cust_002", "Bob Smith", "bob@example.com"),
        ("cust_003", "Carol White", "carol@example.com"),
    ]

    # Add sample customers
    print("📝 Adding sample customers...\n")
    for customer_id, name, email in customers:
        agent.profile_builder.create_profile(customer_id, name, email)
        print(f"✅ Added customer: {name} ({customer_id})")

    # Add some sample purchases
    print("\n💳 Adding sample purchase history...\n")
    agent.profile_builder.add_purchase("cust_001", "iPhone 15", 999, "electronics")
    agent.profile_builder.add_purchase("cust_001", "AirPods Pro", 249, "electronics")
    agent.profile_builder.add_purchase("cust_002", "Running Shoes", 120, "sports")
    agent.profile_builder.add_purchase("cust_002", "Yoga Mat", 35, "sports")
    agent.profile_builder.add_purchase("cust_003", "Coffee Maker", 89, "home")

    print("✅ Added sample purchases")

    # Example interactions
    interactions = [
        ("cust_001", "Alice Johnson", "I'm interested in new tech gadgets and accessories"),
        ("cust_001", "Alice Johnson", "My AirPods are having connectivity issues"),
        ("cust_002", "Bob Smith", "Can you recommend some sports equipment for beginners?"),
        ("cust_003", "Carol White", "I want to upgrade my kitchen appliances"),
    ]

    # Process interactions
    print("\n" + "="*70)
    print("🤖 PROCESSING CUSTOMER INTERACTIONS")
    print("="*70 + "\n")

    for customer_id, name, message in interactions:
        response = agent.process_customer_message(
            customer_id=customer_id,
            customer_name=name,
            message=message
        )

        print(f"\n{'─'*70}")
        print(f"Customer: {name}")
        print(f"Message: {message}")
        print(f"{'─'*70}")
        print(f"Agent Response:\n{response}")
        print()

    # Display customer profiles
    print("\n" + "="*70)
    print("📊 CUSTOMER PROFILES SUMMARY")
    print("="*70 + "\n")

    for customer_id, name, _ in customers:
        print(agent.profile_builder.get_profile_summary(customer_id))
        print()

    # Show recommendations
    print("="*70)
    print("🎯 PRODUCT RECOMMENDATIONS")
    print("="*70 + "\n")

    for customer_id, name, _ in customers:
        recommendations = agent.profile_builder.recommend_products(customer_id)
        print(f"{name}:")
        for rec in recommendations:
            print(f"  • {rec}")
        print()

    print("✅ Example completed successfully!")


if __name__ == "__main__":
    main()
