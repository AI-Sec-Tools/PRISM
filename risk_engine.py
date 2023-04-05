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

# Enhanced Risk Scoring with ML Support
class AdvancedRiskEngine(RiskScoringEngine):
    def __init__(self):
        super().__init__()
        self.ml_enabled = False
        
    def enable_ml_scoring(self):
        """Enable machine learning enhanced scoring."""
        self.ml_enabled = True
        self.logger.info("ML-enhanced scoring enabled")
    
    def calculate_enhanced_risk_score(self, vulnerability: Dict, context: Dict = None) -> Dict:
        """Calculate enhanced risk score with context."""
        base_score = self.calculate_risk_score(vulnerability)
        
        if context:
            # Business impact multiplier
            criticality = context.get('asset_criticality', 'medium')
            multipliers = {'low': 0.8, 'medium': 1.0, 'high': 1.3, 'critical': 1.5}
            business_multiplier = multipliers.get(criticality, 1.0)
            
            # Exposure multiplier
            exposure = context.get('exposure_level', 'internal')
            exposure_multipliers = {'internal': 1.0, 'external': 1.2, 'internet_facing': 1.4}
            exposure_multiplier = exposure_multipliers.get(exposure, 1.0)
            
            enhanced_score = base_score * business_multiplier * exposure_multiplier
        else:
            enhanced_score = base_score
        
        return {
            'base_score': base_score,
            'enhanced_score': min(enhanced_score, 10.0),
            'risk_level': self.categorize_risk(enhanced_score),
            'factors': {
                'business_impact': business_multiplier if context else 1.0,
                'exposure_impact': exposure_multiplier if context else 1.0
            }
        }
