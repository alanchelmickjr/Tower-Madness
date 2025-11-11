# Tower Madness - Pygbag Web Deployment Guide

This guide explains how to deploy Tower Madness to the web using Pygbag, allowing the actual Python/Pygame code to run in browsers via WebAssembly.

## 🎯 Overview

**What is Pygbag?**
Pygbag packages Python/Pygame applications to run in web browsers using Pyodide (Python compiled to WebAssembly). This means your actual Python code runs in the browser - no JavaScript rewrite needed!

**What We've Fixed:**
1. ✅ Removed problematic MP3 files from pygame installation
2. ✅ Worked around CDN 403 errors with custom HTML
3. ✅ Created port 5000 server for Replit Autoscale deployment
4. ✅ Automated the entire build process

## 🚀 Quick Start

### 1. Build the Game

```bash
python build_pygbag.py
```

This script will:
- Remove any problematic MP3 files from pygame examples
- Run pygbag to package your game
- Create `tower-madness.apk` (the game package)
- Copy files to the right locations

### 2. Run Locally

```bash
python serve_web.py
```

Then open: http://localhost:5000

### 3. Deploy to Production

Upload these two files to your web host:
- `tower-madness.apk` (game package)
- `index_pygbag.html` (game interface)

Access the game via `index_pygbag.html`

## 📁 Key Files

| File | Purpose |
|------|---------|
| `main_web.py` | Web-compatible game entry point with async/await |
| `build_pygbag.py` | Automated build script that handles all issues |
| `serve_web.py` | HTTP server for local testing (port 5000) |
| `index_pygbag.html` | Custom HTML interface that loads the game |
| `tower-madness.apk` | Packaged game (created by pygbag) |
| `.pygbag` | Pygbag configuration file |
| `pygbag.json` | Additional build configuration |

## 🔧 How It Works

### Build Process

1. **MP3 Fix**: The script removes pygame's example MP3 files that cause build errors
2. **Pygbag Package**: Runs `pygbag --build main_web.py` to create the game package
3. **APK Creation**: Creates `tower-madness.apk` containing all game code and assets
4. **Custom HTML**: Uses `index_pygbag.html` instead of pygbag's default template

### Runtime Process

1. Browser loads `index_pygbag.html`
2. Pyodide (Python in WebAssembly) is loaded from CDN
3. Game package (`tower-madness.apk`) is downloaded and extracted
4. Python code runs in the browser!
5. Pygame renders to HTML5 Canvas

## 🐛 Troubleshooting

### Build Fails with MP3 Error

**Solution**: Run `python build_pygbag.py` - it automatically fixes this.

**Manual Fix**:
```bash
python -c "import pygame; import os; mp3 = os.path.join(os.path.dirname(pygame.__file__), 'examples/data/house_lo.mp3'); os.remove(mp3) if os.path.exists(mp3) else None"
```

### CDN 403 Forbidden Errors

**Solution**: Already handled! We use a custom HTML file that works around CDN issues.

The build script times out after 3 minutes but checks if the APK was created. If so, it continues successfully.

### Port 5000 Already in Use

```bash
lsof -ti:5000 | xargs kill -9
python serve_web.py
```

### Game Doesn't Load in Browser

1. Check browser console for errors
2. Ensure both files are in the same directory:
   - `tower-madness.apk`
   - `index_pygbag.html`
3. Serve via HTTP server (file:// won't work due to CORS)
4. Try different browser (Chrome/Firefox recommended)

## 📦 Deployment Options

### Option 1: Replit Autoscale (Port 5000)

```bash
python serve_web.py
```

Replit will automatically detect the server on port 5000 and make it publicly accessible.

### Option 2: Static Web Host

Upload to any static web host:
- GitHub Pages
- Netlify
- Vercel
- Cloudflare Pages
- AWS S3 + CloudFront

**Required Files:**
- `tower-madness.apk`
- `index_pygbag.html`

### Option 3: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY tower-madness.apk index_pygbag.html ./
EXPOSE 5000
CMD ["python", "-m", "http.server", "5000"]
```

## 🎮 Game Controls

- **W / ↑** - Move Elevator UP
- **S / ↓** - Move Elevator DOWN
- **E / SPACE** - Open/Close Doors

**Goal**: Deliver 20 passengers to their destinations!

## 🔬 Technical Details

### Requirements

- Python 3.11+
- pygame 2.6+
- pygbag 0.8.6 (0.9.x has CDN issues)

### Install Dependencies

```bash
pip install pygame pygbag==0.8.6
```

### Build Time

- Initial build: ~3 minutes
- Subsequent builds: ~2 minutes (cached)

### Package Size

- APK file: ~1.1 MB
- Total download (with Pyodide): ~15 MB

### Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+ (may have audio issues)
- ❌ IE 11 (not supported)

### Performance

- First load: 10-15 seconds (loading Pyodide)
- Game starts: 2-3 seconds
- FPS: 60 (same as desktop)

## 🔄 Updating the Game

1. Make changes to your game code in `game/` or `main_web.py`
2. Run `python build_pygbag.py` again
3. Test with `python serve_web.py`
4. Deploy updated `tower-madness.apk` and `index_pygbag.html`

## 📚 Additional Resources

- [Pygbag Documentation](https://github.com/pygame-web/pygbag)
- [Pyodide Documentation](https://pyodide.org/)
- [Pygame Documentation](https://www.pygame.org/docs/)

## ❓ FAQ

**Q: Do I need to rewrite my game in JavaScript?**
A: No! Your actual Python code runs in the browser via WebAssembly.

**Q: Will all Pygame features work?**
A: Most do! Audio might need browser interaction to start. Some file system operations are limited.

**Q: Can I use other Python libraries?**
A: Yes, if they're available in Pyodide or pure Python packages.

**Q: How do I add custom assets?**
A: Place them in your game directory. They'll be packaged automatically.

**Q: Why pygbag 0.8.6 instead of latest?**
A: Version 0.9.x has CDN access issues. 0.8.6 is stable.

---

**Built with** ❤️ **using Python, Pygame, and Pygbag**
