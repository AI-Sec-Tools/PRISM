"""
Advanced Scoring Models for PRISM
Multiple scoring algorithms for comprehensive risk assessment.
"""

from abc import ABC, abstractmethod
from typing import Dict

class ScoringModel(ABC):
    @abstractmethod
    def calculate_score(self, vulnerability: Dict) -> float:
        pass

class CVSSPlusModel(ScoringModel):
    def calculate_score(self, vulnerability: Dict) -> float:
        base_score = vulnerability.get('cvss_score', 0.0)
        # Enhanced CVSS with threat intelligence
        if vulnerability.get('has_exploit'):
            base_score *= 1.3
        if vulnerability.get('in_wild'):
            base_score *= 1.5
        return min(base_score, 10.0)

class BusinessImpactModel(ScoringModel):
    def calculate_score(self, vulnerability: Dict) -> float:
        # Business context scoring
        asset_criticality = vulnerability.get('asset_criticality', 'medium')
        multipliers = {'low': 0.5, 'medium': 1.0, 'high': 1.5, 'critical': 2.0}
        base_score = vulnerability.get('cvss_score', 5.0)
        return base_score * multipliers.get(asset_criticality, 1.0)
