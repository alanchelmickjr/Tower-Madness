# 🎮 KEYBOARD NOT WORKING? - TROUBLESHOOTING GUIDE

## The Problem: Keyboard Focus in Browsers

Web browsers need to know which element should receive keyboard input. If you're seeing the game but keys don't work, the game canvas doesn't have "focus."

---

## ✅ SOLUTION 1: Click the Game Screen

**The easiest fix:**

1. Wait for the game to load (you'll see "TOWER MADNESS" title)
2. **Click anywhere on the dark/cyan game screen**
3. You should see a cyan border around the game
4. Now press **SPACEBAR** 
5. Game should start!

---

## ✅ SOLUTION 2: Check Browser Console

Open your browser's developer console to see what's happening:

**How to open console:**
- **Chrome/Edge:** Press `F12` or `Ctrl+Shift+J` (Windows) / `Cmd+Option+J` (Mac)
- **Firefox:** Press `F12` or `Ctrl+Shift+K`
- **Safari:** Enable Developer menu first, then `Cmd+Option+C`

**What to look for:**
1. Click on the game canvas
2. Press SPACEBAR
3. You should see: `Key pressed: Space SPACE` in the console
4. If you don't see this, the canvas doesn't have focus

---

## ✅ SOLUTION 3: Refresh and Try Again

Sometimes the canvas doesn't load properly:

1. **Hard refresh:** `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Wait for loading to complete
3. Click the game screen
4. Try pressing SPACEBAR

---

## ✅ SOLUTION 4: Check Browser Compatibility

Pygbag (the web converter) works best with:
- ✅ **Chrome** - Best performance
- ✅ **Firefox** - Works well
- ✅ **Edge** - Good performance
- ⚠️ **Safari** - May have WebAssembly issues
- ❌ **Internet Explorer** - Not supported

**If using Safari:** Try Chrome or Firefox instead.

---

## ✅ SOLUTION 5: Try Desktop Version First

To verify the game itself works:

```bash
python main.py
```

If the desktop version works but web doesn't, it's a browser/keyboard focus issue.

---

## 🐛 Still Not Working? Debug Steps:

1. **Open browser console (F12)**
2. **Click the game canvas**
3. **Type this in console:**
   ```javascript
   document.getElementById('pygame-canvas').focus();
   ```
4. **Press ENTER**
5. **Now try pressing SPACEBAR in the game**

If this works, it's definitely a focus issue. The updated `index.html` should fix this automatically.

---

## 🔍 Advanced Debugging

**Check if canvas exists:**
```javascript
console.log(document.getElementById('pygame-canvas'));
```

**Check if Pygbag loaded:**
```javascript
console.log(window.pyodide);
```

**Force focus on canvas:**
```javascript
const canvas = document.getElementById('pygame-canvas');
canvas.setAttribute('tabindex', '0');
canvas.focus();
canvas.addEventListener('keydown', (e) => console.log('Key:', e.key));
```

---

## 💡 Why This Happens

Web browsers have security features that prevent pages from capturing keyboard input without user interaction. The game canvas needs to:

1. Be clickable (tabindex attribute)
2. Have focus (user must click it)
3. Listen for keyboard events

The updated `index.html` now handles this automatically, but you still need to **click the game screen first** before pressing keys.

---

## ✅ Expected Behavior

When working correctly:
1. Game loads → Shows "TOWER MADNESS"
2. You click the canvas → Cyan border appears
3. You press SPACEBAR → Game starts
4. You press W/S → Elevator moves
5. You press E → Doors open/close

---

## 🆘 Last Resort: Manual HTML Setup

If nothing works, create a simple test file:

```html
<!DOCTYPE html>
<html>
<body>
<h1>Keyboard Test</h1>
<canvas id="pygame-canvas" tabindex="0" width="1024" height="768" 
        style="border: 3px solid cyan;">
</canvas>
<script>
const canvas = document.getElementById('pygame-canvas');
canvas.addEventListener('keydown', (e) => {
    console.log('Key pressed:', e.key);
    alert('Key works: ' + e.key);
});
canvas.focus();
alert('Click the canvas then press any key');
</script>
</body>
</html>
```

Save as `test.html`, open in browser, click canvas, press a key. If this works, your browser is fine.

---

**Need more help? Check the browser console for error messages and share them for debugging!**