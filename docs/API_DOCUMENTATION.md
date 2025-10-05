
# 🎮 API Documentation - Game Integration & 2-Player Support

## Overview
This document provides comprehensive API documentation for integrating new retro games into the Tower Madness framework, with special focus on 2-player arcade console support using Pygame.

## Table of Contents
- [Quick Start](#quick-start)
- [Core APIs](#core-apis)
- [Game Integration API](#game-integration-api)
- [2-Player Support](#2-player-support)
- [Arcade Console API](#arcade-console-api)
- [Mini-Game API](#mini-game-api)
- [Shared Services API](#shared-services-api)
- [Event System API](#event-system-api)
- [Input Handling API](#input-handling-api)
- [Asset Management API](#asset-management-api)
- [Examples](#examples)

## Quick Start

### Creating a New Game Module

```python
from tower_madness.core import GameModule, SharedContext
from tower_madness.arcade import ArcadeInput
import pygame

class MyRetroGame(GameModule):
    """Quick start example for new retro game."""
    
    def __init__(self):
        super().__init__()
        self.supports_2_player = True  # Enable 2-player support
        
    def initialize(self, context: SharedContext):
        """Initialize your game."""
        self.context = context
        self.players = []
        
        # Setup for 2-player arcade
        if context.platform == "arcade":
            self.setup_arcade_controls()
            
    def setup_arcade_controls(self):
        """Configure arcade cabinet controls."""
        self.p1_controls = ArcadeInput.PLAYER_1
        self.p2_controls = ArcadeInput.PLAYER_2
        
    def update(self, dt: float):
        """Update game logic."""
        # Handle both players
        for player_id, player in enumerate(self.players):
            controls = self.p1_controls if player_id == 0 else self.p2_controls
            self.update_player(player, controls, dt)
            
    def render(self, screen: pygame.Surface):
        """Render game."""
        # Render split-screen or shared view
        if len(self.players) == 2:
            self.render_split_screen(screen)
        else:
            self.render_single_player(screen)
```

### Registering Your Game

```python
from tower_madness import GameRegistry

# Register your game
registry = GameRegistry()
registry.register_game(
    game_id="my_retro_game",
    game_class=MyRetroGame,
    metadata={
        "name": "My Retro Game",
        "max_players": 2,
        "arcade_compatible": True,
        "mini_game": True
    }
)
```

## Core APIs

### GameModule Base Class

```python
class GameModule:
    """
    Base class for all game modules.
    All games must inherit from this class.
    """
    
    def __init__(self):
        """Initialize game module."""
        self.game_id: str = ""
        self.name: str = ""
        self.supports_2_player: bool = False
        self.is_mini_game: bool = False
        self.requires_floor: Optional[int] = None
        
    @abstractmethod
    def initialize(self, context: SharedContext) -> None:
        """
        Initialize game with shared context.
        
        Args:
            context: Shared context containing resources and services
        """
        pass
        
    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update game logic.
        
        Args:
            dt: Delta time in seconds since last update
        """
        pass
        
    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """
        Render game to screen.
        
        Args:
            screen: Pygame surface to render to
        """
        pass
        
    @abstractmethod
    def handle_input(self, event: pygame.event.Event) -> None:
        """
        Handle input events.
        
        Args:
            event: Pygame event to process
        """
        pass
        
    def pause(self) -> None:
        """Called when game is paused."""
        pass
        
    def resume(self) -> None:
        """Called when game is resumed."""
        pass
        
    def cleanup(self) -> None:
        """Clean up resources when game ends."""
        pass
        
    def get_save_data(self) -> dict:
        """
        Get game state for saving.
        
        Returns:
            Dictionary containing saveable game state
        """
        return {}
        
    def load_save_data(self, data: dict) -> None:
        """
        Load game state from save data.
        
        Args:
            data: Previously saved game state
        """
        pass
```

### SharedContext API

```python
class SharedContext:
    """
    Shared context passed to all games.
    Provides access to shared resources and services.
    """
    
    def __init__(self):
        self.platform: str  # "desktop", "mobile", "arcade"
        self.screen_size: Tuple[int, int]
        self.player_count: int
        self.save_system: SaveSystem
        self.achievement_system: AchievementSystem
        self.sprite_generator: SpriteGenerator
        self.audio_manager: AudioManager
        self.event_bus: EventBus
        self.resource_pool: ResourcePool
        
    def get_player_data(self, player_id: int = 0) -> PlayerData:
        """
        Get player data by ID.
        
        Args:
            player_id: Player ID (0 for P1, 1 for P2)
            
        Returns:
            Player data object
        """
        pass
        
    def broadcast_event(self, event: GameEvent) -> None:
        """
        Broadcast event to all listening games.
        
        Args:
            event: Event to broadcast
        """
        pass
        
    def load_shared_asset(self, asset_path: str) -> Any:
        """
        Load asset from shared pool.
        
        Args:
            asset_path: Path to asset
            
        Returns:
            Loaded asset (Surface, Sound, etc.)
        """
        pass
```

## Game Integration API

### Game Registration

```python
class GameRegistry:
    """Registry for managing game modules."""
    
    def register_game(
        self,
        game_id: str,
        game_class: Type[GameModule],
        metadata: dict = None
    ) -> None:
        """
        Register a new game module.
        
        Args:
            game_id: Unique identifier for game
            game_class: Class inheriting from GameModule
            metadata: Optional metadata about game
            
        Example:
            registry.register_game(
                "robot_fighter",
                RobotFighterGame,
                {
                    "name": "Robot Fighter",
                    "max_players": 2,
                    "arcade_compatible": True,
                    "category": "fighting"
                }
            )
        """
        pass
        
    def launch_game(
        self,
        game_id: str,
        player_count: int = 1,
        params: dict = None
    ) -> GameModule:
        """
        Launch a registered game.
        
        Args:
            game_id: ID of game to launch
            player_count: Number of players (1 or 2)
            params: Optional parameters for game
            
        Returns:
            Launched game instance
        """
        pass
        
    def get_game_list(self, filter: dict = None) -> List[GameInfo]:
        """
        Get list of available games.
        
        Args:
            filter: Optional filter criteria
            
        Returns:
            List of game information objects
        """
        pass
```

### Game Transitions

```python
class GameTransition:
    """Handle transitions between games."""
    
    @staticmethod
    def transition_to_mini_game(
        from_game: GameModule,
        mini_game_id: str,
        callback: Callable = None,
        params: dict = None
    ) -> None:
        """
        Transition from main game to mini-game.
        
        Args:
            from_game: Current game instance
            mini_game_id: ID of mini-game to launch
            callback: Function to call when mini-game completes
            params: Parameters to pass to mini-game
            
        Example:
            GameTransition.transition_to_mini_game(
                from_game=elevator_game,
                mini_game_id="robot_fighter",
                callback=lambda result: elevator_game.on_mini_game_complete(result),
                params={"difficulty": "hard", "rounds": 3}
            )
        """
        pass
        
    @staticmethod
    def return_to_main_game(
        mini_game: GameModule,
        result: dict
    ) -> None:
        """
        Return from mini-game to main game.
        
        Args:
            mini_game: Current mini-game instance
            result: Result data to pass back
        """
        pass
```

## 2-Player Support

### Player Management

```python
class PlayerManager:
    """Manage multiple players in games."""
    
    def __init__(self, max_players: int = 2):
        self.max_players = max_players
        self.players: List[Player] = []
        
    def add_player(self, player_id: int) -> Player:
        """
        Add a new player.
        
        Args:
            player_id: Player identifier (0 or 1)
            
        Returns:
            Created player object
            
        Example:
            p1 = player_manager.add_player(0)
            p2 = player_manager.add_player(1)
        """
        pass
        
    def get_player(self, player_id: int) -> Optional[Player]:
        """Get player by ID."""
        pass
        
    def remove_player(self, player_id: int) -> None:
        """Remove player from game."""
        pass
```

### Split-Screen Rendering

```python
class SplitScreenRenderer:
    """Handle split-screen rendering for 2-player games."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width, self.height = screen.get_size()
        
    def get_player_viewport(self, player_id: int) -> pygame.Rect:
        """
        Get viewport rectangle for player.
        
        Args:
            player_id: Player ID (0 or 1)
            
        Returns:
            Viewport rectangle for player
            
        Example:
            # Vertical split
            p1_viewport = renderer.get_player_viewport(0)
            # Returns Rect(0, 0, width/2, height)
            
            p2_viewport = renderer.get_player_viewport(1)
            # Returns Rect(width/2, 0, width/2, height)
        """
        if player_id == 0:
            return pygame.Rect(0, 0, self.width // 2, self.height)
        else:
            return pygame.Rect(self.width // 2, 0, self.width // 2, self.height)
            
    def render_split_screen(
        self,
        render_func: Callable,
        player_states: List[dict]
    ) -> None:
        """
        Render split-screen view.
        
        Args:
            render_func: Function to render single player view
            player_states: List of player states to render
            
        Example:
            renderer.render_split_screen(
                render_func=self.render_player_view,
                player_states=[p1_state, p2_state]
            )
        """
        for i, state in enumerate(player_states):
            viewport = self.get_player_viewport(i)
            subsurface = self.screen.subsurface(viewport)
            render_func(subsurface, state)
```

### Cooperative Gameplay

```python
class CooperativeGame(GameModule):
    """Base class for cooperative 2-player games."""
    
    def __init__(self):
        super().__init__()
        self.supports_2_player = True
        self.players = []
        self.shared_score = 0
        
    def handle_cooperative_action(
        self,
        player1_action: str,
        player2_action: str
    ) -> dict:
        """
        Handle cooperative actions between players.
        
        Args:
            player1_action: Player 1's action
            player2_action: Player 2's action
            
        Returns:
            Result of combined action
            
        Example:
            result = self.handle_cooperative_action(
                "push_button",
                "pull_lever"
            )
            # Returns {"success": True, "unlock": "secret_door"}
        """
        pass
        
    def sync_players(self) -> None:
        """Synchronize player states in co-op mode."""
        pass
```

## Arcade Console API

### Arcade Input Handling

```python
class ArcadeInput:
    """Handle arcade cabinet input for 2 players."""
    
    # Player 1 Controls (Left side)
    PLAYER_1 = {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d,
        "button_1": pygame.K_g,     # Primary action
        "button_2": pygame.K_h,     # Secondary action
        "button_3": pygame.K_j,     # Special
        "start": pygame.K_1,        # Start/Pause
        "coin": pygame.K_5          # Insert coin
    }
    
    # Player 2 Controls (Right side)
    PLAYER_2 = {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "button_1": pygame.K_KP4,    # Primary action
        "button_2": pygame.K_KP5,    # Secondary action
        "button_3": pygame.K_KP6,    # Special
        "start": pygame.K_2,         # Start/Pause
        "coin": pygame.K_6           # Insert coin
    }
    
    @classmethod
    def get_player_input(
        cls,
        player_id: int,
        event: pygame.event.Event
    ) -> Optional[str]:
        """
        Get input action for player.
        
        Args:
            player_id: Player ID (0 or 1)
            event: Pygame keyboard event
            
        Returns:
            Action string or None
            
        Example:
            action = ArcadeInput.get_player_input(0, event)
            if action == "button_1":
                player1.jump()
        """
        controls = cls.PLAYER_1 if player_id == 0 else cls.PLAYER_2
        
        if event.type == pygame.KEYDOWN:
            for action, key in controls.items():
                if event.key == key:
                    return action
        return None
        
    @classmethod
    def is_player_key(cls, key: int, player_id: int) -> bool:
        """Check if key belongs to specific player."""
        controls = cls.PLAYER_1 if player_id == 0 else cls.PLAYER_2
        return key in controls.values()
```

### Arcade Display Configuration

```python
class ArcadeDisplay:
    """Configure display for arcade cabinet."""
    
    # Standard arcade resolutions
    RESOLUTIONS = {
        "cga": (320, 200),
        "vga": (640, 480),
        "svga": (800, 600),
        "xga": (1024, 768),
        "hd": (1280, 720),
        "fhd": (1920, 1080)
    }
    
    @staticmethod
    def setup_arcade_display(
        resolution: str = "xga",
        fullscreen: bool = True,
        scanlines: bool = True
    ) -> pygame.Surface:
        """
        Setup display for arcade cabinet.
        
        Args:
            resolution: Resolution preset name
            fullscreen: Enable fullscreen mode
            scanlines: Add CRT scanline effect
            
        Returns:
            Configured display surface
            
        Example:
            screen = ArcadeDisplay.setup_arcade_display(
                resolution="xga",
                fullscreen=True,
                scanlines=True
            )
        """
        width, height = ArcadeDisplay.RESOLUTIONS[resolution]
        
        flags = pygame.SCALED
        if fullscreen:
            flags |= pygame.FULLSCREEN
            
        screen = pygame.display.set_mode((width, height), flags)
        
        if scanlines:
            ArcadeDisplay.add_scanline_effect(screen)
            
        return screen
        
    @staticmethod
    def add_scanline_effect(screen: pygame.Surface) -> None:
        """Add CRT scanline effect to screen."""
        pass
```

### Coin Operation

```python
class CoinSystem:
    """Handle coin-operated arcade functionality."""
    
    def __init__(self):
        self.credits = 0
        self.coins_per_credit = 1
        self.credits_per_play = 1
        
    def insert_coin(self) -> None:
        """
        Handle coin insertion.
        
        Example:
            coin_system.insert_coin()
            print(f"Credits: {coin_system.credits}")
        """
        self.credits += 1
        self.play_insert_sound()
        
    def can_start_game(self, players: int = 1) -> bool:
        """
        Check if enough credits to start game.
        
        Args:
            players: Number of players
            
        Returns:
            True if enough credits available
        """
        required_credits = self.credits_per_play * players
        return self.credits >= required_credits
        
    def start_game(self, players: int = 1) -> bool:
        """
        Deduct credits and start game.
        
        Args:
            players: Number of players
            
        Returns:
            True if game started successfully
        """
        if self.can_start_game(players):
            self.credits -= self.credits_per_play * players
            return True
        return False
```

## Mini-Game API

### Mini-Game Interface

```python
class MiniGame(GameModule):
    """Base class for mini-games."""
    
    def __init__(self):
        super().__init__()
        self.is_mini_game = True
        self.parent_game: Optional[GameModule] = None
        self.completion_callback: Optional[Callable] = None
        
    def set_parent_game(self, parent: GameModule) -> None:
        """Set reference to parent game."""
        self.parent_game = parent
        
    def set_completion_callback(self, callback: Callable) -> None:
        """Set callback for when mini-game completes."""
        self.completion_callback = callback
        
    def complete_mini_game(self, result: dict) -> None:
        """
        Complete mini-game and return to parent.
        
        Args:
            result: Result data to pass to parent
            
        Example:
            self.complete_mini_game({
                "success": True,
                "score": 1000,
                "unlocks": ["special_item"],
                "achievements": ["mini_game_master"]
            })
        """
        if self.completion_callback:
            self.completion_callback(result)
```

### Mini-Game Examples

```python
class RobotFighterMiniGame(MiniGame):
    """Robot fighting mini-game example."""
    
    def __init__(self):
        super().__init__()
        self.name = "Robot Fighter"
        self.supports_2_player = True
        
    def initialize(self, context: SharedContext):
        """Initialize robot fighter game."""
        super().initialize(context)
        
        # Generate robot sprites
        self.player_robots = []
        for i in range(context.player_count):
            robot = self.create_robot(player_id=i)
            self.player_robots.append(robot)
            
    def create_robot(self, player_id: int) -> Robot:
        """Create robot for player."""
        sprite = self.context.sprite_generator.generate(
            f"Battle robot for player {player_id + 1}",
            style="16bit"
        )
        return Robot(sprite=sprite, player_id=player_id)
        
    def handle_battle_end(self, winner: int) -> None:
        """Handle end of battle."""
        result = {
            "success": winner >= 0,
            "winner": winner,
            "score": self.calculate_score(),
            "rewards": self.calculate_rewards()
        }
        self.complete_mini_game(result)
```

```python
class ChemicalMixerMiniGame(MiniGame):
    """Chemical mixing puzzle mini-game."""
    
    def __init__(self):
        super().__init__()
        self.name = "Chemical Mixer"
        self.supports_2_player = True  # Co-op mode
        
    def initialize(self, context: SharedContext):
        """Initialize chemical mixer game."""
        super().initialize(context)
        
        self.chemicals = ["H2O", "NaCl", "H2SO4", "NaOH"]
        self.target_compound = self.generate_target()
        
        if context.player_count == 2:
            self.setup_cooperative_mode()
            
    def setup_cooperative_mode(self):
        """Setup 2-player cooperative mode."""
        # Player 1 controls valves
        # Player 2 controls temperature and mixing
        self.p1_role = "valve_operator"
        self.p2_role = "mixer_operator"
```

## Shared Services API

### Sprite Generator Service

```python
class SpriteGeneratorService:
    """Shared sprite generation service."""
    
    def generate_sprite(
        self,
        description: str,
        style: str = "16bit",
        size: Tuple[int, int] = (32, 32),
        animation_frames: int = 1
    ) -> Sprite:
        """
        Generate sprite from description.
        
        Args:
            description: Text description of sprite
            style: Art style ("8bit", "16bit", "cga")
            size: Sprite dimensions
            animation_frames: Number of animation frames
            
        Returns:
            Generated sprite object
            
        Example:
            sprite = sprite_service.generate_sprite(
                "Retro robot with laser eyes",
                style="16bit",
                size=(32, 48),
                animation_frames=4
            )
        """
        pass
        
    def batch_generate(
        self,
        descriptions: List[str],
        **kwargs
    ) -> List[Sprite]:
        """Generate multiple sprites efficiently."""
        pass
```

### Audio Service

```python
class AudioService:
    """Shared audio management service."""
    
    def play_sound(
        self,
        sound_id: str,
        volume: float = 1.0,
        loop: bool = False
    ) -> None:
        """
        Play sound effect.
        
        Args:
            sound_id: Sound identifier
            volume: Volume level (0.0 to 1.0)
            loop: Whether to loop sound
            
        Example:
            audio_service.play_sound("coin_insert", volume=0.8)
        """
        pass
        
    def play_music(
        self,
        music_id: str,
        fade_in: float = 0.0
    ) -> None:
        """Play background music."""
        pass
        
    def stop_all_sounds(self) -> None:
        """Stop all playing sounds."""
        pass
```

### Save Service

```python
class SaveService:
    """Shared save game service."""
    
    def save_game(
        self,
        game_id: str,
        save_data: dict,
        slot: int = 0
    ) -> bool:
        """
        Save game data.
        
        Args:
            game_id: Game identifier
            save_data: Data to save
            slot: Save slot number
            
        Returns:
            True if save successful
            
        Example:
            save_service.save_game(
                "elevator_operator",
                {
                    "floor": 5,
                    "score": 1000,
                    "passengers_served": 50
                },
                slot=0
            )
        """
        pass
        
    def load_game(
        self,
        game_id: str,
        slot: int = 0
    ) -> Optional[dict]:
        """Load game data."""
        pass
        
    def get_save_slots(self, game_id: str) -> List[SaveSlot]:
        """Get available save slots for game."""
        pass
```

## Event System API

### Event Bus

```python
class EventBus:
    """Central event communication system."""
    
    def subscribe(
        self,
        event_type: str,
        handler: Callable,
        game_id: Optional[str] = None
    ) -> None:
        """
        Subscribe to event type.
        
        Args:
            event_type: Type of event to listen for
            handler: Function to call when event occurs
            game_id: Optional game ID for filtering
            
        Example:
            event_bus.subscribe(
                "player_scored",
                self.on_player_scored,
                game_id="elevator_operator"
            )
        """
        pass
        
    def publish(
        self,
        event: GameEvent
    ) -> None:
        """
        Publish event to subscribers.
        
        Args:
            event: Event to publish
            
        Example:
            event_bus.publish(GameEvent(
                type="mini_game_unlocked",
                data={"game_id": "robot_fighter"},
                source="elevator_operator"
            ))
        """
        pass
        
    def unsubscribe(
        self,
        event_type: str,
        handler: Callable
    ) -> None:
        """Unsubscribe from event type."""
        pass
```

### Game Events

```python
class GameEvent:
    """Base class for game events."""
    
    def __init__(
        self,
        type: str,
        data: dict = None,
        source: Optional[str] = None,
        target: Optional[str] = None
    ):
        """
        Create game event.
        
        Args:
            type: Event type identifier
            data: Event data
            source: Source game ID
            target: Target game ID (optional)
        """
        self.type = type
        self.data = data or {}
        self.source = source
        self.target = target
        self.timestamp = time.time()
```

### Common Events

```python
class CommonEvents:
    """Common event types used across games."""
    
    # Player events
    PLAYER_JOINED = "player_joined"
    PLAYER_LEFT = "player_left"
    PLAYER_SCORED = "player_scored"
    
    # Game flow events
    GAME_STARTED = "game_started"
    GAME_PAUSED = "game_paused"
    GAME_RESUMED = "game_resumed"
    GAME_ENDED = "game_ended"
    
    # Mini-game events
    MINI_GAME_REQUESTED = "mini_game_requested"
    MINI_GAME_STARTED = "mini_game_started"
    MINI_GAME_COMPLETED = "mini_game_completed"
    
    # Achievement events
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    PROGRESS_UPDATED = "progress_updated"
    
    # Arcade events
    COIN_INSERTED = "coin_inserted"
    CREDITS_UPDATED = "credits_updated"
```

## Input Handling API

### Input Manager

```python
class InputManager:
    """Centralized input management."""
    
    def __init__(self):
        self.input_handlers = {}
        self.active_players = []
        
    def register_handler(
        self,
        game_id: str,
        handler: Callable
    ) -> None:
        """Register input handler for game."""
        self.input_handlers[game_id] = handler
        
    def process_input(
        self,
        event: pygame.event.Event
    ) -> None:
        """
        Process input event.
        
        Args:
            event: Pygame event to process
        """
        # Determine which player
        player_id = self.get_player_from_event(event)
        
        # Route to active game
        active_game = self.get_active_game()
        if active_game in self.input_handlers:
            self.input_handlers[active_game](event, player_id)
            
    def get_player_from_event(
        self,
        event: pygame.event.Event
    ) -> Optional[int]:
        """Determine which player triggered event."""
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if ArcadeInput.is_player_key(event.key, 0):
                return 0
            elif ArcadeInput.is_player_key(event.key, 1):
                return 1
        return None
```

## Asset Management API

### Resource Pool

```python
class ResourcePool:
    """Shared resource management."""
    
    def __init__(self):
        self.sprites = {}
        self.sounds = {}
        self.fonts = {}
        
    def load_sprite(
        self,
        path: str,
        cache: bool = True
    ) -> pygame.Surface:
        """
        Load sprite from file.
        
        Args:
            path: Path to sprite file
            cache: Whether to cache sprite
            
        Returns:
            Loaded sprite surface
        """
        if path in self.sprites:
            return self.sprites[path]
            
        sprite = pygame.image.load(path)
        if cache:
            self.sprites[path] = sprite
        return sprite
        
    def load_sprite_sheet(
        self,
        path: str,
        frame_size: Tuple[int, int],
        cache: bool = True
    ) -> List[pygame.Surface]:
        """Load sprite sheet and split into frames."""
        pass
        
    def preload_assets(
        self,
        manifest: dict
    ) -> None:
        """
        Preload assets from manifest.
        
        Args:
            manifest: Asset manifest dictionary
            
        Example:
            resource_pool.preload_assets({
                "sprites": ["player.png", "enemy.png"],
                "sounds": ["jump.wav", "coin.wav"],
                "fonts": ["retro.ttf"]
            })
        """
        pass
```

## Examples

### Complete 2-Player Arcade Game

```python
import pygame
from tower_madness import GameModule, SharedContext, ArcadeInput

class TwoPlayerArcadeGame(GameModule):
    """Complete example of 2-player arcade game."""
    
    def __init__(self):
        super().__init__()
        self.name = "Co-op Adventure"
        self.supports_2_player = True
        
    def initialize(self, context: SharedContext):
        """Initialize game."""
        self.context = context
        self.screen = pygame.display.get_surface()
        
        # Setup players
        self.players = []
        for i in range(context.player_count):
            player = self.create_player(i)
            self.players.append(player)
            
        # Setup split-screen if 2 players
        if len(self.players) == 2:
            self.setup_split_screen()
            
    def create_player(self, player_id: int):
        """Create player character."""
        return {
            "id": player_id,
            "x": 100 + player_id * 200,
            "y": 300,
            "score": 0,
            "health": 100,
            "sprite": self.context.sprite_