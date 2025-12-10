"""
VANCO AI - Enterprise Client Profile Management

Manages client profiles for Vanco AI enterprise customers including:
- AI & Machine Learning projects
- Full-Stack Product Engineering
- Analytics & Data Engineering
- Cloud & DevOps solutions
- Generative AI implementations
"""
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel


class CustomerProfile(BaseModel):
    """Enterprise Client Profile for Vanco AI"""
    customer_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None  # Enterprise company name
    company_type: Optional[str] = None  # Hospital, Bank, Retail, etc.
    industry: Optional[str] = None  # Client industry vertical
    preferences: List[str] = []  # AI/Tech interests
    project_history: List[Dict[str, Any]] = []  # Past AI projects with Vanco
    proposed_projects: List[Dict[str, Any]] = []  # Projects being discussed
    scheduled_meetings: List[Dict[str, Any]] = []  # Upcoming meetings
    issues_reported: List[Dict[str, Any]] = []
    sentiment_trend: str = "neutral"  # positive, neutral, negative
    last_interaction_summary: str = ""
    interaction_count: int = 0
    project_value: float = 0.0  # Total project value
    estimated_budget: Optional[str] = None  # Client budget range
    tags: List[str] = []
    service_interests: List[str] = []  # Vanco services of interest
    key_requirements: List[str] = []  # Specific requirements mentioned
    decision_timeline: Optional[str] = None  # When they plan to decide
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary"""
        return self.dict()

    def to_json(self) -> str:
        """Convert profile to JSON"""
        return self.json()


class ProfileBuilder:
    """Builds and updates enterprise client profiles for Vanco AI"""

    # Vanco AI Service Categories
    SERVICE_CATEGORIES = [
        "AI & Machine Learning",
        "Full-Stack Product Engineering",
        "Analytics & Data Engineering",
        "Cloud & DevOps",
        "Generative AI (LLMs, VLMs)",
        "Computer Vision",
        "NLP & Conversational AI",
        "Predictive Analytics",
        "Workforce Augmentation",
        "AI Consulting"
    ]

    # Industry verticals Vanco AI serves
    INDUSTRY_VERTICALS = [
        "Automotive",
        "Healthcare",
        "Finance & Banking",
        "Retail & E-commerce",
        "Manufacturing",
        "Logistics & Supply Chain",
        "Technology",
        "Energy & Utilities",
        "Telecommunications"
    ]

    def __init__(self):
        """Initialize profile builder for Vanco AI clients"""
        self.profiles: Dict[str, CustomerProfile] = {}

    def create_profile(
        self,
        customer_id: str,
        name: str,
        email: Optional[str] = None,
        company: Optional[str] = None,
        industry: Optional[str] = None
    ) -> CustomerProfile:
        """Create a new enterprise client profile"""
        profile = CustomerProfile(
            customer_id=customer_id,
            name=name,
            email=email,
            company=company,
            industry=industry,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        self.profiles[customer_id] = profile
        return profile

    def get_profile(self, customer_id: str) -> Optional[CustomerProfile]:
        """Get existing profile or create new one"""
        return self.profiles.get(customer_id)

    def update_preferences(self, customer_id: str, preferences: List[str]) -> bool:
        """Update customer preferences"""
        if customer_id not in self.profiles:
            return False

        profile = self.profiles[customer_id]
        profile.preferences = list(set(profile.preferences + preferences))
        profile.updated_at = datetime.now().isoformat()
        return True

    def add_project(
        self,
        customer_id: str,
        project_name: str,
        value: float,
        service_category: str,
        status: str = "in_progress",
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Add AI project to client history"""
        if customer_id not in self.profiles:
            return False

        profile = self.profiles[customer_id]
        project = {
            "project_name": project_name,
            "value": value,
            "service_category": service_category,
            "status": status,
            "date": datetime.now().isoformat(),
            "details": details or {}
        }
        profile.project_history.append(project)
        profile.project_value += value
        profile.updated_at = datetime.now().isoformat()
        return True

    # Legacy method for backward compatibility
    def add_purchase(
        self,
        customer_id: str,
        product_name: str,
        amount: float,
        category: str,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Legacy method - redirects to add_project"""
        return self.add_project(customer_id, product_name, amount, category, "completed", details)

    def update_company_info(
        self,
        customer_id: str,
        company: Optional[str] = None,
        company_type: Optional[str] = None,
        industry: Optional[str] = None
    ) -> bool:
        """Update company information for client"""
        if customer_id not in self.profiles:
            return False

        profile = self.profiles[customer_id]
        if company:
            profile.company = company
        if company_type:
            profile.company_type = company_type
        if industry:
            profile.industry = industry
        profile.updated_at = datetime.now().isoformat()
        return True

    def add_scheduled_meeting(
        self,
        customer_id: str,
        meeting_date: str,
        meeting_time: str,
        purpose: str,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Add a scheduled meeting to client profile"""
        if customer_id not in self.profiles:
            return False

        profile = self.profiles[customer_id]
        meeting = {
            "date": meeting_date,
            "time": meeting_time,
            "purpose": purpose,
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
            "details": details or {}
        }
        profile.scheduled_meetings.append(meeting)
        profile.updated_at = datetime.now().isoformat()
        return True

    def add_proposed_project(
        self,
        customer_id: str,
        project_name: str,
        project_type: str,
        description: str,
        estimated_value: Optional[float] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Add a proposed/discussed project to client profile"""
        if customer_id not in self.profiles:
            return False

        profile = self.profiles[customer_id]
        project = {
            "project_name": project_name,
            "project_type": project_type,
            "description": description,
            "estimated_value": estimated_value,
            "status": "proposed",
            "created_at": datetime.now().isoformat(),
            "details": details or {}
        }
        profile.proposed_projects.append(project)
        profile.updated_at = datetime.now().isoformat()
        return True

    def update_service_interests(self, customer_id: str, services: List[str]) -> bool:
        """Update client service interests"""
        if customer_id not in self.profiles:
            return False

        profile = self.profiles[customer_id]
        profile.service_interests = list(set(profile.service_interests + services))
        profile.updated_at = datetime.now().isoformat()
        return True

    def add_key_requirement(self, customer_id: str, requirement: str) -> bool:
        """Add a key requirement mentioned by client"""
        if customer_id not in self.profiles:
            return False

        profile = self.profiles[customer_id]
        if requirement not in profile.key_requirements:
            profile.key_requirements.append(requirement)
        profile.updated_at = datetime.now().isoformat()
        return True

    def update_contact_info(
        self,
        customer_id: str,
        email: Optional[str] = None,
        phone: Optional[str] = None
    ) -> bool:
        """Update client contact information"""
        if customer_id not in self.profiles:
            return False

        profile = self.profiles[customer_id]
        if email:
            profile.email = email
        if phone:
            profile.phone = phone
        profile.updated_at = datetime.now().isoformat()
        return True

    def add_issue(
        self,
        customer_id: str,
        issue_description: str,
        category: str,
        severity: str = "medium",
        resolution: Optional[str] = None
    ) -> bool:
        """Add reported issue to profile"""
        if customer_id not in self.profiles:
            return False

        profile = self.profiles[customer_id]
        issue = {
            "description": issue_description,
            "category": category,
            "severity": severity,
            "resolution": resolution,
            "date": datetime.now().isoformat(),
            "resolved": resolution is not None
        }
        profile.issues_reported.append(issue)
        profile.updated_at = datetime.now().isoformat()
        return True

    def update_sentiment(self, customer_id: str, sentiment: str) -> bool:
        """Update customer sentiment trend"""
        if customer_id not in self.profiles:
            return False

        valid_sentiments = ["positive", "neutral", "negative"]
        if sentiment not in valid_sentiments:
            return False

        profile = self.profiles[customer_id]
        profile.sentiment_trend = sentiment
        profile.updated_at = datetime.now().isoformat()
        return True

    def update_last_interaction(self, customer_id: str, summary: str) -> bool:
        """Update last interaction summary"""
        if customer_id not in self.profiles:
            return False

        profile = self.profiles[customer_id]
        profile.last_interaction_summary = summary
        profile.interaction_count += 1
        profile.updated_at = datetime.now().isoformat()
        return True

    def add_tag(self, customer_id: str, tag: str) -> bool:
        """Add tag to customer profile"""
        if customer_id not in self.profiles:
            return False

        profile = self.profiles[customer_id]
        if tag not in profile.tags:
            profile.tags.append(tag)
        profile.updated_at = datetime.now().isoformat()
        return True

    def get_profile_summary(self, customer_id: str) -> str:
        """Get human-readable enterprise client profile summary"""
        if customer_id not in self.profiles:
            return "No profile found"

        profile = self.profiles[customer_id]
        
        # Build comprehensive summary
        summary = f"""
================================================================================
                    ENTERPRISE CLIENT PROFILE
================================================================================

BASIC INFORMATION
-----------------
Client Name: {profile.name}
Client ID: {profile.customer_id}
Company: {profile.company or "Not specified yet"}
Company Type: {profile.company_type or "Not specified yet"}
Industry: {profile.industry or "Not specified yet"}
Email: {profile.email or "Not provided"}
Phone: {profile.phone or "Not provided"}

ENGAGEMENT METRICS
------------------
Sentiment: {profile.sentiment_trend.upper()}
Total Interactions: {profile.interaction_count}
Total Project Value: ${profile.project_value:,.2f}
Estimated Budget: {profile.estimated_budget or "Not discussed"}
Decision Timeline: {profile.decision_timeline or "Not specified"}

AI/TECH INTERESTS
-----------------
{', '.join(profile.preferences) if profile.preferences else "No interests identified yet"}

SERVICE INTERESTS
-----------------
{', '.join(profile.service_interests) if profile.service_interests else "No specific services discussed yet"}

KEY REQUIREMENTS
----------------
"""
        if profile.key_requirements:
            for req in profile.key_requirements:
                summary += f"  * {req}\n"
        else:
            summary += "No specific requirements captured yet\n"

        summary += """
SCHEDULED MEETINGS
------------------
"""
        if profile.scheduled_meetings:
            for meeting in profile.scheduled_meetings:
                summary += f"  * {meeting['date']} at {meeting['time']} - {meeting['purpose']} [{meeting['status']}]\n"
        else:
            summary += "No meetings scheduled\n"

        summary += """
PROPOSED PROJECTS
-----------------
"""
        if profile.proposed_projects:
            for project in profile.proposed_projects:
                value_str = f"${project['estimated_value']:,.2f}" if project.get('estimated_value') else "TBD"
                summary += f"  * {project['project_name']} ({project['project_type']})\n"
                summary += f"    Description: {project['description']}\n"
                summary += f"    Estimated Value: {value_str} | Status: {project['status']}\n"
        else:
            summary += "No projects proposed yet\n"

        summary += """
COMPLETED PROJECTS
------------------
"""
        if profile.project_history:
            for project in profile.project_history[-5:]:
                status_icon = "[DONE]" if project.get('status') == 'completed' else "[IN PROGRESS]"
                summary += f"  {status_icon} {project['project_name']}: ${project['value']:,.2f}\n"
                summary += f"          Category: {project['service_category']} | Date: {project['date'][:10]}\n"
        else:
            summary += "No completed projects yet\n"

        if profile.issues_reported:
            summary += """
SUPPORT REQUESTS
----------------
"""
            for issue in profile.issues_reported[-3:]:
                status = "[RESOLVED]" if issue['resolved'] else "[OPEN]"
                summary += f"  {status} {issue['description']}\n"

        summary += f"""
TAGS
----
{', '.join(profile.tags) if profile.tags else "No tags"}

LAST INTERACTION
----------------
{profile.last_interaction_summary or "No previous interaction"}

================================================================================
"""
        return summary

    def recommend_services(self, customer_id: str) -> List[str]:
        """Generate AI service recommendations based on project history and interests"""
        if customer_id not in self.profiles:
            return []

        profile = self.profiles[customer_id]
        recommendations = []

        # Recommendation logic based on project patterns
        service_categories = {}
        for project in profile.project_history:
            category = project['service_category']
            service_categories[category] = service_categories.get(category, 0) + 1

        # Suggest complementary AI services based on past projects
        service_suggestions = {
            "AI & Machine Learning": ["Predictive Analytics", "Computer Vision", "NLP & Conversational AI"],
            "Generative AI (LLMs, VLMs)": ["AI Consulting", "Full-Stack Product Engineering", "Workforce Augmentation"],
            "Full-Stack Product Engineering": ["Cloud & DevOps", "Analytics & Data Engineering", "AI & Machine Learning"],
            "Analytics & Data Engineering": ["Predictive Analytics", "AI & Machine Learning", "Cloud & DevOps"],
            "Cloud & DevOps": ["Full-Stack Product Engineering", "Analytics & Data Engineering", "AI & Machine Learning"],
            "Computer Vision": ["AI & Machine Learning", "Generative AI (LLMs, VLMs)", "Full-Stack Product Engineering"],
            "NLP & Conversational AI": ["Generative AI (LLMs, VLMs)", "AI Consulting", "Full-Stack Product Engineering"],
            "Predictive Analytics": ["Analytics & Data Engineering", "AI & Machine Learning", "AI Consulting"],
            "Workforce Augmentation": ["AI Consulting", "Full-Stack Product Engineering", "Generative AI (LLMs, VLMs)"],
            "AI Consulting": ["Full-Stack Product Engineering", "Generative AI (LLMs, VLMs)", "AI & Machine Learning"]
        }

        for category, count in sorted(service_categories.items(), key=lambda x: x[1], reverse=True)[:2]:
            if category in service_suggestions:
                recommendations.extend(service_suggestions[category])

        # Add interest-based recommendations
        for interest in profile.preferences + profile.service_interests:
            if interest not in recommendations and interest in self.SERVICE_CATEGORIES:
                recommendations.append(interest)

        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)

        return unique_recommendations[:5]

    # Legacy method for backward compatibility
    def recommend_products(self, customer_id: str) -> List[str]:
        """Legacy method - redirects to recommend_services"""
        return self.recommend_services(customer_id)

    def export_profile(self, customer_id: str) -> Dict[str, Any]:
        """Export profile as dictionary"""
        if customer_id not in self.profiles:
            return {}

        return self.profiles[customer_id].to_dict()

    def import_profile(self, profile_data: Dict[str, Any]) -> bool:
        """Import profile from dictionary"""
        try:
            profile = CustomerProfile(**profile_data)
            self.profiles[profile.customer_id] = profile
            return True
        except Exception as e:
            print(f"Error importing profile: {e}")
            return False
