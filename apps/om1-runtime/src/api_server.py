#!/usr/bin/env python3
"""
Bitcoin Advisor Agent - HTTP API Server

Provides REST API endpoints for the Next.js frontend to interact with the agent.
"""

import sys
import json
import os
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agent.runtime import BitcoinAdvisorAgent


class AgentAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for agent API."""

    agent: BitcoinAdvisorAgent = None
    agent_lock = threading.Lock()
    last_signal = None
    agent_status = {
        'running': False,
        'cycle_count': 0,
        'last_updated': None
    }

    def _set_cors_headers(self):
        """Set CORS headers for Next.js frontend."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _send_json(self, data: dict, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _send_error(self, message: str, status: int = 500):
        """Send error response."""
        self._send_json({'error': message}, status)

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/health':
            self._send_json({
                'status': 'healthy',
                'agent_running': AgentAPIHandler.agent is not None
            })

        elif path == '/api/status':
            self._send_json(AgentAPIHandler.agent_status)

        elif path == '/api/signal':
            if AgentAPIHandler.last_signal:
                self._send_json(AgentAPIHandler.last_signal)
            else:
                self._send_error('No signal available yet. Try POST /api/analyze', 404)

        else:
            self._send_error('Not found', 404)

    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/analyze':
            self._handle_analyze()
        else:
            self._send_error('Not found', 404)

    def _handle_analyze(self):
        """Trigger a new analysis cycle."""
        try:
            if not AgentAPIHandler.agent:
                self._send_error('Agent not initialized', 503)
                return

            with AgentAPIHandler.agent_lock:
                # Run one cycle
                print("\n🔄 Running analysis cycle triggered by API request...")

                # Collect inputs
                print("📊 Collecting input data...")
                input_data = AgentAPIHandler.agent._collect_inputs()

                # Generate signal
                print("🎯 Generating trading signal...")
                signal = AgentAPIHandler.agent._generate_signal(input_data)

                # Create response
                response = {
                    'signal': signal['signal'],
                    'confidence': signal['confidence'],
                    'reasoning': signal['reasoning'],
                    'data': {
                        'btc_price': input_data.get('bitcoin_price', {}).get('price'),
                        'rsi': input_data.get('bitcoin_price', {}).get('rsi'),
                        'sentiment': input_data.get('news_sentiment', {}).get('sentiment_label')
                    },
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S')
                }

                # Update status
                AgentAPIHandler.agent_status['cycle_count'] += 1
                AgentAPIHandler.agent_status['last_updated'] = response['timestamp']
                AgentAPIHandler.last_signal = response

                print(f"✅ Signal generated: {signal['signal']} ({signal['confidence']}%)")

                self._send_json(response)

        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            import traceback
            traceback.print_exc()
            self._send_error(str(e))

    def log_message(self, format, *args):
        """Override to customize logging."""
        print(f"[{self.log_date_time_string()}] {format % args}")


def load_agent_config():
    """Load agent configuration."""
    from dotenv import load_dotenv

    # Load environment variables
    env_path = project_root.parent.parent / '.env'
    load_dotenv(env_path)

    config_path = project_root / 'config' / 'bitcoin_advisor.json'

    with open(config_path, 'r') as f:
        config = json.load(f)

    # Replace environment variable placeholders
    config_str = json.dumps(config)
    for key, value in os.environ.items():
        config_str = config_str.replace(f'${{{key}}}', value)

    return json.loads(config_str)


def main():
    """Start API server."""
    print("=" * 60)
    print("🚀 Bitcoin Advisor Agent - API Server")
    print("=" * 60)
    print()

    # Load configuration and initialize agent
    print("📋 Loading agent configuration...")
    config = load_agent_config()

    print("🤖 Initializing agent...")
    AgentAPIHandler.agent = BitcoinAdvisorAgent(config)
    AgentAPIHandler.agent_status['running'] = True

    print()
    print("=" * 60)
    print("✅ Agent initialized and ready")
    print("=" * 60)
    print()

    # Start HTTP server
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', '8000'))

    server = HTTPServer((host, port), AgentAPIHandler)

    print(f"🌐 API Server running at http://{host}:{port}")
    print()
    print("📡 Available endpoints:")
    print(f"   GET  http://{host}:{port}/health")
    print(f"   GET  http://{host}:{port}/api/status")
    print(f"   GET  http://{host}:{port}/api/signal")
    print(f"   POST http://{host}:{port}/api/analyze")
    print()
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down server...")
        server.shutdown()
        print("👋 Server stopped")


if __name__ == '__main__':
    main()
