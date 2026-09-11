"""
XENTRA - BloodHound Path Extraction -> TheHive Case Automation
"""

from neo4j import GraphDatabase
from xentra.core.thehive_client import TheHiveClient

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "bh123"

THEHIVE_API_KEY = "H80wR64YmDY/Edzp2sw6SLFHC5gBd2xW"

MAX_PATH_LENGTH = 4
MAX_PATHS = 25

EDGE_RECOMMENDATIONS = {
    "MemberOf": "Review group membership; enforce tiered admin model to limit standing privileged group membership.",
    "AdminTo": "Remove unnecessary local admin rights; use LAPS or PAM for just-in-time local admin access.",
    "HasSession": "Investigate why this session exists; rotate credentials if session was unexpected.",
    "GenericAll": "Restrict GenericAll ACE; apply least-privilege ACLs on this object.",
    "GenericWrite": "Restrict GenericWrite ACE; apply least-privilege ACLs on this object.",
    "WriteDacl": "Remove WriteDacl permission; this allows granting arbitrary further access.",
    "WriteOwner": "Remove WriteOwner permission; this allows an attacker to take ownership of the object.",
    "ForceChangePassword": "Restrict ForceChangePassword permission to authorized password-reset workflows only.",
    "AddMember": "Restrict AddMember permission; this allows adding arbitrary principals to privileged groups.",
    "Owns": "Review object ownership; unexpected ownership can grant implicit control.",
}
DEFAULT_RECOMMENDATION = "Review this relationship type and apply least-privilege remediation."


def get_paths_to_domain_admins(driver):
    query = """
    MATCH p=shortestPath((u:User)-[*1..%d]->(g:Group))
    WHERE toUpper(g.name) CONTAINS 'DOMAIN ADMINS'
      AND u.name <> g.name
    RETURN p
    LIMIT %d
    """ % (MAX_PATH_LENGTH, MAX_PATHS)

    paths = []
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            path = record["p"]
            nodes = [n.get("name", "UNKNOWN") for n in path.nodes]
            rels = [r.type for r in path.relationships]
            paths.append({"nodes": nodes, "rels": rels})
    return paths


def build_attack_path_string(path):
    parts = [path["nodes"][0]]
    for rel, node in zip(path["rels"], path["nodes"][1:]):
        parts.append(f"-> {rel} -> {node}")
    return " ".join(parts)


def build_recommendations(path):
    seen = []
    for rel in path["rels"]:
        rec = EDGE_RECOMMENDATIONS.get(rel, DEFAULT_RECOMMENDATION)
        if rec not in seen:
            seen.append(rec)
    return seen


def severity_for_path(path):
    risky_edges = {"GenericAll", "GenericWrite", "WriteDacl", "WriteOwner",
                   "ForceChangePassword", "AddMember", "Owns"}
    if any(r in risky_edges for r in path["rels"]):
        return "Critical"
    if len(path["rels"]) == 1 and path["rels"][0] == "MemberOf":
        return "Medium"
    return "High"


def main():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    client = TheHiveClient(api_key=THEHIVE_API_KEY)

    paths = get_paths_to_domain_admins(driver)
    driver.close()

    print(f"Found {len(paths)} path(s) to Domain Admins.\n")

    seen_signatures = set()
    created = 0

    for path in paths:
        signature = tuple(path["nodes"])
        if signature in seen_signatures:
            continue
        seen_signatures.add(signature)

        attack_path_str = build_attack_path_string(path)
        start_node = path["nodes"][0]
        end_node = path["nodes"][-1]

        ticket = {
            "title": f"Attack path to Domain Admins: {start_node}",
            "attack_path": attack_path_str,
            "recommended_actions": build_recommendations(path),
            "severity": severity_for_path(path),
            "cve_id": "N/A",
            "owner": "wado",
        }

        status, result = client.create_case(ticket)
        print(f"[{status}] {start_node} -> {end_node} | severity={ticket['severity']}")
        if status != 201:
            print(f"   -> {result}")
        else:
            created += 1

    print(f"\nDone. {created} case(s) created out of {len(seen_signatures)} unique path(s).")


if __name__ == "__main__":
    main()
