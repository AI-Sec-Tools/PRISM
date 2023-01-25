"""
Threat Intelligence Manager for PRISM
Integrates with various threat intelligence feeds.
"""

import requests
import logging
from typing import Dict, List
from datetime import datetime

class ThreatIntelligenceManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.feeds = {
            'cisa_kev': 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json',
            'epss': 'https://api.first.org/data/v1/epss'
        }
    
    def update_feeds(self) -> Dict:
        """Update threat intelligence feeds."""
        results = {}
        for feed_name, feed_url in self.feeds.items():
            try:
                result = self._update_feed(feed_name, feed_url)
                results[feed_name] = result
            except Exception as e:
                self.logger.error(f"Failed to update {feed_name}: {e}")
                results[feed_name] = {'error': str(e)}
        return results
    
    def _update_feed(self, name: str, url: str) -> Dict:
        """Update a specific feed."""
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if name == 'cisa_kev':
            return self._process_kev_data(data)
        elif name == 'epss':
            return self._process_epss_data(data)
    
    def _process_kev_data(self, data: Dict) -> Dict:
        """Process CISA KEV data."""
        vulnerabilities = data.get('vulnerabilities', [])
        processed = []
        for vuln in vulnerabilities:
            processed.append({
                'cve_id': vuln.get('cveID'),
                'in_kev': True,
                'known_exploited': True
            })
        return {'processed': len(processed), 'vulnerabilities': processed}
    
    def _process_epss_data(self, data: Dict) -> Dict:
        """Process EPSS data."""
        return {'status': 'updated', 'timestamp': datetime.now().isoformat()}
    
    def get_vulnerability_intelligence(self, cve_id: str) -> Dict:
        """Get threat intelligence for a specific CVE."""
        # This would query stored intelligence data
        return {
            'cve_id': cve_id,
            'epss_score': 0.1,  # Default
            'in_kev': False,
            'known_exploited': False
        }
