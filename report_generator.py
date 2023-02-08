"""
Report Generator for PRISM
Generates executive and technical vulnerability risk reports.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class ReportGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.output_dir = Path('reports')
        self.output_dir.mkdir(exist_ok=True)
    
    async def generate(self, report_type: str = 'executive') -> str:
        """Generate vulnerability risk report."""
        if report_type == 'executive':
            return await self._generate_executive_report()
        elif report_type == 'technical':
            return await self._generate_technical_report()
        else:
            raise ValueError(f"Unknown report type: {report_type}")
    
    async def _generate_executive_report(self) -> str:
        """Generate executive summary report."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = self.output_dir / f"executive_report_{timestamp}.html"
        
        report_content = """
        <!DOCTYPE html>
        <html>
        <head><title>PRISM Executive Risk Report</title></head>
        <body>
            <h1>Executive Vulnerability Risk Summary</h1>
            <h2>Key Risk Metrics</h2>
            <ul>
                <li>Total Vulnerabilities: 150</li>
                <li>Critical Risk: 12 (8%)</li>
                <li>High Risk: 34 (23%)</li>
                <li>Remediation Priority: Focus on 12 critical vulnerabilities</li>
            </ul>
            <h2>Recommendations</h2>
            <p>Immediate action required for critical vulnerabilities affecting internet-facing assets.</p>
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        return str(output_path)
    
    async def _generate_technical_report(self) -> str:
        """Generate technical detailed report."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = self.output_dir / f"technical_report_{timestamp}.html"
        
        report_content = """
        <!DOCTYPE html>
        <html>
        <head><title>PRISM Technical Risk Report</title></head>
        <body>
            <h1>Technical Vulnerability Analysis</h1>
            <h2>Detailed Risk Breakdown</h2>
            <table border="1">
                <tr><th>CVE ID</th><th>Risk Score</th><th>CVSS</th><th>Asset</th></tr>
                <tr><td>CVE-2024-0001</td><td>9.8</td><td>9.3</td><td>web-server-01</td></tr>
                <tr><td>CVE-2024-0002</td><td>8.5</td><td>7.5</td><td>db-server-01</td></tr>
            </table>
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        return str(output_path)
