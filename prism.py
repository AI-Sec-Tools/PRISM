#!/usr/bin/env python3
"""
PRISM - Priority Risk Intelligence & Scoring Manager
A comprehensive vulnerability prioritization platform with context-aware risk scoring.

Author: Manan Wason, Dewank Pant
License: MIT
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional
import yaml

from risk_engine import RiskScoringEngine
from context_analyzer import BusinessContextAnalyzer
from intelligence_feeds import ThreatIntelligenceManager
from data_ingestion import VulnerabilityDataIngester
from web_dashboard import launch_dashboard
from report_generator import ReportGenerator
from database import DatabaseManager

class PRISM:
    """Main PRISM application class for vulnerability prioritization."""
    
    def __init__(self, config_path: str = "config/prism.yaml"):
        """Initialize PRISM with configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.logger = self._setup_logging()
        
        # Initialize core components
        self.db_manager = DatabaseManager()
        self.risk_engine = RiskScoringEngine()
        self.context_analyzer = BusinessContextAnalyzer()
        self.intel_manager = ThreatIntelligenceManager()
        self.data_ingester = VulnerabilityDataIngester()
        self.report_generator = ReportGenerator()
        
        self.logger.info("PRISM initialized successfully")
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            return self._create_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """Create default configuration."""
        default_config = {
            'database': {'path': 'data/prism.db'},
            'logging': {'level': 'INFO', 'file': 'logs/prism.log'},
            'web_dashboard': {'host': '0.0.0.0', 'port': 8080}
        }
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False, indent=2)
        
        return default_config
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        log_file = log_config.get('file', 'logs/prism.log')
        
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        return logging.getLogger('PRISM')
    
    async def ingest_vulnerabilities(self, source_path: str, source_type: str = 'auto') -> Dict:
        """Ingest vulnerabilities from various sources."""
        self.logger.info(f"Ingesting vulnerabilities from {source_path}")
        
        try:
            if source_type == 'json' or source_path.endswith('.json'):
                vulns = self.data_ingester.ingest_json(source_path)
            elif source_type == 'csv' or source_path.endswith('.csv'):
                vulns = self.data_ingester.ingest_csv(source_path)
            elif source_type == 'api':
                vulns = self.data_ingester.ingest_api(source_path)
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
            
            processed = self.data_ingester.process_vulnerabilities(vulns)
            
            # Store in database
            for vuln in processed:
                self.db_manager.store_vulnerability(vuln)
            
            self.logger.info(f"Successfully ingested {len(processed)} vulnerabilities")
            return {'count': len(processed), 'format': source_type}
            
        except Exception as e:
            self.logger.error(f"Failed to ingest vulnerabilities: {e}")
            raise
    
    async def analyze_and_score(self) -> Dict:
        """Analyze context and compute risk scores for vulnerabilities."""
        self.logger.info("Starting vulnerability analysis and scoring")
        
        # This would integrate all components for comprehensive scoring
        return {'analysis_complete': True, 'scored_vulnerabilities': 0}
    
    async def generate_report(self, report_type: str = 'executive') -> str:
        """Generate vulnerability risk reports."""
        return await self.report_generator.generate(report_type)
    
    async def launch_web_dashboard(self):
        """Launch the interactive web dashboard."""
        dashboard_config = self.config.get('web_dashboard', {})
        await launch_dashboard(dashboard_config)

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="PRISM - Priority Risk Intelligence & Scoring Manager"
    )
    
    parser.add_argument('--config', '-c', default='config/prism.yaml',
                       help='Configuration file path')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Ingestion command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest vulnerability data')
    ingest_parser.add_argument('--source', '-s', required=True, help='Source file or URL')
    ingest_parser.add_argument('--type', '-t', choices=['json', 'csv', 'api', 'auto'],
                              default='auto', help='Source data type')
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Launch web dashboard')
    dashboard_parser.add_argument('--host', default='0.0.0.0', help='Dashboard host')
    dashboard_parser.add_argument('--port', type=int, default=8080, help='Dashboard port')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate reports')
    report_parser.add_argument('--type', '-t', choices=['executive', 'technical'],
                              default='executive', help='Report type')
    
    return parser

async def main():
    """Main entry point for PRISM."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        prism = PRISM(config_path=args.config)
        
        if args.command == 'ingest':
            result = await prism.ingest_vulnerabilities(args.source, args.type)
            print(f"Ingested {result['count']} vulnerabilities successfully")
        
        elif args.command == 'dashboard':
            prism.config['web_dashboard'].update({
                'host': args.host,
                'port': args.port
            })
            await prism.launch_web_dashboard()
        
        elif args.command == 'report':
            report_path = await prism.generate_report(args.type)
            print(f"Report generated: {report_path}")
    
    except Exception as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
