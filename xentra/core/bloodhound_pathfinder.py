import yaml
from neo4j import GraphDatabase
from xentra.core.thehive_client import TheHiveClient
from xentra.utils.logger import get_logger

logger = get_logger("BloodHoundPathfinder")

EDGE_RECOMMENDATIONS = {
    "MemberOf": "Review group membership; enforce tiered admin model.",
    "AdminTo": "Remove unnecessary local admin rights; use LAPS/PAM.",
    "HasSession": "Investigate session; rotate credentials if unexpected.",
    "GenericAll": "Restrict GenericAll ACE; apply least-privilege ACLs.",
    "GenericWrite": "Restrict GenericWrite ACE; apply least-privilege ACLs.",
    "WriteDacl": "Remove WriteDacl permission.",
    "WriteOwner": "Remove WriteOwner permission.",
    "ForceChangePassword": "Restrict to authorized reset workflows only.",
    "AddMember": "Restrict AddMember permission to privileged groups.",
    "Owns": "Review object ownership.",
}
DEFAULT_RECOMMENDATION = "Review this relationship type; apply least-privilege remediation."


class BloodHoundPathfinder:
    def __init__(self, config_path="xentra/config/settings.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        bh = self.config["bloodhound"]
        self.driver = GraphDatabase.driver(
            bh["neo4j_uri"], auth=(bh["neo4j_user"], bh["neo4j_password"])
        )
        self.max_path_length = bh.get("max_path_length", 4)
        self.max_paths = bh.get("max_paths", 25)
        self.thehive = TheHiveClient(api_key=self.config["thehive"]["api_key"])

    def get_paths_to_domain_admins(self):
        query = """
        MATCH p=shortestPath((u:User)-[*1..%d]->(g:Group))
        WHERE toUpper(g.name) CONTAINS 'DOMAIN ADMINS' AND u.name <> g.name
        RETURN p LIMIT %d
        """ % (self.max_path_length, self.max_paths)
        paths = []
        with self.driver.session() as session:
            for record in session.run(query):
                p = record["p"]
                paths.append({
                    "nodes": [n.get("name", "UNKNOWN") for n in p.nodes],
                    "rels": [r.type for r in p.relationships],
                })
        return paths

    def build_attack_path_string(self, path):
        parts = [path["nodes"][0]]
        for rel, node in zip(path["rels"], path["nodes"][1:]):
            parts.append(f"-> {rel} -> {node}")
        return " ".join(parts)

    def build_recommendations(self, path):
        seen = []
        for rel in path["rels"]:
            rec = EDGE_RECOMMENDATIONS.get(rel, DEFAULT_RECOMMENDATION)
            if rec not in seen:
                seen.append(rec)
        return seen

    def severity_for_path(self, path):
        risky = {"GenericAll", "GenericWrite", "WriteDacl", "WriteOwner",
                 "ForceChangePassword", "AddMember", "Owns"}
        if any(r in risky for r in path["rels"]):
            return "Critical"
        if len(path["rels"]) == 1 and path["rels"][0] == "MemberOf":
            return "Medium"
        return "High"

    def run(self):
        paths = self.get_paths_to_domain_admins()
        logger.info(f"Found {len(paths)} path(s) to Domain Admins.")

        seen_sigs, created, tickets = set(), 0, []
        for path in paths:
            sig = tuple(path["nodes"])
            if sig in seen_sigs:
                continue
            seen_sigs.add(sig)

            ticket = {
                "title": f"Attack path to Domain Admins: {path['nodes'][0]}",
                "attack_path": self.build_attack_path_string(path),
                "recommended_actions": self.build_recommendations(path),
                "severity": self.severity_for_path(path),
                "cve_id": "N/A",
                "owner": "wado",
            }
            status, result = self.thehive.create_case(ticket)
            if status == 201:
                created += 1
            tickets.append(ticket)
            logger.info(f"[{status}] {path['nodes'][0]} -> {path['nodes'][-1]} | severity={ticket['severity']}")

        self.driver.close()
        logger.info(f"Done. {created} case(s) created out of {len(seen_sigs)} unique path(s).")
        return tickets
