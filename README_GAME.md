# Tower Madness - Elevator Operator 🏢🤖

An arcade-ready retro game for SF Tech Week Algorave where you operate an elevator caught between good and evil!

## 🎮 Game Narrative

You are the elevator operator in a mysterious tower where:
- **Floor 4**: The GOOD Robot Lab - Where loving robots are built to counter evil (cyan/blue theme)
- **Basement (-1)**: The EVIL Robot Fight Club - Red-lit cage battles of chaos
- **Roof (Floor 5)**: The escape route to the legendary roof rave!

You're caught between these two factions, trying to deliver NPCs to their destinations while managing the balance between chaos and harmony.

## 🕹️ How to Play

### Controls
**Player 1 (Keyboard)**:
- `W` / `S` - Move elevator up/down
- `E` - Open/close doors
- `SPACE` - Action button

**Player 2 (Keyboard)**:
- `↑` / `↓` - Move elevator up/down  
- `Right Shift` - Open/close doors
- `Enter` - Action button

### Gameplay
1. NPCs spawn at different floors with destinations
2. Open doors to let NPCs in/out of the elevator
3. Deliver them to their desired floors for points
4. Watch out for special characters like John the Doorman!
5. Balance chaos and harmony levels

### Scoring
- Basic delivery: 10 points
- Good robots to Floor 4: +20 bonus
- Evil robots to Basement: +15 bonus
- Anyone escaping to roof: +25 bonus
- John the Doorman: +50 bonus!

## 🚀 Quick Start

### Requirements
- Python 3.8+
- Pygame 2.5+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tower-madness.git
cd tower-madness
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the game:
```bash
python main.py
```

## 🎪 Arcade Cabinet Setup

The game is designed for arcade cabinet deployment at events like SF Tech Week Algorave:

1. Edit `config.py`:
```python
ARCADE_MODE = True
FULLSCREEN = True
CURRENT_DISPLAY_MODE = "sf_tech_week"  # 1920x1080
```

2. For 2-player arcade setup:
- Map joystick inputs to keyboard keys
- Configure button mappings in `config.py`

## 🏗️ Project Structure

```
Tower Madness/
├── main.py                 # Entry point
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── game/
│   ├── core/
│   │   ├── engine.py     # Game engine
│   │   └── constants.py  # Game constants
│   ├── entities/
│   │   ├── elevator.py   # Elevator entity
│   │   ├── floor.py      # Floor entity
│   │   └── npc.py        # NPC classes
│   └── scenes/
│       └── elevator_scene.py  # Main gameplay
```

## 🎨 Features

### Current Features
- ✅ Epic retro intro screen with animated elevator shaft
- ✅ Dynamic NPC spawning (good robots, evil robots, neutral)
- ✅ Special character: John the Doorman
- ✅ Floor 4: Good Robot Lab with healing aura effects
- ✅ Basement: Evil Robot Fight Club with red lighting
- ✅ Chaos/Harmony balance system
- ✅ 2-player support
- ✅ Arcade cabinet ready
- ✅ Visual effects (screen shake, flash, particles)

### Planned Features
- 🔄 Robot Fighter mini-game
- 🔄 16-floor side-to-side climber mode
- 🔄 AI-powered narrative generation
- 🔄 Procedural floor generation
- 🔄 Online leaderboards
- 🔄 Beat-sync for Algorave events

## 🎵 For SF Tech Week Algorave

Special features for the event:
- Attract mode when idle
- QR code display for info
- Party mode visual effects
- Beat synchronization (coming soon)

## 🤝 Contributing

This is an open-source project for the SF Tech Week community! Feel free to:
- Add new floor types
- Create new NPC characters
- Enhance visual effects
- Add sound/music
- Improve the narrative system

## 📝 License

MIT License - Free for all to enjoy at raves and arcades!

## 🙏 Credits

Created for SF Tech Week Algorave 2024
Special thanks to John the Doorman - connecting us all!

---

**Remember**: In Tower Madness, you're not just operating an elevator - you're navigating the space between good and evil, chaos and harmony, basement fight clubs and rooftop raves! 🎮✨