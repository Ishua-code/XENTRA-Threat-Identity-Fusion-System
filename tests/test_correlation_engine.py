import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from xentra.core.identity_scorer import IdentityScorer

def test_domain_admin_no_mfa_is_high_risk():
    scorer = IdentityScorer()
    score = scorer.calculate_score("domain_admin", "false", 5)
    assert score >= 0.8, f"Expected high risk score, got {score}"

def test_standard_user_with_mfa_is_low_risk():
    scorer = IdentityScorer()
    score = scorer.calculate_score("standard", "true", 5)
    assert score <= 0.2, f"Expected low risk score, got {score}"

def test_stale_account_increases_score():
    scorer = IdentityScorer()
    fresh_score = scorer.calculate_score("standard", "true", 5)
    stale_score = scorer.calculate_score("standard", "true", 90)
    assert stale_score > fresh_score, "Stale account should have higher score"

if __name__ == "__main__":
    test_domain_admin_no_mfa_is_high_risk()
    test_standard_user_with_mfa_is_low_risk()
    test_stale_account_increases_score()
    print("All tests passed!")
