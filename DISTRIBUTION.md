# 🎮 Tower Madness Distribution Options

Since web deployment via Pygbag is having issues, here are alternative ways to play Tower Madness:

## 1. 🐍 Direct Python Execution (Easiest)
**Requirements:** Python 3.8+ and pygame

```bash
# Install Python from python.org
# Clone the repo
git clone https://github.com/alanchelmickjr/Tower-Madness.git
cd Tower-Madness

# Install pygame
pip install pygame

# Run the game
python main.py
```

## 2. 🎯 Standalone Executable with PyInstaller
Create a single executable file that runs without Python installed:

```bash
# Install PyInstaller
pip install pyinstaller

# Create standalone executable
pyinstaller --onefile --windowed --add-data "game:game" --add-data "docs:docs" --icon=icon.ico main.py

# Find executable in dist/ folder
# Windows: Tower-Madness.exe
# Mac: Tower-Madness.app
# Linux: Tower-Madness
```

## 3. 🐳 Docker Container
Run in a containerized environment:

```dockerfile
# Dockerfile
FROM python:3.9-slim
RUN apt-get update && apt-get install -y python3-pygame
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

```bash
docker build -t tower-madness .
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix tower-madness
```

## 4. 📦 Python Package (pip install)
Package and distribute via PyPI:

```bash
# Create setup.py
python setup.py sdist bdist_wheel
twine upload dist/*

# Users can then:
pip install tower-madness
tower-madness  # Run from anywhere
```

## 5. 🎮 itch.io Desktop App
Upload to itch.io as a downloadable game:
1. Create PyInstaller executable
2. Zip with all assets
3. Upload to itch.io
4. Players download and run directly

## 6. 🖥️ Replit Online IDE
Share as a Replit project:
1. Import GitHub repo to Replit
2. Configure run command
3. Share link - plays in browser terminal

## 7. 🚀 Steam Distribution
For wider reach:
1. Create executable with PyInstaller
2. Apply to Steam Direct ($100 fee)
3. Upload build to Steamworks
4. Distribute on Steam platform

## 8. 🏗️ Arcade Cabinet Mode
For events at Frontier Tower:
```bash
# Full screen arcade mode
python main.py --fullscreen --arcade

# Or modify main.py to auto-start in kiosk mode
```

## 9. 📱 Termux on Android
Run on Android devices:
```bash
# In Termux app
pkg install python
pip install pygame
git clone https://github.com/alanchelmickjr/Tower-Madness.git
cd Tower-Madness
python main.py
```

## 10. 🌐 Alternative Web Frameworks
Instead of Pygbag, try:
- **Transcrypt**: Python to JavaScript transpiler
- **Skulpt**: Python in browser
- **Brython**: Python 3 in browser
- **Pyodide**: Full Python stack in WebAssembly

## Quick Start Script
```bash
#!/bin/bash
# install_and_play.sh
echo "Installing Tower Madness..."
pip install pygame
git clone https://github.com/alanchelmickjr/Tower-Madness.git
cd Tower-Madness
echo "Starting game..."
python main.py
```

## Recommended Approach for SF Tech Week
For the hackathon and demo:
1. **Primary**: Direct Python execution on demo laptops
2. **Backup**: PyInstaller executables on USB drives
3. **Share**: GitHub repo with simple install instructions
4. **Future**: Fix Pygbag or use alternative web framework

## System Requirements
- **Minimum**: Python 3.8, 512MB RAM, Any OS
- **Recommended**: Python 3.9+, 1GB RAM, Hardware acceleration
- **Controls**: Keyboard (W/S/E or Arrow keys + Space)

## Troubleshooting
- **No module pygame**: Run `pip install pygame`
- **No audio**: Install SDL_mixer: `apt-get install python3-pygame`
- **Slow performance**: Disable AI sprite generation in config
- **Black screen**: Check pygame version: `pip install pygame==2.6.0`

## Contact
- GitHub: https://github.com/alanchelmickjr/Tower-Madness
- Issues: https://github.com/alanchelmickjr/Tower-Madness/issues
- SF Tech Week Demo: Floor 2 - The Spaceship