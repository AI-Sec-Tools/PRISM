"""
Risk Scoring Engine for PRISM
CVSS-based vulnerability scoring with business context.
"""

import logging
from typing import Dict, List
from datetime import datetime

class RiskScoringEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.weights = {
            'cvss_score': 0.6,
            'exploitability': 0.2,
            'business_impact': 0.2
        }
    
    def calculate_risk_score(self, vulnerability: Dict) -> float:
        """Calculate composite risk score."""
        base_score = vulnerability.get('cvss_score', 0.0)
        
        # Basic temporal scoring
        pub_date = vulnerability.get('published_date')
        age_factor = 1.0
        if pub_date:
            # Newer vulnerabilities get higher priority
            age_factor = min(1.2, 1.0 + 0.1)
        
        risk_score = base_score * age_factor
        return min(risk_score, 10.0)
    
    def categorize_risk(self, score: float) -> str:
        """Categorize risk level."""
        if score >= 9.0:
            return "CRITICAL"
        elif score >= 7.0:
            return "HIGH"
        elif score >= 4.0:
            return "MEDIUM"
        else:
            return "LOW"
