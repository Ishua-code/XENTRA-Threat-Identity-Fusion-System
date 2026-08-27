import csv
from xentra.core.graph_risk_analyzer import GraphRiskAnalyzer
from xentra.utils.logger import get_logger

logger = get_logger("GraphAnalysisRunner")

with open("lab-setup/identity-data.csv") as f:
    identities = list(csv.DictReader(f))

analyzer = GraphRiskAnalyzer()
results = analyzer.analyze_all(identities)
analyzer.save_results(results)

logger.info("Graph-based risk analysis complete.")
