import csv
from xentra.core.epss_client import EPSSClient
from xentra.core.identity_scorer import IdentityScorer
from xentra.core.bloodhound_pathfinder import BloodHoundPathfinder
from xentra.core.correlation_engine import CorrelationEngine
from xentra.utils.logger import get_logger

logger = get_logger("Main")

def run_pipeline():
    logger.info("=" * 50)
    logger.info("XENTRA Pipeline Starting")
    logger.info("=" * 50)

    logger.info("STAGE 1: Vulnerability Detection + EPSS Enrichment")
    epss_client = EPSSClient()
    epss_client.enrich_dataset()

    logger.info("STAGE 2: Identity Exposure Scoring (Rule-Based)")
    identity_scorer = IdentityScorer()
    identity_scorer.score_all_identities()

    logger.info("STAGE 2.5: BloodHound Attack Path Analysis + TheHive Case Creation")
    pathfinder = BloodHoundPathfinder()
    pathfinder.run()

    logger.info("STAGE 3: Correlation Engine (Graph-Enhanced)")
    engine = CorrelationEngine()
    results = engine.run()

    logger.info("=" * 50)
    logger.info("Top 5 Unified Risk Findings:")
    for r in results[:5]:
        logger.info(f"  {r['cve_id']} | {r['owner']} | Score: {r['unified_risk_score']}")
    logger.info("=" * 50)
    logger.info("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()
