import json
import os
from dataclasses import dataclass, asdict
from typing import Optional, Dict, List

@dataclass
class Player:
    name: str
    wins: int = 0
    losses: int = 0
    custom_beyblades: List[Dict] = None
    
    def __post_init__(self):
        if self.custom_beyblades is None:
            self.custom_beyblades = []
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Player':
        return cls(**data)

class PlayerManager:
    def __init__(self, save_file: str = "data/players.json"):
        self.save_file = save_file
        self.players: Dict[str, Player] = {}
        self._load_players()
    
    def _load_players(self):
        """Load players from save file"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.players = {
                        name: Player.from_dict(player_data)
                        for name, player_data in data.items()
                    }
            except Exception as e:
                print(f"Error loading players: {e}")
                self.players = {}
    
    def save_players(self):
        """Save players to file"""
        os.makedirs(os.path.dirname(self.save_file), exist_ok=True)
        with open(self.save_file, 'w') as f:
            json.dump(
                {name: player.to_dict() for name, player in self.players.items()},
                f,
                indent=2
            )
    
    def get_player(self, name: str) -> Optional[Player]:
        """Get player by name"""
        return self.players.get(name)
    
    def create_player(self, name: str) -> Player:
        """Create a new player"""
        if name in self.players:
            raise ValueError(f"Player {name} already exists")
        
        player = Player(name=name)
        self.players[name] = player
        self.save_players()
        return player
    
    def update_player(self, player: Player):
        """Update player data"""
        self.players[player.name] = player
        self.save_players()
    
    def add_custom_beyblade(self, player_name: str, beyblade_data: dict):
        """Add a custom beyblade to player's collection"""
        player = self.get_player(player_name)
        if not player:
            raise ValueError(f"Player {player_name} not found")
        
        player.custom_beyblades.append(beyblade_data)
        self.update_player(player)
    
    def get_custom_beyblades(self, player_name: str) -> List[Dict]:
        """Get player's custom beyblades"""
        player = self.get_player(player_name)
        if not player:
            return []
        return player.custom_beyblades 