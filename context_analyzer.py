"""
Business Context Analyzer for PRISM
Analyzes business context for accurate vulnerability risk scoring.
"""

import logging
from typing import Dict, List
from enum import Enum

class ExposureLevel(Enum):
    INTERNAL = "internal"
    EXTERNAL = "external" 
    INTERNET_FACING = "internet_facing"
    PUBLICLY_ACCESSIBLE = "publicly_accessible"

class BusinessCriticality(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BusinessContextAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_asset_context(self, asset: Dict) -> Dict:
        """Analyze business context for an asset."""
        context = {
            'asset_id': asset.get('id'),
            'criticality': self._assess_criticality(asset),
            'exposure_level': self._determine_exposure(asset),
            'business_functions': asset.get('business_functions', [])
        }
        return context
    
    def _assess_criticality(self, asset: Dict) -> str:
        """Assess business criticality."""
        asset_type = asset.get('type', '').lower()
        if 'payment' in asset_type or 'financial' in asset_type:
            return BusinessCriticality.CRITICAL.value
        elif 'database' in asset_type or 'auth' in asset_type:
            return BusinessCriticality.HIGH.value
        elif 'web' in asset_type:
            return BusinessCriticality.MEDIUM.value
        else:
            return BusinessCriticality.LOW.value
    
    def _determine_exposure(self, asset: Dict) -> str:
        """Determine exposure level."""
        ip_addresses = asset.get('ip_addresses', [])
        for ip in ip_addresses:
            if not ip.startswith(('10.', '172.', '192.168.')):
                return ExposureLevel.INTERNET_FACING.value
        return ExposureLevel.INTERNAL.value
