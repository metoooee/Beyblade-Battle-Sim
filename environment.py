from dataclasses import dataclass
from typing import Dict, List, Optional
import random

@dataclass
class EnvironmentalEvent:
    name: str
    description: str
    effect_type: str  # "power", "defense", "speed", "stamina"
    effect_value: float  # Multiplier for the effect
    duration: int  # Number of turns the effect lasts
    probability: float  # Probability of this event occurring (0-1)

class EnvironmentManager:
    def __init__(self):
        self.current_event: Optional[EnvironmentalEvent] = None
        self.event_duration: int = 0
        self.events = self._create_events()
    
    def _create_events(self) -> List[EnvironmentalEvent]:
        return [
            EnvironmentalEvent(
                "Strong Wind",
                "A strong wind has picked up, increasing attack power but reducing defense!",
                "power",
                1.3,
                2,
                0.2
            ),
            EnvironmentalEvent(
                "Heavy Rain",
                "Heavy rain has started, making the stadium slippery and reducing speed!",
                "speed",
                0.7,
                2,
                0.15
            ),
            EnvironmentalEvent(
                "Sandstorm",
                "A sandstorm has formed, reducing visibility and defense!",
                "defense",
                0.8,
                2,
                0.15
            ),
            EnvironmentalEvent(
                "Heat Wave",
                "A heat wave has hit, increasing stamina consumption!",
                "stamina",
                0.8,
                2,
                0.15
            ),
            EnvironmentalEvent(
                "Magnetic Field",
                "A magnetic field has formed, increasing defense but reducing speed!",
                "defense",
                1.2,
                2,
                0.1
            ),
            EnvironmentalEvent(
                "Energy Surge",
                "An energy surge has occurred, increasing power temporarily!",
                "power",
                1.4,
                1,
                0.1
            ),
            EnvironmentalEvent(
                "Ice Formation",
                "Ice has formed on the stadium, increasing speed but reducing control!",
                "speed",
                1.3,
                2,
                0.15
            )
        ]
    
    def check_for_event(self) -> Optional[EnvironmentalEvent]:
        """Check if a new environmental event should occur"""
        if self.current_event is not None:
            self.event_duration -= 1
            if self.event_duration <= 0:
                self.current_event = None
                return None
        
        # Only allow new events if there isn't a current one
        if self.current_event is None:
            for event in self.events:
                if random.random() < event.probability:
                    self.current_event = event
                    self.event_duration = event.duration
                    return event
        
        return self.current_event
    
    def apply_event_effects(self, power: int, defense: int, speed: int, stamina: int) -> Dict[str, int]:
        """Apply current environmental event effects to stats"""
        if self.current_event is None:
            return {
                "power": power,
                "defense": defense,
                "speed": speed,
                "stamina": stamina
            }
        
        modified_stats = {
            "power": power,
            "defense": defense,
            "speed": speed,
            "stamina": stamina
        }
        
        if self.current_event.effect_type in modified_stats:
            modified_stats[self.current_event.effect_type] = int(
                modified_stats[self.current_event.effect_type] * self.current_event.effect_value
            )
        
        return modified_stats
    
    def get_current_event_status(self) -> Optional[str]:
        """Get description of current environmental event"""
        if self.current_event is None:
            return None
        
        return f"{self.current_event.description} (Duration: {self.event_duration} turns)" 