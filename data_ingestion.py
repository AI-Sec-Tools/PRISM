"""
Data Ingestion Module for PRISM
Support for JSON, CSV, and API data sources.
"""

import json
import csv
import requests
import logging
from typing import Dict, List
from pathlib import Path

class VulnerabilityDataIngester:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = ['json', 'csv', 'api']
    
    def ingest_json(self, file_path: str) -> List[Dict]:
        """Ingest vulnerabilities from JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return data
        elif 'vulnerabilities' in data:
            return data['vulnerabilities']
        else:
            return [data]
    
    def ingest_csv(self, file_path: str) -> List[Dict]:
        """Ingest vulnerabilities from CSV file."""
        vulnerabilities = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                vulnerabilities.append(dict(row))
        return vulnerabilities
    
    def ingest_api(self, api_url: str) -> List[Dict]:
        """Ingest vulnerabilities from API endpoint."""
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list):
            return data
        elif 'vulnerabilities' in data:
            return data['vulnerabilities']
        else:
            return [data]
    
    def process_vulnerabilities(self, vulns: List[Dict]) -> List[Dict]:
        """Process and normalize vulnerability data."""
        processed = []
        for vuln in vulns:
            # Normalize field names
            normalized = {
                'id': vuln.get('id') or vuln.get('cve_id') or vuln.get('vulnerability_id'),
                'title': vuln.get('title') or vuln.get('summary') or vuln.get('description', '')[:100],
                'severity': vuln.get('severity', 'medium').lower(),
                'cvss_score': float(vuln.get('cvss_score', 0)),
                'published_date': vuln.get('published_date') or vuln.get('date')
            }
            if normalized['id']:
                processed.append(normalized)
        
        self.logger.info(f"Processed {len(processed)} vulnerabilities")
        return processed
