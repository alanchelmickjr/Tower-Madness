#!/usr/bin/env python3
"""
Build script for web deployment using Pygbag
Converts the Tower Madness game to run in a web browser
"""

import os
import sys
import shutil
import subprocess

def prepare_web_build():
    """Prepare the game for web deployment."""
    
    print("🏢 Tower Madness Web Build Script 🏢")
    print("=" * 50)
    
    # Check if pygbag is installed
    try:
        import pygbag
        print("✅ Pygbag is installed")
    except ImportError:
        print("❌ Pygbag not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pygbag"])
        print("✅ Pygbag installed")
    
    # Create web build directory
    build_dir = "web_build"
    if os.path.exists(build_dir):
        print(f"🗑️  Cleaning existing {build_dir} directory...")
        shutil.rmtree(build_dir)
    
    os.makedirs(build_dir)
    print(f"📁 Created {build_dir} directory")
    
    # Copy game files
    print("📋 Copying game files...")
    
    # Files and directories to copy
    items_to_copy = [
        "main.py",
        "config.py",
        "game",
        "requirements.txt",
        ".env.example"
    ]
    
    for item in items_to_copy:
        if os.path.isdir(item):
            shutil.copytree(item, os.path.join(build_dir, item))
            print(f"  ✅ Copied directory: {item}")
        elif os.path.isfile(item):
            shutil.copy2(item, build_dir)
            print(f"  ✅ Copied file: {item}")
    
    # Create index.html for web
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tower Madness - Elevator Operator</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: Arial, sans-serif;
        }
        #game-container {
            text-align: center;
        }
        h1 {
            color: #0ff;
            text-shadow: 2px 2px 4px rgba(0,255,255,0.5);
        }
        .controls {
            color: #fff;
            margin: 20px;
            padding: 20px;
            background: rgba(0,0,0,0.8);
            border: 2px solid #0ff;
            border-radius: 10px;
        }
        .loading {
            color: #0ff;
            font-size: 24px;
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div id="game-container">
        <h1>🏢 Tower Madness: Elevator Operator 🏢</h1>
        <div class="loading">Loading game...</div>
        <canvas id="canvas"></canvas>
        <div class="controls">
            <h3>Controls:</h3>
            <p>W/↑: Go UP | S/↓: Go DOWN | E/SPACE: Open/Close Doors</p>
            <p>Goal: Deliver 20 passengers to their destinations!</p>
            <p>Watch out for floods and hackathons!</p>
        </div>
    </div>
    
    <script src="https://pygame-web.github.io/archives/0.8/pythons.js" type="module"></script>
    <script type="module">
        import { loadPyodide } from 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js';
        
        async function main() {
            let pyodide = await loadPyodide();
            await pyodide.loadPackage(['pygame', 'numpy']);
            pyodide.runPython(`
                import sys
                sys.path.append('.')
                import main
                main.main()
            `);
        }
        
        main();
    </script>
</body>
</html>"""
    
    with open(os.path.join(build_dir, "index.html"), "w") as f:
        f.write(index_html)
    print("  ✅ Created index.html")
    
    # Create a web-compatible main.py wrapper
    web_main = """# Web-compatible main.py for Tower Madness
import asyncio
import pygame
import sys

# Add game directory to path
sys.path.insert(0, '.')

# Import the original main
from main import main as original_main

async def web_main():
    \"\"\"Async wrapper for web deployment.\"\"\"
    # Initialize pygame
    pygame.init()
    
    # Run the game
    await original_main()

# For Pygbag
if __name__ == "__main__":
    asyncio.run(web_main())
"""
    
    # Rename original main.py
    shutil.move(
        os.path.join(build_dir, "main.py"),
        os.path.join(build_dir, "main_original.py")
    )
    
    # Write new web-compatible main.py
    with open(os.path.join(build_dir, "main.py"), "w") as f:
        f.write(web_main)
    print("  ✅ Created web-compatible main.py")
    
    print("\n" + "=" * 50)
    print("✅ Web build prepared successfully!")
    print("\n📦 To build for web, run:")
    print(f"  cd {build_dir}")
    print("  python -m pygbag .")
    print("\n🌐 Then open: http://localhost:8000")
    print("\n🚀 To deploy:")
    print("  1. The build will create a 'build' directory")
    print("  2. Upload the contents to any web server")
    print("  3. Or use GitHub Pages, Netlify, Vercel, etc.")
    
    return build_dir

def run_pygbag_server(build_dir):
    """Run the Pygbag development server."""
    print("\n🚀 Starting Pygbag server...")
    os.chdir(build_dir)
    subprocess.run([sys.executable, "-m", "pygbag", "."])

if __name__ == "__main__":
    build_dir = prepare_web_build()
    
    # Ask if user wants to run the server
    response = input("\n🎮 Start the web server now? (y/n): ")
    if response.lower() == 'y':
        run_pygbag_server(build_dir)