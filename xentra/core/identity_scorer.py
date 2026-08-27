import csv
import yaml
from xentra.utils.logger import get_logger

logger = get_logger("IdentityScorer")

class IdentityScorer:
    def __init__(self, config_path="xentra/config/settings.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.weights = self.config["identity_scoring"]

    def calculate_score(self, privilege, mfa_enabled, last_login_days):
        score = 0.0
        if privilege == "domain_admin":
            score += self.weights["domain_admin_weight"]
        elif privilege == "service_account":
            score += self.weights["service_account_weight"]
        else:
            score += self.weights["standard_weight"]

        if str(mfa_enabled).lower() == "false":
            score += self.weights["no_mfa_penalty"]

        if int(last_login_days) > self.weights["stale_account_days"]:
            score += self.weights["stale_account_penalty"]

        return round(min(score, 1.0), 3)

    def score_all_identities(self):
        input_path = self.config["paths"]["identity_dataset"]
        output_path = self.config["paths"]["scored_identities"]

        logger.info(f"Loading identity dataset from {input_path}")
        with open(input_path) as f:
            rows = list(csv.DictReader(f))

        for row in rows:
            row["identity_exposure_score"] = self.calculate_score(
                row["privilege_level"], row["mfa_enabled"], row["last_login_days_ago"]
            )
            logger.info(f"{row['username']}: Exposure = {row['identity_exposure_score']}")

        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        logger.info(f"Scored identities saved to {output_path}")
        return rows
