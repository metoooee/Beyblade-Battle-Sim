from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class BeybladePart:
    name: str
    type: str  # "attack", "defense", "stamina", "balance"
    power_modifier: float  # Multiplier for power
    defense_modifier: float  # Multiplier for defense
    special_effect: str = ""  # Special effect description

class BeybladePartsManager:
    def __init__(self):
        self.energy_rings = self._create_energy_rings()
        self.fusion_wheels = self._create_fusion_wheels()
        self.spin_tracks = self._create_spin_tracks()
        self.performance_tips = self._create_performance_tips()
    
    def _create_energy_rings(self) -> List[BeybladePart]:
        return [
            BeybladePart("Dragon", "attack", 1.2, 0.9, "Increases attack power but reduces defense"),
            BeybladePart("Pegasus", "balance", 1.1, 1.1, "Balanced stats"),
            BeybladePart("Bull", "defense", 0.9, 1.2, "Increases defense but reduces attack"),
            BeybladePart("Lion", "stamina", 1.0, 1.0, "Good stamina and balanced stats"),
            BeybladePart("Phoenix", "attack", 1.3, 0.8, "High attack power but very low defense"),
            BeybladePart("Turtle", "defense", 0.8, 1.3, "High defense but very low attack")
        ]
    
    def _create_fusion_wheels(self) -> List[BeybladePart]:
        return [
            BeybladePart("Destructor", "attack", 1.2, 0.9, "Heavy attack-focused wheel"),
            BeybladePart("Defense", "defense", 0.9, 1.2, "Heavy defense-focused wheel"),
            BeybladePart("Balance", "balance", 1.1, 1.1, "Well-balanced wheel"),
            BeybladePart("Stamina", "stamina", 1.0, 1.0, "Good for long battles"),
            BeybladePart("Assault", "attack", 1.3, 0.8, "Extreme attack power"),
            BeybladePart("Guardian", "defense", 0.8, 1.3, "Extreme defense power")
        ]
    
    def _create_spin_tracks(self) -> List[BeybladePart]:
        return [
            BeybladePart("Short", "attack", 1.1, 0.95, "Better for attack types"),
            BeybladePart("Medium", "balance", 1.0, 1.0, "Balanced performance"),
            BeybladePart("Long", "defense", 0.95, 1.1, "Better for defense types"),
            BeybladePart("Extra Long", "stamina", 0.9, 1.15, "Best for stamina types")
        ]
    
    def _create_performance_tips(self) -> List[BeybladePart]:
        return [
            BeybladePart("Sharp", "attack", 1.1, 0.95, "Increases attack power"),
            BeybladePart("Flat", "defense", 0.95, 1.1, "Increases defense"),
            BeybladePart("Round", "balance", 1.0, 1.0, "Balanced performance"),
            BeybladePart("Rubber", "stamina", 0.9, 1.15, "Best for stamina")
        ]
    
    def create_custom_beyblade(self, name: str, energy_ring: BeybladePart, fusion_wheel: BeybladePart, 
                             spin_track: BeybladePart, performance_tip: BeybladePart) -> dict:
        """Create a custom beyblade with the selected parts"""
        # Calculate final power and defense based on part modifiers
        final_power = int(75 * (energy_ring.power_modifier + fusion_wheel.power_modifier + 
                               spin_track.power_modifier + performance_tip.power_modifier) / 4)
        final_defense = int(75 * (energy_ring.defense_modifier + fusion_wheel.defense_modifier + 
                                 spin_track.defense_modifier + performance_tip.defense_modifier) / 4)
        
        # Determine beyblade type based on parts
        type_counts = {
            "attack": 0,
            "defense": 0,
            "balance": 0,
            "stamina": 0
        }
        
        for part in [energy_ring, fusion_wheel, spin_track, performance_tip]:
            if part.type in type_counts:
                type_counts[part.type] += 1
        
        # Determine final type
        max_type = max(type_counts.items(), key=lambda x: x[1])
        if max_type[1] > 0:
            final_type = max_type[0].capitalize()
        else:
            final_type = "Balance"
        
        # Create custom special moves based on parts and their types
        custom_moves = {
            "attack_moves": [
                {
                    "name": f"{energy_ring.name} {fusion_wheel.name} Assault",
                    "power": 85 if energy_ring.type == "attack" or fusion_wheel.type == "attack" else 75,
                    "move_type": "attack"
                },
                {
                    "name": f"{spin_track.name} {performance_tip.name} Strike",
                    "power": 80 if spin_track.type == "attack" or performance_tip.type == "attack" else 70,
                    "move_type": "attack"
                }
            ],
            "defense_moves": [
                {
                    "name": f"{energy_ring.name} {fusion_wheel.name} Shield",
                    "power": 70 if energy_ring.type == "defense" or fusion_wheel.type == "defense" else 60,
                    "move_type": "defense"
                }
            ],
            "critical_moves": [
                {
                    "name": f"{energy_ring.name} {fusion_wheel.name} {spin_track.name} Ultimate",
                    "power": 100 if (energy_ring.type == "attack" and fusion_wheel.type == "attack") or 
                                   (fusion_wheel.type == "attack" and spin_track.type == "attack") or
                                   (energy_ring.type == "attack" and spin_track.type == "attack") else 90,
                    "move_type": "critical"
                }
            ]
        }
        
        # Add special effects based on part combinations
        if energy_ring.type == "attack" and fusion_wheel.type == "attack":
            custom_moves["attack_moves"][0]["power"] += 10
            custom_moves["attack_moves"][0]["name"] += " (Double Attack)"
        
        if spin_track.type == "defense" and performance_tip.type == "defense":
            custom_moves["defense_moves"][0]["power"] += 10
            custom_moves["defense_moves"][0]["name"] += " (Double Defense)"
        
        if energy_ring.type == "stamina" and performance_tip.type == "stamina":
            custom_moves["critical_moves"][0]["power"] += 5
            custom_moves["critical_moves"][0]["name"] += " (Stamina Boost)"
        
        return {
            "name": name,
            "type": final_type,
            "power": final_power,
            "defense": final_defense,
            "special_moves": custom_moves
        }
    
    def get_available_parts(self) -> Dict[str, List[str]]:
        """Get lists of available parts"""
        return {
            "energy_rings": [p.name for p in self.energy_rings],
            "fusion_wheels": [p.name for p in self.fusion_wheels],
            "spin_tracks": [p.name for p in self.spin_tracks],
            "performance_tips": [p.name for p in self.performance_tips]
        } 