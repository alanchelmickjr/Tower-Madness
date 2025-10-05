#!/bin/bash
# Quick deployment script for Tower Madness web version

echo "🏢 Tower Madness - Web Deployment Script 🏢"
echo "=========================================="
echo ""

# Check if pygbag is installed
if ! python -c "import pygbag" 2>/dev/null; then
    echo "📦 Installing pygbag..."
    pip install pygbag
    echo "✅ Pygbag installed"
else
    echo "✅ Pygbag already installed"
fi

echo ""
echo "🔨 Building for web..."
echo "Using fixed main_web.py (black screen issue resolved)"
echo ""

# Build the game
pygbag main_web.py --build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📁 Build output is in: build/web/"
    echo ""
    echo "🚀 Deployment Options:"
    echo ""
    echo "1. Test Locally:"
    echo "   cd build/web && python -m http.server 8000"
    echo "   Then open: http://localhost:8000"
    echo ""
    echo "2. Deploy to GitHub Pages:"
    echo "   git checkout -b gh-pages"
    echo "   cp -r build/web/* ."
    echo "   git add ."
    echo "   git commit -m 'Deploy to GitHub Pages'"
    echo "   git push origin gh-pages"
    echo ""
    echo "3. Deploy to Vercel:"
    echo "   vercel --prod"
    echo ""
    echo "4. Deploy to Netlify:"
    echo "   netlify deploy --prod --dir=build/web"
    echo ""
    echo "📖 For more details, see DEPLOY_WEB.md"
    echo ""
else
    echo ""
    echo "❌ Build failed. Check errors above."
    echo ""
    echo "Common fixes:"
    echo "- Make sure pygame is installed: pip install pygame"
    echo "- Check that all game files are present"
    echo "- Try: pygbag --help for more options"
    echo ""
fi