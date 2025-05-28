from typing import List, Dict, Optional
import uuid
from datetime import datetime
import random
from beyblade import Beyblade, SpecialMove
from utils import BattleError, save_battle_log

class BeyBattle:
    def __init__(self, beyblade1: Beyblade, beyblade2: Beyblade):
        self.beyblade1 = beyblade1
        self.beyblade2 = beyblade2
        self.current_turn = 1
        self.battle_id = str(uuid.uuid4())
        self.battle_log: List[Dict] = []
        self.winner: Optional[Beyblade] = None

    def is_battle_over(self) -> bool:
        """Check if the battle is over"""
        return self.beyblade1.is_knocked_out() or self.beyblade2.is_knocked_out()

    def get_winner(self) -> Optional[Beyblade]:
        """Get the winner of the battle"""
        if self.beyblade1.is_knocked_out():
            return self.beyblade2
        elif self.beyblade2.is_knocked_out():
            return self.beyblade1
        return None

    def check_stadium_out(self) -> None:
        """Random chance for stadium out based on remaining stamina"""
        for beyblade in [self.beyblade1, self.beyblade2]:
            if not beyblade.is_stadium_out:
                stamina_percentage = beyblade.current_stamina / beyblade.max_stamina
                stadium_out_chance = 0.05 * (1 - stamina_percentage)  # Higher chance when low on stamina
                if random.random() < stadium_out_chance:
                    beyblade.is_stadium_out = True
                    beyblade.current_stamina = 0

    def execute_turn(self, move1: SpecialMove, move2: SpecialMove) -> Dict[str, any]:
        """Execute a single turn of battle"""
        if self.is_battle_over():
            raise BattleError("Battle is already over!")

        # Determine order based on spin speed
        first = self.beyblade1 if self.beyblade1.spin_speed >= self.beyblade2.spin_speed else self.beyblade2
        second = self.beyblade2 if first == self.beyblade1 else self.beyblade1
        first_move = move1 if first == self.beyblade1 else move2
        second_move = move2 if second == self.beyblade2 else move1

        # Execute moves
        turn_log = {
            'turn': self.current_turn,
            'timestamp': datetime.now().isoformat(),
            'actions': []
        }

        # First Beyblade's move
        if not first.is_knocked_out():
            try:
                result = first.use_special_move(first_move, second)
                turn_log['actions'].append(result)
            except BattleError as e:
                turn_log['actions'].append({
                    'error': str(e),
                    'beyblade': first.name
                })

        # Check for stadium out
        self.check_stadium_out()

        # Second Beyblade's move
        if not second.is_knocked_out():
            try:
                result = second.use_special_move(second_move, first)
                turn_log['actions'].append(result)
            except BattleError as e:
                turn_log['actions'].append({
                    'error': str(e),
                    'beyblade': second.name
                })

        # Check for stadium out again
        self.check_stadium_out()

        # Update battle state
        self.battle_log.append(turn_log)
        self.current_turn += 1

        # Check for battle end
        if self.is_battle_over():
            self.winner = self.get_winner()
            self.save_battle()

        return turn_log

    def save_battle(self) -> None:
        """Save the battle log to a file"""
        battle_data = {
            'battle_id': self.battle_id,
            'beyblade1': self.beyblade1.name,
            'beyblade2': self.beyblade2.name,
            'winner': self.winner.name if self.winner else None,
            'total_turns': self.current_turn - 1,
            'log': self.battle_log
        }
        save_battle_log(self.battle_id, battle_data)

    def get_battle_status(self) -> str:
        """Get a string representation of the current battle status"""
        status = f"\nTurn {self.current_turn}\n"
        status += f"{self.beyblade1}\n"
        status += f"{self.beyblade2}\n"
        
        if self.beyblade1.is_stadium_out:
            status += f"\n{self.beyblade1.name} was knocked out of the stadium!"
        if self.beyblade2.is_stadium_out:
            status += f"\n{self.beyblade2.name} was knocked out of the stadium!"
            
        if self.winner:
            status += f"\nBattle Over! Winner: {self.winner.name}"
        return status 