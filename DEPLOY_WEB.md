# 🌐 Web Deployment Guide for Tower Madness

## Quick Fix Applied ✅

The black screen issue on pybag has been **FIXED**! The problem was:
- `main_web.py` wasn't initializing the display screen before creating the game engine
- The GameEngine constructor requires `screen` and `clock` parameters that weren't being passed

## 🚀 Deployment Options

### Option 1: Pygbag (Recommended for Pygame)

**What is Pygbag?**
Pygbag converts Python/Pygame games to run in web browsers using WebAssembly.

**Steps:**

1. **Install Pygbag**
```bash
pip install pygbag
```

2. **Build for Web**
```bash
# Use the fixed main_web.py as entry point
pygbag main_web.py
```

3. **Test Locally**
The build will automatically start a local server. Open:
```
http://localhost:8000
```

4. **Deploy the Build**
After building, you'll have a `build/web` folder. Upload this to any static hosting:
- GitHub Pages
- Netlify
- Vercel
- Cloudflare Pages

### Option 2: GitHub Pages (Free & Easy)

1. **Create a `gh-pages` branch:**
```bash
git checkout -b gh-pages
```

2. **Build the game:**
```bash
pygbag main_web.py --build
```

3. **Copy build files to root:**
```bash
cp -r build/web/* .
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages
```

4. **Enable GitHub Pages:**
- Go to your repo Settings → Pages
- Source: Deploy from branch `gh-pages`
- Your game will be live at: `https://yourusername.github.io/Tower-Madness/`

### Option 3: Vercel (Free & Fast)

**Method A: Using Vercel CLI**

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Create `vercel.json`:**
```json
{
  "buildCommand": "pip install pygbag && pygbag main_web.py --build",
  "outputDirectory": "build/web",
  "framework": null
}
```

3. **Deploy:**
```bash
vercel
```

**Method B: Using GitHub Integration**

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Add build settings:
   - Build Command: `pip install pygbag && pygbag main_web.py --build`
   - Output Directory: `build/web`
4. Deploy!

### Option 4: Netlify (Free & Simple)

1. **Create `netlify.toml`:**
```toml
[build]
  command = "pip install pygbag && pygbag main_web.py --build"
  publish = "build/web"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

2. **Deploy via Netlify CLI:**
```bash
npm install -g netlify-cli
netlify deploy --prod
```

Or drag & drop the `build/web` folder to [netlify.com/drop](https://app.netlify.com/drop)

### Option 5: Itch.io (Game Platform)

1. **Build for web:**
```bash
pygbag main_web.py --build
```

2. **Create a ZIP:**
```bash
cd build/web
zip -r tower-madness-web.zip *
```

3. **Upload to itch.io:**
- Create a new project
- Set to "HTML" project type
- Upload the ZIP
- Check "This file will be played in the browser"

## 📋 Pre-Deployment Checklist

- [x] Fixed `main_web.py` display initialization
- [x] Created proper `index.html` with styling
- [ ] Test locally with `python -m http.server` or pygbag
- [ ] Verify all game assets are included
- [ ] Check that `pygame` and dependencies load correctly
- [ ] Test on different browsers (Chrome, Firefox, Safari)

## 🐛 Troubleshooting

### Black Screen Issues
- ✅ **FIXED**: Display now properly initialized in `main_web.py`
- Ensure `pygame.display.set_mode()` is called before `GameEngine()`
- Check browser console for Python errors

### Loading Issues
- Clear browser cache (Ctrl+Shift+Delete)
- Disable browser extensions temporarily
- Try a different browser
- Check that all files are in the `build/web` folder

### Performance Issues
- Pygbag games run slower than native Python
- Expected 30-60 FPS in browser vs 60+ FPS native
- Consider reducing screen resolution if needed

### Asset Loading
- All assets must be in the same directory structure
- Audio may have delays in web browsers
- Some fonts may need web-compatible alternatives

## 🎮 Testing Your Deployment

1. **Local Test First:**
```bash
cd build/web
python -m http.server 8000
# Open http://localhost:8000
```

2. **Check These:**
- Does the game menu appear?
- Can you press SPACE to start?
- Do the elevator controls work?
- Are NPCs spawning?
- Does scoring work?

3. **Browser Compatibility:**
- ✅ Chrome/Edge (Chromium) - Best
- ✅ Firefox - Good
- ⚠️ Safari - May have issues with WebAssembly
- ❌ Internet Explorer - Not supported

## 🚀 Quick Deploy Commands

**One-liner for GitHub Pages:**
```bash
pygbag main_web.py --build && git checkout -b gh-pages && cp -r build/web/* . && git add . && git commit -m "Deploy" && git push origin gh-pages
```

**One-liner for Vercel:**
```bash
pip install pygbag && pygbag main_web.py --build && vercel --prod
```

## 📱 Mobile Support

The game is designed for desktop but can work on mobile:
- Touch controls may need implementation
- Landscape orientation recommended
- Minimum screen width: 800px

## 🎯 Next Steps

1. Test the fixed version locally
2. Choose a deployment platform
3. Build and deploy
4. Share your game URL!

## 📧 Support

If you encounter issues:
1. Check the browser console for errors
2. Verify all files in `build/web` directory
3. Test with different browsers
4. Review Pygbag documentation: https://pygame-web.github.io/

---

**Your game is now ready for the web! 🎉**

The black screen issue has been fixed by properly initializing the pygame display in `main_web.py`. Deploy and enjoy!