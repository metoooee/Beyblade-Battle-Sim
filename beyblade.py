from dataclasses import dataclass
from typing import List, Dict
from utils import TYPE_ADVANTAGES, SpecialMoveError, calculate_damage, calculate_stamina_loss
import random

@dataclass
class SpecialMove:
    name: str
    power: int
    move_type: str  # "attack", "defense" veya "critical"
    
    def __str__(self) -> str:
        move_type_str = "🔥 Critical" if self.move_type == "critical" else self.move_type.title()
        return f"{self.name} ({move_type_str}, Power: {self.power})"

class Beyblade:
    def __init__(self, name: str, type: str, power: int, defense: int, special_moves: List[SpecialMove]):
        self.name = name
        self.type = type
        self.power = power
        self.defense = defense
        self.health = 100
        self.stamina = 100  # New stamina attribute
        self.spin_speed = 100  # New spin speed attribute
        self.special_moves = special_moves
        self.defense_count = 2
        self.critical_used = False
        self.available_moves = []
    
    def start_turn(self):
        """Reset turn-specific attributes"""
        self.defense_active = False
        # Reduce stamina and spin speed each turn
        self.stamina = max(0, self.stamina - 5)
        self.spin_speed = max(0, self.spin_speed - 3)
        # If stamina is low, reduce spin speed more
        if self.stamina < 30:
            self.spin_speed = max(0, self.spin_speed - 5)
    
    def use_special_move(self, move: SpecialMove, opponent: 'Beyblade') -> dict:
        """Use a special move and return the result"""
        if move.move_type == "defense":
            if self.defense_count <= 0:
                return {'error': 'no_defense_moves_left'}
            self.defense_count -= 1
            self.defense_active = True
            return {'defense_remaining': self.defense_count}
        
        if move.move_type == "critical":
            if self.critical_used:
                return {'error': 'critical_already_used'}
            self.critical_used = True
            # Critical moves have higher base damage
            base_damage = int((self.power * move.power) / 150)  # Less reduction for critical moves
            spin_multiplier = (self.spin_speed / 100) * 0.9  # Higher spin multiplier for critical
            final_damage = int(base_damage * spin_multiplier)
            is_critical = True
        else:
            # Normal attack calculation
            base_damage = int((self.power * move.power) / 200)
            spin_multiplier = (self.spin_speed / 100) * 0.7
            final_damage = int(base_damage * spin_multiplier)
            is_critical = False
        
        # Apply type advantage
        if self.type == "attack" and opponent.type == "defense":
            final_damage = int(final_damage * 1.1)
        elif self.type == "defense" and opponent.type == "stamina":
            final_damage = int(final_damage * 1.1)
        elif self.type == "stamina" and opponent.type == "attack":
            final_damage = int(final_damage * 1.1)
        
        # Additional critical hit chance for non-critical moves
        if not is_critical and self.spin_speed > 70 and random.random() < 0.3:
            final_damage = int(final_damage * 1.2)
            is_critical = True
        
        # Ensure minimum damage of 1 and maximum damage of 30 for normal attacks
        # Critical moves can exceed 30 damage
        if not is_critical:
            final_damage = max(1, min(30, final_damage))
        else:
            final_damage = max(1, final_damage)
        
        return {
            'damage': final_damage,
            'critical': is_critical
        }
    
    def is_defeated(self) -> bool:
        """Check if the Beyblade is defeated"""
        return self.health <= 0 or self.spin_speed <= 0
    
    def __str__(self) -> str:
        """String representation of the Beyblade"""
        critical_status = "🔥 Available" if not self.critical_used else "❌ Used"
        defense_status = f"🛡️ {self.defense_count} remaining" if self.defense_count > 0 else "❌ None"
        return f"{self.name} ({self.type}) - Health: {self.health}, Stamina: {self.stamina}, Spin Speed: {self.spin_speed}\n" \
               f"Critical Move: {critical_status}, Defense Moves: {defense_status}"

# Specific Beyblades
class DragonFury(Beyblade):
    def __init__(self, special_moves: list[SpecialMove]):
        # Select attack, defense, and critical moves
        dragon_moves = [
            move for move in special_moves 
            if move.name in ["Dragon Emperor Soaring Bite Strike", "Dragon Emperor Shield", "Dragon Emperor Supreme Flight"]
        ]
        super().__init__(
            name="L-Drago Destructor",
            type="Attack",
            power=90,
            defense=50,
            special_moves=dragon_moves
        )

class StormPegasus(Beyblade):
    def __init__(self, special_moves: list[SpecialMove]):
        # Select attack, defense, and critical moves
        pegasus_moves = [
            move for move in special_moves 
            if move.name in ["Pegasus Starblast Attack", "Pegasus Shield", "Pegasus Stardust Driver"]
        ]
        super().__init__(
            name="Storm Pegasus",
            type="Balance",
            power=75,
            defense=75,
            special_moves=pegasus_moves
        )

class RockLion(Beyblade):
    def __init__(self, special_moves: list[SpecialMove]):
        # Select attack, defense, and critical moves
        lion_moves = [
            move for move in special_moves 
            if move.name in ["Lion Wild Wind Fang Dance", "Lion Shield", "Lion Reverse Wind Strike"]
        ]
        super().__init__(
            name="Rock Leone",
            type="Defense",
            power=50,
            defense=90,
            special_moves=lion_moves
        )

class DarkBull(Beyblade):
    def __init__(self, special_moves: list[SpecialMove]):
        # Select attack, defense, and critical moves
        bull_moves = [
            move for move in special_moves 
            if move.name in ["Bull Upper Attack", "Bull Defense Wall", "Bull Destruction"]
        ]
        super().__init__(
            name="Dark Bull",
            type="Power",
            power=80,
            defense=60,
            special_moves=bull_moves
        )

class Draciel(Beyblade):
    def __init__(self, special_moves: list[SpecialMove]):
        # Select attack, defense, and critical moves
        draciel_moves = [
            move for move in special_moves 
            if move.name in ["Turtle Shell Attack", "Turtle Shell Defense", "Turtle Shell Counter"]
        ]
        super().__init__(
            name="Draciel",
            type="Defense",
            power=60,
            defense=90,
            special_moves=draciel_moves
        )

class Dragoon(Beyblade):
    def __init__(self, special_moves: list[SpecialMove]):
        # Select attack, defense, and critical moves
        dragoon_moves = [
            move for move in special_moves 
            if move.name in ["Dragon Emperor Strike", "Dragon Emperor Shield", "Dragon Emperor Critical"]
        ]
        super().__init__(
            name="Dragoon",
            type="Balance",
            power=75,
            defense=75,
            special_moves=dragoon_moves
        )

class Dranzer(Beyblade):
    def __init__(self, special_moves: list[SpecialMove]):
        # Select attack, defense, and critical moves
        dranzer_moves = [
            move for move in special_moves 
            if move.name in ["Phoenix Wing Attack", "Phoenix Wing Shield", "Phoenix Wing Critical"]
        ]
        super().__init__(
            name="Dranzer",
            type="Attack",
            power=90,
            defense=60,
            special_moves=dranzer_moves
        )

class Driger(Beyblade):
    def __init__(self, special_moves: list[SpecialMove]):
        # Select attack, defense, and critical moves
        driger_moves = [
            move for move in special_moves 
            if move.name in ["Tiger Claw Attack", "Tiger Claw Shield", "Tiger Claw Critical"]
        ]
        super().__init__(
            name="Driger",
            type="Attack",
            power=85,
            defense=65,
            special_moves=driger_moves
        )

