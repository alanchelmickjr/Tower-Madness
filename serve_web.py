#!/usr/bin/env python3
"""
Simple HTTP server for Tower Madness web deployment
Serves the Pygbag build on port 5000 for Replit Autoscale
"""

import http.server
import socketserver
import os
from pathlib import Path

# Determine which directory to serve
web_dir = Path(__file__).parent

# Check if we have the necessary files
if not (web_dir / "tower-madness.apk").exists():
    print("❌ Error: tower-madness.apk not found!")
    print("   Run: python build_pygbag.py first to build the game")
    exit(1)

if not (web_dir / "index_pygbag.html").exists():
    print("❌ Error: index_pygbag.html not found!")
    exit(1)

# Change to the directory
os.chdir(web_dir)

PORT = 5000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve index_pygbag.html as the default page."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(web_dir), **kwargs)

    def end_headers(self):
        # Add CORS headers for Pyodide
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        # Serve index_pygbag.html when accessing root
        if self.path == '/':
            self.path = '/index_pygbag.html'
        return super().do_GET()

print("=" * 60)
print("🏢 Tower Madness - Web Server (Pygbag)")
print("=" * 60)
print(f"📂 Serving from: {web_dir}")
print(f"🌐 Server running at: http://0.0.0.0:{PORT}")
print(f"🌐 Local access: http://localhost:{PORT}")
print("=" * 60)
print("📦 Files being served:")
print(f"   - index_pygbag.html (main page)")
print(f"   - tower-madness.apk (game package)")
print("=" * 60)
print("Press Ctrl+C to stop the server")
print()

try:
    with socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n👋 Server stopped")
except OSError as e:
    if e.errno == 98:
        print(f"\n❌ Error: Port {PORT} is already in use!")
        print("   Try: lsof -ti:{PORT} | xargs kill -9")
    else:
        print(f"\n❌ Server error: {e}")
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
