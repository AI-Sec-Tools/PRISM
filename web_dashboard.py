"""
Web Dashboard for PRISM
Interactive FastAPI-based dashboard for vulnerability risk management.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import logging
from typing import Dict, List

class PRISMDashboard:
    def __init__(self):
        self.app = FastAPI(title="PRISM Dashboard", version="1.0.0")
        self.logger = logging.getLogger(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_home():
            return """
            <html>
            <head><title>PRISM Dashboard</title></head>
            <body>
                <h1>PRISM - Vulnerability Risk Dashboard</h1>
                <div id="stats">
                    <h2>Risk Statistics</h2>
                    <p>Total Vulnerabilities: <span id="total">Loading...</span></p>
                    <p>Critical Risk: <span id="critical">Loading...</span></p>
                </div>
                <script>
                    fetch('/api/stats').then(r => r.json()).then(data => {
                        document.getElementById('total').textContent = data.total;
                        document.getElementById('critical').textContent = data.critical;
                    });
                </script>
            </body>
            </html>
            """
        
        @self.app.get("/api/stats")
        async def get_stats():
            return {
                'total': 150,
                'critical': 12,
                'high': 34,
                'medium': 78,
                'low': 26
            }
        
        @self.app.get("/api/top-risks")
        async def get_top_risks():
            return [
                {'id': 'CVE-2024-0001', 'score': 9.8, 'severity': 'critical'},
                {'id': 'CVE-2024-0002', 'score': 8.5, 'severity': 'high'},
                {'id': 'CVE-2024-0003', 'score': 7.9, 'severity': 'high'}
            ]

async def launch_dashboard(config: Dict):
    """Launch the PRISM web dashboard."""
    dashboard = PRISMDashboard()
    import uvicorn
    uvicorn.run(dashboard.app, host='0.0.0.0', port=8080)
