import json
import requests

class TheHiveClient:
    def __init__(self, url="http://localhost:9000", api_key="PASTE_YOUR_API_KEY_HERE"):
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def create_case(self, ticket):
        payload = {
            "title": ticket["title"],
            "description": f"Attack path: {ticket['attack_path']}\nRecommended: {', '.join(ticket['recommended_actions'])}",
            "severity": 3 if ticket["severity"] == "Critical" else 2,
            "tags": [ticket.get("cve_id", "N/A"), ticket.get("owner", "unassigned")]
        }
        response = requests.post(f"{self.url}/api/v1/case", headers=self.headers, json=payload)
        return response.status_code, response.json()

    def push_all_tickets(self, tickets_path="engine/generated-tickets.json"):
        with open(tickets_path) as f:
            tickets = json.load(f)
        for t in tickets:
            status, result = self.create_case(t)
            print(f"{t.get('ticket_id', '?')}: HTTP {status}")
