import csv
import json
import networkx as nx
import yaml
from xentra.utils.logger import get_logger

logger = get_logger("GraphRiskAnalyzer")

class GraphRiskAnalyzer:
    def __init__(self, config_path="xentra/config/settings.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.graph = nx.DiGraph()

    def build_graph_from_identities(self, identities):
        self.graph.add_node("DOMAIN_ADMIN")

        host_to_privileged = {}
        for identity in identities:
            if identity["privilege_level"] in ("domain_admin", "service_account"):
                host_to_privileged.setdefault(identity["owned_asset_ip"], []).append(identity["username"])

        for identity in identities:
            username = identity["username"]
            privilege = identity["privilege_level"]
            host = identity["owned_asset_ip"]

            if privilege in ("domain_admin", "service_account"):
                self.graph.add_edge(username, host)
                self.graph.add_edge(host, "DOMAIN_ADMIN")

        for identity in identities:
            username = identity["username"]
            privilege = identity["privilege_level"]
            host = identity["owned_asset_ip"]
            mfa = str(identity["mfa_enabled"]).lower()

            if privilege == "standard" and mfa == "false" and host in host_to_privileged:
                for privileged_user in host_to_privileged[host]:
                    self.graph.add_edge(username, privileged_user)

        logger.info(f"Graph built with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")

    def get_shortest_path_score(self, username):
        try:
            path = nx.shortest_path(self.graph, source=username, target="DOMAIN_ADMIN")
            path_length = len(path) - 1
            score = round(1 / path_length, 3)
            return score, path_length, path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return 0.0, None, None

    def get_betweenness_centrality(self):
        return nx.betweenness_centrality(self.graph)

    def analyze_all(self, identities):
        self.build_graph_from_identities(identities)
        centrality_scores = self.get_betweenness_centrality()

        results = []
        attack_paths = []

        for identity in identities:
            username = identity["username"]
            proximity_score, hops, path = self.get_shortest_path_score(username)
            centrality_score = round(centrality_scores.get(username, 0.0), 3)

            results.append({
                "username": username,
                "hops_to_domain_admin": hops if hops is not None else "unreachable",
                "graph_proximity_score": proximity_score,
                "betweenness_centrality": centrality_score
            })

            if path is not None:
                attack_paths.append({
                    "account": username,
                    "path": path,
                    "hops": hops
                })
                logger.info(f"{username}: ATTACK PATH = {' -> '.join(path)} ({hops} hops)")
            else:
                logger.info(f"{username}: No attack path to Domain Admin (isolated/secure)")

        self._save_attack_paths(attack_paths)
        return results

    def _save_attack_paths(self, attack_paths):
        attack_paths.sort(key=lambda x: x["hops"])
        with open("engine/attack-paths.json", "w") as f:
            json.dump(attack_paths, f, indent=2)
        logger.info(f"Saved {len(attack_paths)} attack paths to engine/attack-paths.json")

    def save_results(self, results, output_path="engine/graph-risk-analysis.csv"):
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        logger.info(f"Graph risk analysis saved to {output_path}")
