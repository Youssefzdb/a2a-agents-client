# A2A Agents Client Library

Python client for communicating with 25+ A2A (Agent-to-Agent) protocol agents.

## Installation

```bash
pip install requests
```

## Quick Start

```python
from a2a_client import A2AClient

client = A2AClient()

# List all available agents
agents = client.list_agents()

# Call an agent
response = client.call_agent(
    agent_url="http://47.253.174.153/",
    message="Hello!"
)
print(response)
```

## API Key Format

Some agents require an API key:

```python
client = A2AClient(api_key="a2a_your_key_here")
```

## Available Agents

| Agent | URL | Specialization |
|-------|-----|----------------|
| EVO-AI | http://47.253.174.153/ | Distributed LLM |
| Practice Negotiation | http://18.222.26.118:8082/a2a | Negotiation practice |
| Mongo Stack Gen | https://rabbitmq-elasticsearch-postgres-stack-generator-mongo.getvda.ai/a2a/ | Docker-compose |
| Postgres+Mongo Stack | https://rabbitmq-postgres-mongodb-stack-generator.getvda.ai/a2a/ | Docker-compose |
| Degenscan Intel | https://intel.degenscan.io/a2a | Market intelligence |
| Feeless402 | https://feeless402.com/a2a | x402 pricing |
| MusedIn | https://musedin.com/a2a | Job network |
| Astro Agents | https://astro-agent.dev/a2a | Astrology |
| Overwing | https://overwing.ai/a2a | Content safety |
| Sanctum Beacon | https://sanctum-beacon.onrender.com/a2a | Community |
| Increatus Tools | https://studio.tail7ba746.ts.net/agents/tools/a2a | Calculators |
| Burs-IA | https://burs-ia.com/a2a | Agent station |
| PHION | https://phion.systems/a2a | Trust infrastructure |
| + 12 more | ... | ... |

## Usage Examples

### Basic Message

```python
import requests

def call_agent(agent_url, message):
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "message/send",
        "params": {
            "message": {
                "messageId": "unique-id",
                "role": "user",
                "parts": [
                    {"kind": "text", "text": message}
                ]
            }
        }
    }
    
    response = requests.post(
        agent_url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    return response.json()
```

### With Skill (Data Part)

```python
def call_skill(agent_url, skill_id, input_data):
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "message/send",
        "params": {
            "message": {
                "messageId": "unique-id",
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
    
    response = requests.post(
        agent_url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    return response.json()
```

### Get Agent Card

```python
def get_agent_card(agent_url):
    # Try common paths
    for path in ["/.well-known/agent-card.json", "/a2a/.well-known/agent-card.json"]:
        url = agent_url.rstrip("/") + path
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    return None
```

## A2A Protocol

### Request Format

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "message/send",
  "params": {
    "message": {
      "messageId": "unique-id",
      "role": "user",
      "parts": [
        {"kind": "text", "text": "Hello"}
      ]
    }
  }
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "kind": "task",
    "id": "task-id",
    "contextId": "context-id",
    "status": {
      "state": "completed",
      "message": {
        "parts": [
          {"kind": "text", "text": "Agent response"}
        ]
      }
    }
  }
}
```

## Error Handling

```python
try:
    response = call_agent(agent_url, message)
    if "error" in response:
        print(f"Error: {response['error']}")
    else:
        result = response.get("result", {})
        # Process result
except Exception as e:
    print(f"Connection error: {e}")
```

## Rate Limits

Some agents have rate limits:
- **Overwing**: 10 free evaluations/day
- **Degenscan**: Paid per call (x402 USDC)
- **Stack Generators**: No rate limit

## License

MIT
