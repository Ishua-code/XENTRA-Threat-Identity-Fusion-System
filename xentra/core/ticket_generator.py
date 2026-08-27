import csv
import json
from datetime import datetime
import yaml
from xentra.utils.logger import get_logger

logger = get_logger("TicketGenerator")


class TicketGenerator:
    def __init__(self, config_path="xentra/config/settings.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.critical_threshold = self.config["scoring"]["risk_threshold_critical"]
        self.high_threshold = self.config["scoring"]["risk_threshold_high"]

    def _load_attack_paths(self):
        try:
            with open("engine/attack-paths.json") as f:
                paths = json.load(f)
            return {p["account"]: p for p in paths}
        except FileNotFoundError:
            logger.warning("No attack-paths.json found, tickets will not include path evidence")
            return {}

    def _get_severity(self, score):
        if score >= self.critical_threshold:
            return "Critical"
        elif score >= self.high_threshold:
            return "High"
        else:
            return "Medium"

    def _recommend_action(self, finding, path_info):
        actions = []
        if path_info and path_info.get("hops", 99) <= 2:
            actions.append("Enforce MFA immediately on this account")
        if path_info and path_info.get("hops", 99) >= 3:
            actions.append("Review lateral movement path; rotate credentials for all accounts in the chain")
        actions.append("Patch " + finding["cve_id"] + " on host " + finding["host"])
        return actions

    def generate_tickets(self, unified_scores_path="engine/unified-risk-scores.csv"):
        with open(unified_scores_path) as f:
            findings = list(csv.DictReader(f))

        attack_paths = self._load_attack_paths()
        tickets = []

        for finding in findings:
            score = float(finding["unified_risk_score"])
            if score < self.high_threshold:
                continue

            owner = finding["owner"]
            path_info = attack_paths.get(owner)

            severity = self._get_severity(score)
            ticket_id = "XENTRA-" + datetime.now().strftime("%Y%m%d%H%M%S") + "-" + str(len(tickets) + 1)
            title = severity + " Risk: " + finding["cve_id"] + " on account '" + owner + "'"

            if path_info:
                attack_path_value = path_info["path"]
                hops_value = path_info["hops"]
            else:
                attack_path_value = "No confirmed path found"
                hops_value = "N/A"

            ticket = {
                "ticket_id": ticket_id,
                "title": title,
                "severity": severity,
                "cve_id": finding["cve_id"],
                "host": finding["host"],
                "owner": owner,
                "epss_score": finding["epss_score"],
                "identity_exposure_score": finding["identity_exposure_score"],
                "unified_risk_score": score,
                "attack_path": attack_path_value,
                "hops_to_domain_admin": hops_value,
                "recommended_actions": self._recommend_action(finding, path_info),
                "status": "Open",
                "created_at": datetime.now().isoformat()
            }
            tickets.append(ticket)
            logger.info("Generated " + ticket_id + " | " + severity + " | " + title)

        self._save_tickets(tickets)
        return tickets

    def _save_tickets(self, tickets):
        with open("engine/generated-tickets.json", "w") as f:
            json.dump(tickets, f, indent=2)
        logger.info("Saved " + str(len(tickets)) + " tickets to engine/generated-tickets.json")
