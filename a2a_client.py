#!/usr/bin/env python3
"""
A2A Agents Client Library
Python client for Agent-to-Agent protocol communication.
"""

import json
import requests
from typing import Optional, Dict, Any


class A2AClient:
    """Client for communicating with A2A protocol agents."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        })
    
    def list_agents(self) -> list:
        """List all available agents (requires agent-router.org API key)."""
        if not self.api_key:
            return []
        
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "discover_agents",
                "arguments": {"query": "", "limit": 50}
            }
        }
        
        response = self.session.post(
            f"https://www.agent-router.org/mcp?apiKey={self.api_key}",
            json=payload,
            timeout=30
        )
        return response.json()
    
    def call_agent(
        self,
        agent_url: str,
        message: str,
        context_id: Optional[str] = None,
        task_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a message to an A2A agent.
        
        Args:
            agent_url: The agent's A2A endpoint URL
            message: Text message to send
            context_id: Optional context ID for multi-turn conversations
            task_id: Optional task ID to continue existing task
        
        Returns:
            Agent response dictionary
        """
        msg = {
            "messageId": f"msg-{id(message)}",
            "role": "user",
            "parts": [{"kind": "text", "text": message}]
        }
        
        if context_id:
            msg["contextId"] = context_id
        if task_id:
            msg["taskId"] = task_id
        
        payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "message/send",
            "params": {"message": msg}
        }
        
        response = self.session.post(
            agent_url,
            json=payload,
            timeout=30
        )
        return response.json()
    
    def call_skill(
        self,
        agent_url: str,
        skill_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call a specific skill on an agent.
        
        Args:
            agent_url: The agent's A2A endpoint URL
            skill_id: Skill identifier
            input_data: Skill input parameters
        
        Returns:
            Agent response dictionary
        """
        payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "message/send",
            "params": {
                "message": {
                    "messageId": f"skill-{id(input_data)}",
                    "role": "user",
                    "parts": [
                        {
                            "kind": "data",
                            "data": {
                                "skill": skill_id,
                                "input": input_data
                            }
                        }
                    ]
                }
            }
        }
        
        response = self.session.post(
            agent_url,
            json=payload,
            timeout=30
        )
        return response.json()
    
    def get_agent_card(self, agent_url: str) -> Optional[Dict[str, Any]]:
        """
        Fetch agent card metadata.
        
        Args:
            agent_url: The agent's A2A endpoint URL
        
        Returns:
            Agent card dictionary or None
        """
        base = agent_url.rstrip("/")
        paths = [
            "/.well-known/agent-card.json",
            "/a2a/.well-known/agent-card.json"
        ]
        
        for path in paths:
            try:
                response = requests.get(base + path, timeout=10)
                if response.status_code == 200:
                    return response.json()
            except Exception:
                continue
        
        return None
    
    @staticmethod
    def extract_response(result: Dict[str, Any]) -> str:
        """
        Extract text response from agent result.
        
        Args:
            result: Full agent response
        
        Returns:
            Extracted text content
        """
        # Handle different response formats
        if "result" in result:
            r = result["result"]
        else:
            r = result
        
        # Try parts
        parts = r.get("parts", [])
        if parts:
            texts = [p.get("text", "") for p in parts if p.get("kind") == "text"]
            if texts:
                return "\n".join(texts)
        
        # Try status.message.parts
        status = r.get("status", {})
        msg = status.get("message", {})
        parts = msg.get("parts", [])
        if parts:
            texts = [p.get("text", "") for p in parts if p.get("kind") == "text"]
            if texts:
                return "\n".join(texts)
        
        # Try artifacts
        artifacts = r.get("artifacts", [])
        if artifacts:
            texts = []
            for art in artifacts:
                for p in art.get("parts", []):
                    if p.get("kind") == "text":
                        texts.append(p.get("text", ""))
            if texts:
                return "\n".join(texts)
        
        return json.dumps(r, indent=2)


# Pre-configured agent URLs
AGENTS = {
    "evo-ai": "http://47.253.174.153/",
    "negotiation": "http://18.222.26.118:8082/a2a",
    "mongo-stack": "https://rabbitmq-elasticsearch-postgres-stack-generator-mongo.getvda.ai/a2a/",
    "postgres-mongo-stack": "https://rabbitmq-postgres-mongodb-stack-generator.getvda.ai/a2a/",
    "es-mongo-redis": "https://elasticsearch-mongodb-redis-stack-generator-el-d8f067.getvda.ai/a2a/",
    "es-redis": "https://elasticsearch-redis-stack-generator-elasticsea-588e3e.getvda.ai/a2a/",
    "degenscan": "https://intel.degenscan.io/a2a",
    "feeless402": "https://feeless402.com/a2a",
    "musedin": "https://musedin.com/a2a",
    "astro": "https://astro-agent.dev/a2a",
    "overwing": "https://overwing.ai/a2a",
    "sanctum": "https://sanctum-beacon.onrender.com/a2a",
    "increatus": "https://studio.tail7ba746.ts.net/agents/tools/a2a",
    "burs-ia": "https://burs-ia.com/a2a",
    "phion": "https://phion.systems/a2a",
    "ops-control": "https://tkoqkknsezxavtxfywkm.supabase.co/functions/v1/agent402-register-origin-shim",
    "smalltalk": "http://18.222.26.118:47831/a2a",
}


if __name__ == "__main__":
    # Quick test
    client = A2AClient()
    
    print("Testing EVO-AI agent...")
    response = client.call_agent(
        agent_url=AGENTS["evo-ai"],
        message="Hello!"
    )
    print(client.extract_response(response))
