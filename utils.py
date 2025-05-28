from typing import Dict, Any
import json
from datetime import datetime
import os
import random

class BeybladeError(Exception):
    """Base exception for Beyblade-related errors"""
    pass

class BattleError(Exception):
    """Base exception for Battle-related errors"""
    pass

class SpecialMoveError(Exception):
    """Exception raised for errors in the SpecialMove class."""
    pass

def calculate_damage(attacker_power, move_power, defender_defense, type_advantage=1.0, critical=False, defending=False):
    """Calculate damage from an attack"""
    base_damage = (attacker_power * move_power) / (defender_defense * 10)
    
    # Apply type advantage
    base_damage *= type_advantage
    
    # Apply critical hit bonus
    if critical:
        base_damage *= 2
    
    # Apply defense reduction if defender is using defense
    if defending:
        base_damage *= 0.7  # Reduce damage by 30%
    
    return max(1, int(base_damage))  # Minimum damage is 1

def calculate_stamina_loss(power, move_type="attack"):
    """Calculate stamina loss based on the move"""
    if move_type == "critical":
        return power * 2
    elif move_type == "defense":
        return power * 0.5
    else:  # Regular attack
        return power

def load_json_data(file_path):
    """Load data from a JSON file"""
    try:
        if not os.path.exists(file_path):
            # Check in data directory
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
            alt_path = os.path.join(data_dir, os.path.basename(file_path))
            if os.path.exists(alt_path):
                file_path = alt_path
            else:
                raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in file: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading JSON data: {str(e)}")

def save_battle_log(battle_id: str, log_data: Dict[str, Any]) -> None:
    """Save battle log to a JSON file"""
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"logs/battle_{battle_id}_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)
    except IOError:
        raise BattleError(f"Failed to save battle log to {filename}")

# Type advantages (based on Beyblade types)
TYPE_ADVANTAGES = {
    'Attack': {'Defense': 1.5, 'Balance': 1.2},
    'Defense': {'Power': 1.5, 'Attack': 0.8},
    'Balance': {'Power': 1.2, 'Defense': 1.2},
    'Power': {'Attack': 1.5, 'Balance': 0.8}
} 