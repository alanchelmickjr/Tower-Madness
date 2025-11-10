# 🚀 Deploy to Vercel Pro - Quick Guide

You have Vercel Pro! This gives you better build resources and is perfect for this Python/Pygame project.

## ⚡ Quick Deploy (2 Methods)

---

### **Method 1: GitHub Integration (Easiest)**

1. **Go to** [vercel.com/new](https://vercel.com/new)

2. **Import your GitHub repository**: `Tower-Madness`

3. **Configure Build Settings**:
   ```
   Framework Preset: Other
   Root Directory: ./
   Build Command: pip3 install pygbag && python3 -m pygbag --build main_web.py
   Output Directory: build/web
   Install Command: (leave empty)
   ```

4. **Deploy!**

5. **If it fails with Python errors**, use Method 2 below

---

### **Method 2: Pre-Build + Deploy (100% Reliable)**

If Method 1 fails due to Python version issues, this ALWAYS works:

```bash
# 1. Build on your machine
chmod +x deploy.sh
./deploy.sh

# 2. Verify build succeeded
ls build/web/index.html  # Should exist

# 3. Deploy to Vercel
vercel build/web --prod

# OR navigate first:
cd build/web
vercel --prod
```

This deploys the pre-built static files (no Python needed on Vercel).

---

## 🎯 Why Vercel Pro is Perfect for This

- ✅ Better build resources (Python + pygbag need memory)
- ✅ More build minutes (pygbag takes 2-4 minutes)
- ✅ Global CDN for fast game loading
- ✅ Easy custom domains
- ✅ Analytics to see player engagement

---

## 🐛 Troubleshooting

### "Python not found" during build
- **Solution**: Use Method 2 (pre-build locally)
- Vercel's build environment might not have Python 3.11+

### Build timeout
- Unlikely with Pro, but if it happens, use Method 2

### 404 errors after deployment
- Check that Output Directory is set to `build/web`
- Make sure `index.html` is in the root of that directory

### Game shows black screen
- ✅ Already fixed in `main_web.py`
- Clear browser cache and reload

---

## 🎮 After Deployment

Your game will be live at: `https://tower-madness-[random].vercel.app`

### Custom Domain (Pro Feature!)
1. Go to your project settings in Vercel
2. Add your custom domain
3. Vercel will handle SSL automatically

### Analytics (Pro Feature!)
Check your Vercel dashboard to see:
- How many people are playing
- Load times
- Geographic distribution

---

## 💡 Recommended Approach

1. **Try Method 1 first** (GitHub integration)
   - Let Vercel build it automatically
   - Easiest if it works

2. **If Method 1 fails**, use **Method 2**
   - Build locally with `./deploy.sh`
   - Deploy with `vercel build/web --prod`
   - This method is 100% reliable

---

## 🚀 One-Liner Deploy (Method 2)

```bash
./deploy.sh && cd build/web && vercel --prod
```

That's it! Your Pygame game will be live on Vercel with Pro performance! 🎉

---

## 📊 Vercel Pro Benefits You're Using

- ⚡ Edge network (fast worldwide)
- 📈 Analytics dashboard
- 🔒 DDoS protection
- 🌐 Easy custom domains
- 💪 Better build resources
- ⏱️ More build minutes

You made the right choice with Vercel Pro for this project!
