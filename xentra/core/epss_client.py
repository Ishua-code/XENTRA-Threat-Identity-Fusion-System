import csv
import time
import requests
import yaml
from xentra.utils.logger import get_logger

logger = get_logger("EPSSClient")

class EPSSClient:
    def __init__(self, config_path="xentra/config/settings.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.base_url = self.config["api"]["epss_base_url"]
        self.timeout = self.config["api"]["request_timeout"]
        self.delay = self.config["api"]["rate_limit_delay"]

    def get_score(self, cve_id):
        try:
            response = requests.get(
                self.base_url, params={"cve": cve_id}, timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            if data.get("data"):
                return float(data["data"][0]["epss"])
            logger.warning(f"No EPSS data found for {cve_id}, defaulting to 0.0")
            return 0.0
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {cve_id}: {e}")
            return 0.0
        except (KeyError, ValueError, IndexError) as e:
            logger.error(f"Unexpected response format for {cve_id}: {e}")
            return 0.0

    def enrich_dataset(self):
        input_path = self.config["paths"]["cve_dataset"]
        output_path = self.config["paths"]["enriched_vulnerabilities"]

        logger.info(f"Loading CVE dataset from {input_path}")
        with open(input_path) as f:
            rows = list(csv.DictReader(f))

        logger.info(f"Fetching EPSS scores for {len(rows)} CVEs...")
        for i, row in enumerate(rows, 1):
            row["epss_score"] = self.get_score(row["cve_id"])
            logger.info(f"[{i}/{len(rows)}] {row['cve_id']}: EPSS = {row['epss_score']}")
            time.sleep(self.delay)

        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        logger.info(f"Enriched dataset saved to {output_path}")
        return rows
