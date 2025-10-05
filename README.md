# 🏢 Tower Madness: Elevator Operator Simulator
## 🎮 Elevator Operator - The Flagship Game

### Overview
**Elevator Operator** is a retro-style arcade game set in the chaotic Frontier Tower in downtown San Francisco. Built specifically for 2-player arcade cabinets, this game brings cooperative and competitive gameplay to the vertical chaos of a 16-floor tech hub.

As the elevator operator (or operators in 2-player mode!), you must navigate the social dynamics, special events, and disasters while managing an increasingly complex cast of characters and situations. Experience the gritty reality of downtown SF - dodge obstacles just to reach the building entrance, hope the doorman John is at his post, and manage an elevator full of tech workers, artists, robots, and the occasional disaster.

### 🕹️ 2-Player Arcade Cabinet Support
- **Cooperative Mode**: Work together to manage the chaos
- **Competitive Mode**: See who can serve passengers better
- **Split Controls**: Player 1 controls elevator movement, Player 2 manages doors and special systems
- **Shared Disasters**: Both players must coordinate during emergencies
- **Dual Scoring**: Individual and team scores tracked simultaneously

### 🌆 Setting: Frontier Tower SF
Based on the real [frontiertower.io](https://frontiertower.io), the game captures the essence of a vertical village for frontier technologies:

**Street Level Challenges:**
- Navigate homeless encampments and urban obstacles
- Avoid aggressive panhandlers and street hazards
- Dodge piles of... urban debris
- Race to the singular entrance before unwanted followers slip in
- Hope doorman John is at his post (he's not always there!)

### 🏗️ Core Game Features

#### Dynamic Floor System
Each of the 16 floors (+2 special floors) offers unique experiences:

**Floor Layout:**
- **Street Level**: Urban obstacle course to building entrance
- **Floor 1 (Lobby)**: Meet doorman John, choose your destination
- **Floor 2 (Event Space)**: "The Spaceship" - large open meeting area with tech events
- **Floor 3**: Private offices with stressed startup founders
- **Floor 4 (Robotics Lab)**: Epic robot headquarters! Home to Alan the head robot (tour guide extraordinaire), 7 G1 Unitrees, 5 Compaq boosters, 4 big robots, 1 AGI warehouse bot, 20 LeRobot arms, 10 Lekiwi robots, 2 XLE robots, 4 mini fighting bots, 1 Earth rover, AGX Xavier monitoring system, and many more! Run by Vitaly and Xenia
- **Floor 5**: Movement Floor & Fitness Center - yoga practitioners and gym bros
- **Floor 6**: Arts & Music - creative chaos and impromptu performances
- **Floor 7**: Frontier Maker Space - dangerous machinery and flying sparks
- **Floor 8**: Neuro & Biotech Labs - scientists with questionable experiments
- **Floor 9**: AI & Autonomous Systems - rogue robots and AI researchers
- **Floor 10**: Frontier @ Accelerate - venture capitalists and pitch events
- **Floor 11**: Health & Longevity - biohackers and supplement enthusiasts
- **Floor 12**: Ethereum & DeFi - crypto bros and blockchain evangelists
- **Floor 14**: Human Flourishing - meditation circles and philosophy debates
- **Floor 15**: Coworking & Library - silent workers who hate noise
- **Floor 16**: d/acc Lounge - cross-pollination and networking chaos
- **Basement**: Secret Robot Fight Club (unlockable)
- **Roof**: Motor Room Access (secret achievement floor)
- **Loading Dock**: Trash area behind building (special events)

#### 🎯 Gameplay Mechanics

**Elevator Operations:**
- Manual elevator control (up/down/stop)
- Door open/close timing mechanics
- Weight limit management
- Speed vs. safety trade-offs
- Emergency stop capabilities

**Passenger Management:**
- Pick up and drop off various character types
- Handle impatient passengers
- Manage conflicting passenger requests
- Deal with VIPs and special guests
- Navigate social dynamics between floors

#### 🎨 AI-Powered Features

**Sprite Generator System:**
- Describe any character and get instant retro pixel art
- Dynamic sprite generation for NPCs
- Customizable art style (8-bit, 16-bit, CGA, etc.)
- Emotion and animation states
- Procedural variation system

**Floor Generator:**
- Text-to-floor conversion system
- Describe a floor concept → playable level
- Dynamic event scripting
- Procedural room layouts
- Custom challenge generation

#### 💥 Special Events & Disasters

**Random Events:**
- **Flood**: Water rising from basement, electrical hazards
- **Power Outage**: Navigate in darkness with emergency lighting
- **Overcrowding**: 100+ people trying to pack into elevator
- **Elevator Malfunction**: Creaking sounds, cable issues, stuck between floors
- **Fire Alarm**: Mass evacuation chaos
- **VIP Visit**: Clear elevator for important guests
- **Robot Uprising**: Basement robots escape to upper floors
- **Crypto Crash**: Panicked traders on Floor 12
- **Biohazard Leak**: Floor 8 contamination event
- **Protest**: Activists block certain floors
- **Earthquake**: Building shaking, debris falling

**Special Scenarios:**
- Morning Rush Hour
- Lunch Break Chaos
- Happy Hour Mayhem
- Late Night Weirdness
- Weekend Ghost Town

### 🔧 Technical Architecture

#### Stackable Framework Design
The game is built as a modular framework allowing integration of other retro games:

**Core Systems:**
```
tower-madness/
├── core/
│   ├── engine/          # Main game engine
│   ├── sprites/         # Sprite generation system
│   ├── physics/         # Movement and collision
│   └── events/          # Event management system
├── games/
│   ├── elevator/        # Elevator Operator game
│   ├── robot_fighter/   # Robot Fighter mini-game
│   └── chemical_mixer/  # Chemical Mixer puzzle game
├── shared/
│   ├── assets/          # Shared sprites and sounds
│   ├── ui/              # Common UI components
│   └── utils/           # Shared utilities
└── generators/
    ├── sprite_gen/      # AI sprite generator
    ├── floor_gen/       # Floor description parser
    └── event_gen/       # Dynamic event system
```

**Integration Points:**
- Mini-games accessible from specific floors
- Shared character system across games
- Unified scoring and progression
- Cross-game achievements
- Modular asset pipeline

### 📖 Game Storylines & Narrative
**Complete narrative documentation available in [docs/GAME_STORYLINES.md](docs/GAME_STORYLINES.md)**

**Main Story Arc: "Rise to the Top (Before the Robots Do)"**
- Start on the chaotic streets of SF
- Dodge homeless, say hi to John the doorman
- Progress through 16 floors of increasing chaos
- Discover the robot conspiracy in the basement
- Ultimate secret: The roof isn't just a motor room - it's a RAVE! 🎉

**Key Narrative Elements:**
- John the doorman is actually an android
- The basement hosts a secret robot fight club
- Floor 4 robotics engineers hear the roof rave while building
- APEX-7 (lead robot) is secretly the roof rave DJ
- Three different endings based on your choices
- New Game+ reveals "the real game"

### 📋 User Stories

#### Epic: Core Gameplay Loop
**As a player, I want to operate an elevator in a chaotic tech building**

**User Story 1: Street Navigation**
```
GIVEN I am starting a new game
WHEN I begin on the street level
THEN I must navigate obstacles to reach the building entrance
AND avoid unwanted followers
AND hope the doorman is present
```

**User Story 2: Elevator Control**
```
GIVEN I am operating the elevator
WHEN I receive passenger requests
THEN I can move up/down between floors
AND open/close doors at appropriate times
AND manage passenger satisfaction
```

**User Story 3: Passenger Management**
```
GIVEN passengers are waiting on different floors
WHEN I arrive at their floor
THEN they board if there's space
AND express satisfaction/frustration based on wait time
AND tip based on service quality
```

#### Epic: AI-Generated Content
**As a player, I want dynamically generated content for variety**

**User Story 4: Character Generation**
```
GIVEN the sprite generator system
WHEN a new NPC is needed
THEN the AI generates a unique retro sprite
AND assigns personality traits
AND creates appropriate dialogue
```

**User Story 5: Floor Experiences**
```
GIVEN the floor generator system
WHEN I visit a floor
THEN unique events occur based on floor theme
AND NPCs behave according to floor context
AND environmental hazards match the setting
```

#### Epic: Special Events
**As a player, I want unexpected challenges to keep gameplay exciting**

**User Story 6: Disaster Management**
```
GIVEN a disaster event triggers
WHEN I must respond to the emergency
THEN I need to evacuate passengers safely
AND manage panic levels
AND minimize casualties for bonus points
```

**User Story 7: Secret Areas**
```
GIVEN I discover the basement robot fight club
WHEN I complete special requirements
THEN I unlock mini-game access
AND can earn special rewards
AND unlock new character types
```

#### Epic: Progression System
**As a player, I want to feel progression and achievement**

**User Story 8: Scoring System**
```
GIVEN I complete elevator runs
WHEN I transport passengers efficiently
THEN I earn points based on:
- Speed of service
- Passenger satisfaction
- Special event handling
- Combos and streaks
AND unlock new features and floors
```

**User Story 9: Achievements**
```
GIVEN various gameplay challenges exist
WHEN I complete specific objectives
THEN I unlock achievements like:
- "Doorman's Friend" - John always at post
- "Disaster Master" - Survive all disaster types
- "Roof Access" - Reach the secret motor room
- "Fight Club Member" - Win robot tournament
```

### 🎮 Game Modes

**Story Mode:**
- Progressive difficulty through work week
- Unlock floors gradually
- Character storylines develop
- Special event sequences
- Supports 2-player co-op storytelling

**Arcade Mode (Optimized for Cabinet Play):**
- High score challenge
- All floors unlocked
- Increasing disaster frequency
- Endless play until failure
- 2-player competitive/cooperative modes
- Designed for quick sessions at events

**Sandbox Mode:**
- Create custom scenarios
- Test floor generator
- Design character sprites
- Share creations with community
- Build 2-player challenges

**2-Player Modes:**
- **Co-op Campaign**: Work together through story mode
- **Versus Mode**: Compete for best elevator operator
- **Chaos Mode**: One player causes problems, other fixes them
- **Tag Team**: Switch control every 2 minutes

### 🚀 Getting Started

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Quick Installation
```bash
# Clone the repository
git clone https://github.com/alanchelmickjr/Tower-Madness.git
cd Tower-Madness

# Install dependencies
pip install -r requirements.txt

# Set up OpenAI API (optional, for AI-generated NPC sprites)
cp .env.example .env.local
# Edit .env.local and add your OpenAI API key from https://platform.openai.com/api-keys

# Run the game!
python main.py
```

#### Controls
- **↑/W**: Move elevator up
- **↓/S**: Move elevator down
- **SPACE**: Open/close doors
- **ESC**: Pause game
- **R**: Restart (when game over)

#### Configuration
```python
# config.py
GAME_CONFIG = {
    'difficulty': 'normal',  # easy, normal, hard, chaos
    'ai_sprites': True,      # Enable AI sprite generation
    'floor_generator': True,  # Enable dynamic floors
    'disasters': True,        # Enable random disasters
    'mini_games': True,       # Enable integrated mini-games
    'players': 2,            # Number of players (1 or 2)
    'arcade_mode': True      # Enable arcade cabinet features
}

# Arcade Cabinet Controls (2-Player Setup)
PLAYER_1_CONTROLS = {
    'up': 'W',
    'down': 'S',
    'left': 'A',
    'right': 'D',
    'action': 'G',
    'special': 'H'
}

PLAYER_2_CONTROLS = {
    'up': 'UP_ARROW',
    'down': 'DOWN_ARROW',
    'left': 'LEFT_ARROW',
    'right': 'RIGHT_ARROW',
    'action': 'NUMPAD_4',
    'special': 'NUMPAD_5'
}
```

### 🛠️ Development

#### Adding New Floors
```python
# floors/custom_floor.py
class CustomFloor(BaseFloor):
    def __init__(self):
        super().__init__(
            floor_number=17,
            name="Secret Lab",
            description="Top secret experiments"
        )
    
    def generate_npcs(self):
        return [
            NPC("Mad Scientist", sprite="scientist_crazy"),
            NPC("Test Subject", sprite="human_glowing")
        ]
    
    def special_events(self):
        return ["explosion", "mutation", "portal_opening"]
```

#### Creating Custom Sprites
```python
# generators/sprite_gen.py
sprite = generate_sprite(
    description="Disheveled tech founder, hasn't slept in days",
    style="16-bit",
    emotion="stressed",
    animation_frames=4
)
```

#### Implementing Disasters
```python
# events/disasters.py
class FloodDisaster(BaseDisaster):
    def trigger(self, elevator, floors):
        self.water_level = 0
        self.rising_speed = 0.5
        self.affected_floors = [1, 2, 3, "basement"]
        
    def update(self, dt):
        self.water_level += self.rising_speed * dt
        if self.water_level > floor.height:
            floor.flooded = True
```

### 🎯 Roadmap

**Phase 1: Core Elevator Game** ✅
- Basic elevator mechanics
- 16 floor implementation
- Simple passenger AI
- Score system

**Phase 2: AI Integration** 🚧
- Sprite generator implementation
- Floor generator system
- Dynamic NPC dialogue
- Procedural events

**Phase 3: Special Features** 📋
- Disaster system
- Secret areas (basement, roof)
- Mini-game integration
- Achievement system

**Phase 4: Polish & Expansion** 📋
- Mobile port
- Arcade cabinet support ✅
- 2-player modes ✅
- SF Tech Week Algorave debut 🎉
- Online leaderboards
- Community content sharing

### 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas Needing Help:**
- Pixel art and sprites
- Sound effects and music (especially for Algorave!)
- Floor ideas and events
- Disaster scenarios
- Character dialogue
- Game balancing
- 2-player gameplay mechanics
- Arcade cabinet optimization

### 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

### 🙏 Acknowledgments

- Inspired by classic elevator games and SimTower
- Frontier Tower SF for the setting inspiration
- The Pygame community for excellent documentation
- SF Tech Week for hosting us at Algorave
- The arcade cabinet hardware providers
- Alan and the Floor 4 Robotics Lab crew who are definitely planning something
- Vitaly and Xenia for running the epic robotics floor
- All contributors and playtesters

### 📞 Contact

- **GitHub**: [Tower Madness Repository](https://github.com/alanchelmickjr/Tower-Madness)
- **Live at**: Frontier Tower, Floor 2 - Retro Arcade Hackathon (RIGHT NOW!)
- **Coming to**: SF Tech Week Algorave
- **Building**: 1062 Folsom St, San Francisco, CA

---

**Remember:** In downtown SF, even getting to work is an adventure. Good luck, Elevator Operator!

**🎮 See you at the SF Tech Week Algorave - bring a friend for 2-player action on the arcade cabinet!**

---

## 📚 Complete Documentation

- **[Game Storylines & Narratives](docs/GAME_STORYLINES.md)** - Full story arcs, character development, and narrative beats
- **[User Stories](docs/USER_STORIES.md)** - Detailed agile user stories with acceptance criteria
- **[AI Sprite Generator](docs/AI_SPRITE_GENERATOR.md)** - Dynamic sprite generation system
- **[Floor Generator](docs/FLOOR_GENERATOR.md)** - Text-to-floor level generation
- **[Events & Disasters](docs/EVENTS_AND_DISASTERS.md)** - Complete disaster system
- **[Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)** - Stackable framework design
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Integration APIs for new games

**Ready to build? The documentation is complete. Time to make it real!** 🚀
