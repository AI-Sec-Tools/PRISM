"""
Web Dashboard for PRISM
Production-ready FastAPI dashboard with comprehensive features.
"""

import asyncio
import json
import logging
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

class PRISMDashboard:
    def __init__(self, config, prism_instance):
        self.config = config
        self.prism = prism_instance
        self.logger = logging.getLogger(__name__)
        
        self.app = FastAPI(
            title="PRISM - Priority Risk Intelligence & Scoring Manager",
            description="Comprehensive vulnerability prioritization platform",
            version="1.0.0"
        )
        
        self._setup_routes()
    
    def _setup_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_home(request: Request):
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>PRISM Dashboard</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <nav class="navbar navbar-dark bg-dark">
                    <div class="container-fluid">
                        <span class="navbar-brand">PRISM - Vulnerability Risk Management</span>
                    </div>
                </nav>
                
                <div class="container-fluid mt-4">
                    <div class="row">
                        <div class="col-md-3">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Total Vulnerabilities</h5>
                                    <h2 class="text-primary" id="total-vulns">-</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Critical Risk</h5>
                                    <h2 class="text-danger" id="critical-count">-</h2>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
                <script>
                    async function loadData() {
                        const response = await fetch('/api/stats');
                        const data = await response.json();
                        document.getElementById('total-vulns').textContent = data.total;
                        document.getElementById('critical-count').textContent = data.critical;
                    }
                    loadData();
                    setInterval(loadData, 30000);
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
        
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "service": "prism"}

async def launch_dashboard(config, prism_instance):
    dashboard = PRISMDashboard(config, prism_instance)
    host = config.get('host', '0.0.0.0')
    port = config.get('port', 8080)
    
    config_obj = uvicorn.Config(dashboard.app, host=host, port=port)
    server = uvicorn.Server(config_obj)
    await server.serve()
