"""
Memory module for storing and retrieving customer interactions using Supermemory.ai
"""
import os
import requests
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel


class MemoryItem(BaseModel):
    """Model for memory items"""
    content: str
    metadata: Dict[str, Any]
    timestamp: str


class SupermemoryManager:
    """Manager for Supermemory.ai vector memory storage"""

    def __init__(self, api_key: str, base_url: str = "https://api.supermemory.ai"):
        """Initialize Supermemory manager"""
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def create_memory_namespace(self, customer_id: str) -> bool:
        """Create a unique namespace for each customer"""
        try:
            endpoint = f"{self.base_url}/namespaces"
            data = {
                "namespace_id": f"customer_{customer_id}",
                "description": f"Memory namespace for customer {customer_id}"
            }
            response = requests.post(endpoint, headers=self.headers, json=data, timeout=10)
            return response.status_code in [200, 201, 409]  # 409 = already exists
        except Exception as e:
            print(f"Error creating namespace: {e}")
            return False

    def store_memory(
        self,
        customer_id: str,
        content: str,
        memory_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store customer memory/interaction in Supermemory.ai"""
        try:
            if metadata is None:
                metadata = {}

            endpoint = f"{self.base_url}/memories"
            memory_data = {
                "namespace_id": f"customer_{customer_id}",
                "content": content,
                "type": memory_type,
                "metadata": {
                    **metadata,
                    "timestamp": datetime.now().isoformat(),
                    "customer_id": customer_id
                }
            }

            response = requests.post(
                endpoint,
                headers=self.headers,
                json=memory_data,
                timeout=10
            )
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"Error storing memory: {e}")
            return False

    def retrieve_memories(
        self,
        customer_id: str,
        query: str,
        limit: int = 5,
        memory_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant memories based on semantic search"""
        try:
            endpoint = f"{self.base_url}/memories/search"
            search_params = {
                "namespace_id": f"customer_{customer_id}",
                "query": query,
                "limit": limit
            }
            if memory_type:
                search_params["type"] = memory_type

            response = requests.post(
                endpoint,
                headers=self.headers,
                json=search_params,
                timeout=10
            )

            if response.status_code == 200:
                return response.json().get("results", [])
            return []
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []

    def get_all_memories(self, customer_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get all memories for a customer"""
        try:
            endpoint = f"{self.base_url}/memories"
            params = {
                "namespace_id": f"customer_{customer_id}",
                "limit": limit
            }
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                return response.json().get("memories", [])
            return []
        except Exception as e:
            print(f"Error getting all memories: {e}")
            return []

    def delete_memory(self, customer_id: str, memory_id: str) -> bool:
        """Delete a specific memory"""
        try:
            endpoint = f"{self.base_url}/memories/{memory_id}"
            params = {"namespace_id": f"customer_{customer_id}"}
            response = requests.delete(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            return response.status_code in [200, 204]
        except Exception as e:
            print(f"Error deleting memory: {e}")
            return False

    def update_memory(
        self,
        customer_id: str,
        memory_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update an existing memory"""
        try:
            endpoint = f"{self.base_url}/memories/{memory_id}"
            update_data = {
                "namespace_id": f"customer_{customer_id}",
                "content": content,
                "metadata": metadata or {}
            }
            response = requests.put(
                endpoint,
                headers=self.headers,
                json=update_data,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating memory: {e}")
            return False


class LocalMemoryManager:
    """Fallback local memory manager for development/testing without Supermemory.ai"""

    def __init__(self):
        """Initialize local memory storage"""
        self.memories: Dict[str, List[Dict[str, Any]]] = {}

    def create_memory_namespace(self, customer_id: str) -> bool:
        """Create a namespace"""
        if customer_id not in self.memories:
            self.memories[customer_id] = []
        return True

    def store_memory(
        self,
        customer_id: str,
        content: str,
        memory_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store memory locally"""
        self.create_memory_namespace(customer_id)
        memory_entry = {
            "id": len(self.memories[customer_id]),
            "content": content,
            "type": memory_type,
            "metadata": {
                **(metadata or {}),
                "timestamp": datetime.now().isoformat()
            }
        }
        self.memories[customer_id].append(memory_entry)
        return True

    def retrieve_memories(
        self,
        customer_id: str,
        query: str,
        limit: int = 5,
        memory_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve memories (simple keyword matching)"""
        if customer_id not in self.memories:
            return []

        memories = self.memories[customer_id]
        if memory_type:
            memories = [m for m in memories if m["type"] == memory_type]

        # Simple keyword matching
        query_lower = query.lower()
        relevant = [m for m in memories if query_lower in m["content"].lower()]
        return relevant[:limit]

    def get_all_memories(self, customer_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get all memories"""
        if customer_id not in self.memories:
            return []
        return self.memories[customer_id][-limit:]

    def delete_memory(self, customer_id: str, memory_id: str) -> bool:
        """Delete memory"""
        if customer_id in self.memories:
            self.memories[customer_id] = [
                m for m in self.memories[customer_id] if m.get("id") != int(memory_id)
            ]
            return True
        return False

    def update_memory(
        self,
        customer_id: str,
        memory_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update memory"""
        if customer_id in self.memories:
            for memory in self.memories[customer_id]:
                if memory.get("id") == int(memory_id):
                    memory["content"] = content
                    if metadata:
                        memory["metadata"].update(metadata)
                    return True
        return False
