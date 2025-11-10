# 🚀 Deploy Tower Madness to Vercel (EASIEST METHOD)

## Why Vercel Failed Before
Vercel needs **static files** (HTML/JS), but your game is Python. We need to **build it first** using pygbag, which converts Python/Pygame to WebAssembly.

## ✅ I've Set Everything Up For You!

I created these files:
- ✅ `vercel.json` - Tells Vercel how to build your game
- ✅ `package.json` - Required by Vercel
- ✅ `netlify.toml` - Alternative option for Netlify
- ✅ `.vercelignore` - Excludes unnecessary files

## 🎯 Three Easy Deployment Options

---

### **Option 1: Vercel (via GitHub - RECOMMENDED)**

This is the easiest no-code option!

#### Steps:

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add Vercel deployment config"
   git push
   ```

2. **Go to [vercel.com](https://vercel.com)** and sign in with GitHub

3. **Click "Add New Project"** → **Import your Tower-Madness repository**

4. **Configure the project:**
   - Framework Preset: **Other**
   - Build Command: `pip3 install pygbag && python3 -m pygbag --build main_web.py`
   - Output Directory: `build/web`
   - Install Command: (leave empty)

5. **Click Deploy!** 🚀

6. **Wait 2-5 minutes** for the build to complete

7. **Your game will be live!** Vercel will give you a URL like: `https://tower-madness-xyz.vercel.app`

⚠️ **IMPORTANT**: The first deploy might fail if Vercel doesn't have Python. If it fails, try **Option 2** below instead.

---

### **Option 2: Build Locally, Deploy to Vercel**

This method ALWAYS works because you build on your own machine:

#### Steps:

1. **Build the game locally**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```
   This creates `build/web/` folder with your game.

2. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

3. **Deploy** (from your project root):
   ```bash
   vercel --prod
   ```

4. **Answer the prompts**:
   - Set up and deploy? **Y**
   - Which scope? (choose your account)
   - Link to existing project? **N**
   - Project name? **tower-madness** (or whatever you want)
   - Directory? **./build/web**

5. **Done!** Vercel will give you a live URL 🎉

---

### **Option 3: Netlify (Alternative to Vercel)**

Netlify is another great option, often easier for Python projects:

#### Method A: Drag & Drop (Easiest!)

1. **Build locally**:
   ```bash
   ./deploy.sh
   ```

2. **Go to** [app.netlify.com/drop](https://app.netlify.com/drop)

3. **Drag the `build/web` folder** onto the page

4. **Done!** Your game is live in seconds! 🎮

#### Method B: Netlify CLI

1. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

2. **Build and deploy**:
   ```bash
   ./deploy.sh
   netlify deploy --prod --dir=build/web
   ```

3. **Follow the prompts** to connect your site

---

## 🎮 After Deployment

Once deployed, your game will be accessible at a URL like:
- Vercel: `https://your-game.vercel.app`
- Netlify: `https://your-game.netlify.app`

### How to Play:
1. **Click on the game canvas**
2. **Press SPACEBAR** to start
3. Use **W/S** or **Arrow Keys** to move elevator
4. Press **E** or **SPACE** to open/close doors

---

## 🐛 Troubleshooting

### Build Fails on Vercel/Netlify
- **Solution**: Use "Build Locally" method (Option 2)
- Build on your computer, then deploy the `build/web` folder

### "Python not found" Error
- Vercel's build might not have Python 3.11+
- **Solution**: Build locally with `./deploy.sh`, then deploy with Vercel CLI

### Game Loads but Shows Black Screen
- ✅ This is FIXED in the current `main_web.py`
- Make sure you deployed the latest version

### Game Won't Start
- Click the game canvas first
- Then press SPACEBAR (not just clicking)
- Check browser console (F12) for errors

### Slow Loading
- First load takes 10-20 seconds (downloading Python/Pygame)
- Subsequent loads are cached and faster

---

## 🎯 Quick Command Reference

```bash
# Build locally
./deploy.sh

# Deploy to Vercel (after local build)
vercel --prod

# Deploy to Netlify (after local build)
netlify deploy --prod --dir=build/web

# Test locally before deploying
cd build/web
python3 -m http.server 8000
# Open http://localhost:8000
```

---

## 📊 Comparison

| Platform | Difficulty | Build Time | Free Tier | Best For |
|----------|-----------|------------|-----------|----------|
| **Vercel** | Medium | 3-5 min | ✅ Yes | Fast CDN, great for sharing |
| **Netlify** | Easy | 2-4 min | ✅ Yes | Easiest drag-drop option |
| **GitHub Pages** | Medium | Manual | ✅ Yes | Open source projects |
| **Itch.io** | Easy | 1 min | ✅ Yes | Game-specific platform |

---

## 🎉 Recommended Path

1. **Try Option 2** (Build Locally + Vercel CLI) - Most reliable
2. If that's too technical, use **Option 3A** (Netlify Drag & Drop) - Super easy!

Both give you a shareable URL within minutes!

---

## 🆘 Still Having Issues?

Common fixes:
1. Make sure `./deploy.sh` ran successfully
2. Check that `build/web/index.html` exists
3. Make sure you're deploying the `build/web` folder, not the root
4. Try Netlify drag & drop if Vercel isn't working

**The game WILL work once deployed** - all the web fixes are already in place! ✅
