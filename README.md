# Beyblade-Battle-Sim
Project: Beyblade Battle Simulator
Overview
Beyblade Battle Simulator is a Python-based, terminal game that simulates Beyblade battles between players or against the computer. Players can choose from starter Beyblades or create custom ones by selecting parts, each with unique effects. The game features special moves, environmental effects, a commentator, and a save/load system.

System Design
Main Components
main.py: Entry point, game loop, user interface, and orchestration.
beyblade.py: Defines Beyblade classes, stats, and special move logic.
player.py: Manages player registration, login, and stats.
beyblade_parts.py: Handles custom Beyblade part selection and effects.
environment.py: Manages random environmental events affecting battles.
utils.py: Utility functions (e.g., loading JSON data).
music_manager.py: Handles background music (optional/bonus).
data/: Stores moves, player data, and save files in JSON format.
Game Flow
Startup: Loads music, checks for saved games.
Player Management: Login or register.
Beyblade Selection: Choose starter, create, or load custom Beyblade.
Opponent Selection: Play against computer or another player.
Battle Loop: Players select moves; system applies effects, checks for environmental events, and updates stats.
Save/Load: Players can save and resume games.
Victory/Defeat: Updates player stats and ends the game.
Techniques Used
Object-Oriented Programming: Classes for Beyblades, Players, Moves, Parts, and Environment.
JSON Serialization: For saving/loading game state and player data.
Randomization: For move selection (AI), environmental events, and commentator phrases.
Terminal UI: Uses colorama for colored output and clear prompts.
Modular Design: Each feature is separated into its own module for maintainability.
Error Handling: Input validation and exception handling for robust gameplay.
Extensibility: Easy to add new Beyblades, moves, or parts by updating JSON files or classes.
Notable Features
Custom Beyblade Creation: Players can mix and match parts, each affecting stats and generating unique moves.
Special Moves: Attack, defense, and critical moves, each with unique effects and usage limits.
Environmental Effects: Random events can alter battle dynamics.
Commentator: Adds dynamic, randomized commentary for immersion.
Save/Load System: Allows players to pause and resume battles.
Conclusion
The Beyblade Battle Simulator demonstrates a modular, extensible approach to turn-based game design in Python, combining OOP, file I/O, and user interaction for an engaging terminal experience.
