from beyblade import DragonFury, StormPegasus, RockLion, DarkBull, SpecialMove, Beyblade, Draciel, Dragoon, Dranzer, Driger
from utils import load_json_data
from player import PlayerManager, Player
from beyblade_parts import BeybladePartsManager
from environment import EnvironmentManager
import os
from colorama import init, Fore, Style
import random
import json
from music_manager import MusicManager

# Initialize colorama for Windows
init()

music_manager = MusicManager()
music_manager.play_background_music()

def load_moves() -> dict:
    """Load moves from JSON file"""
    return load_json_data(os.path.join('data', 'moves.json'))

def create_move_from_data(move_data: dict) -> SpecialMove:
    """Create a SpecialMove object from move data"""
    return SpecialMove(
        name=move_data['name'],
        power=move_data['power'],
        move_type=move_data['move_type']
    )

def create_starter_beyblades() -> list:
    """Create starter Beyblades with their special moves"""
    moves_data = load_moves()
    
    # Load all moves
    all_moves = []
    for move_type in ['attack_moves', 'defense_moves', 'critical_moves']:
        for move in moves_data[move_type]:
            all_moves.append(create_move_from_data(move))
    
    # Create Beyblades with boosted stats for computer opponents
    dragon = DragonFury(special_moves=all_moves)
    pegasus = StormPegasus(special_moves=all_moves)
    lion = RockLion(special_moves=all_moves)
    bull = DarkBull(special_moves=all_moves)
    draciel = Draciel(special_moves=all_moves)
    dragoon = Dragoon(special_moves=all_moves)
    dranzer = Dranzer(special_moves=all_moves)
    driger = Driger(special_moves=all_moves)
    
    # Boost stats for computer opponents
    for beyblade in [dragon, pegasus, lion, bull, draciel, dragoon, dranzer, driger]:
        beyblade.power = int(beyblade.power * 1.2)
        beyblade.defense = int(beyblade.defense * 1.2)
    
    return [dragon, pegasus, lion, bull, draciel, dragoon, dranzer, driger]

def print_beyblade_list(beyblade_list: list) -> None:
    """Print available Beyblades"""
    print(f"\n{Fore.CYAN}Available Beyblades:{Style.RESET_ALL}")
    for i, beyblade in enumerate(beyblade_list, 1):
        print(f"{i}. {beyblade}")

def print_moves_list(beyblade) -> None:
    """Print available special moves for a Beyblade"""
    print(f"\n{Fore.YELLOW}Special moves for {beyblade.name}:{Style.RESET_ALL}")
    
    # Önce özel hareketleri filtreleme işlemi
    # Eğer kaydedilen oyunda tüm hareketlerle yüklenmişse, tekrar filtreleme yapalım
    if len(beyblade.special_moves) > 6:  # Bir beyblade'in normalde en fazla 3-4 hareketi olmalı
        # Önce beyblade'in ismine bakalım - rakam veya 1-2 karakter ise custom beyblade olabilir
        if len(beyblade.name) <= 2 or beyblade.name.isdigit():
            # Custom beyblade için özel hareketleri elle tanımlayalım 
            # (Normalde veritabanından alınmalı ama şimdilik sabit değerler kullanıyoruz)
            custom_moves = []
            custom_moves.append(SpecialMove(f"Dragon Destructor Assault (Double Attack)", 95, "attack"))
            custom_moves.append(SpecialMove(f"Short Sharp Strike", 80, "attack"))
            custom_moves.append(SpecialMove(f"Dragon Destructor Shield", 60, "defense"))
            
            # Critical move durumunu kontrol et
            if not beyblade.critical_used:
                custom_moves.append(SpecialMove(f"Dragon Destructor Short Ultimate", 100, "critical"))
            
            # Özel hareketleri güncelle
            beyblade.special_moves = custom_moves
        else:
            # Starter beyblade - tüm hareketleri yükle ve filtrele
            moves_data = load_moves()
            all_moves = []
            for move_type in ['attack_moves', 'defense_moves', 'critical_moves']:
                for move in moves_data[move_type]:
                    all_moves.append(create_move_from_data(move))
            
            # Bu beyblade için özel hareketleri filtreleme
            filtered_moves = get_starter_beyblade_moves(beyblade.name, all_moves)
            
            # Eğer filtreleme başarılıysa (en az bir hareket bulunmuşsa), özel hareketleri güncelleme
            if filtered_moves:
                beyblade.special_moves = filtered_moves
    
    # Initialize available moves list
    available_moves = []
    
    # Normal attack moves
    print(f"{Fore.RED}Attack Moves:{Style.RESET_ALL}")
    attack_moves = [move for move in beyblade.special_moves if move.move_type == "attack"]
    for i, move in enumerate(attack_moves, 1):
        print(f"{i}. {move}")
    available_moves.extend(attack_moves)
    
    # Defense moves (if any left)
    if beyblade.defense_count > 0:
        print(f"\n{Fore.BLUE}Defense Moves:{Style.RESET_ALL}")
        defense_moves = [move for move in beyblade.special_moves if move.move_type == "defense"]
        for i, move in enumerate(defense_moves, 1):
            print(f"{len(available_moves) + i}. {move}")
        available_moves.extend(defense_moves)
    
    # Critical moves (only if not used)
    if not beyblade.critical_used:
        print(f"\n{Fore.MAGENTA}Critical Moves:{Style.RESET_ALL}")
        critical_moves = [move for move in beyblade.special_moves if move.move_type == "critical"]
        for i, move in enumerate(critical_moves, 1):
            print(f"{len(available_moves) + i}. {move}")
        available_moves.extend(critical_moves)
    
    # Add save/exit options
    print(f"\n{Fore.YELLOW}=== Options ==={Style.RESET_ALL}")
    print(f"{len(available_moves) + 1}. Save Game")
    print(f"{len(available_moves) + 2}. Exit Game")
    
    # Store available moves in the beyblade object
    beyblade.available_moves = available_moves
    
    # If no moves are available, add a default attack move
    if not available_moves:
        default_move = SpecialMove("Basic Attack", 50, "attack")
        beyblade.available_moves = [default_move]
        print(f"\n{Fore.RED}No special moves available! Using basic attack.{Style.RESET_ALL}")
        print(f"1. {default_move}")

def get_user_choice(prompt: str, max_choice: int) -> int:
    """Get user input with validation"""
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= max_choice:
                return choice
            print(f"Please enter a number between 1 and {max_choice}")
        except ValueError:
            print("Please enter a valid number")

def create_custom_beyblade(parts_manager: BeybladePartsManager) -> Beyblade:
    """Create a custom beyblade through user input"""
    print(f"\n{Fore.GREEN}Let's create your custom Beyblade!{Style.RESET_ALL}")
    
    # Get beyblade name
    name = input("\nEnter a name for your Beyblade: ")
    
    # Select parts with characteristics
    print(f"\n{Fore.CYAN}Select Energy Ring:{Style.RESET_ALL}")
    for i, ring in enumerate(parts_manager.energy_rings, 1):
        print(f"{i}. {ring.name} - Type: {ring.type}, Power: {ring.power_modifier:.1f}x, Defense: {ring.defense_modifier:.1f}x")
        print(f"   Effect: {ring.special_effect}")
    er_choice = get_user_choice("Enter your choice: ", len(parts_manager.energy_rings))
    selected_energy_ring = parts_manager.energy_rings[er_choice - 1]
    
    print(f"\n{Fore.CYAN}Select Fusion Wheel:{Style.RESET_ALL}")
    for i, wheel in enumerate(parts_manager.fusion_wheels, 1):
        print(f"{i}. {wheel.name} - Type: {wheel.type}, Power: {wheel.power_modifier:.1f}x, Defense: {wheel.defense_modifier:.1f}x")
        print(f"   Effect: {wheel.special_effect}")
    fw_choice = get_user_choice("Enter your choice: ", len(parts_manager.fusion_wheels))
    selected_fusion_wheel = parts_manager.fusion_wheels[fw_choice - 1]
    
    print(f"\n{Fore.CYAN}Select Spin Track:{Style.RESET_ALL}")
    for i, track in enumerate(parts_manager.spin_tracks, 1):
        print(f"{i}. {track.name} - Type: {track.type}, Power: {track.power_modifier:.1f}x, Defense: {track.defense_modifier:.1f}x")
        print(f"   Effect: {track.special_effect}")
    st_choice = get_user_choice("Enter your choice: ", len(parts_manager.spin_tracks))
    selected_spin_track = parts_manager.spin_tracks[st_choice - 1]
    
    print(f"\n{Fore.CYAN}Select Performance Tip:{Style.RESET_ALL}")
    for i, tip in enumerate(parts_manager.performance_tips, 1):
        print(f"{i}. {tip.name} - Type: {tip.type}, Power: {tip.power_modifier:.1f}x, Defense: {tip.defense_modifier:.1f}x")
        print(f"   Effect: {tip.special_effect}")
    pt_choice = get_user_choice("Enter your choice: ", len(parts_manager.performance_tips))
    selected_performance_tip = parts_manager.performance_tips[pt_choice - 1]
    
    # Create the custom beyblade
    beyblade_data = parts_manager.create_custom_beyblade(
        name=name,
        energy_ring=selected_energy_ring,
        fusion_wheel=selected_fusion_wheel,
        spin_track=selected_spin_track,
        performance_tip=selected_performance_tip
    )
    
    # Create special moves from custom moves generated based on parts
    special_moves = []
    for move_type in ['attack_moves', 'defense_moves', 'critical_moves']:
        for move in beyblade_data["special_moves"][move_type]:
            special_moves.append(SpecialMove(
                name=move["name"],
                power=move["power"],
                move_type=move["move_type"]
            ))
    
    # Print the custom special moves
    print(f"\n{Fore.YELLOW}Your custom Beyblade has the following special moves:{Style.RESET_ALL}")
    print(f"{Fore.RED}Attack Moves:{Style.RESET_ALL}")
    for move in special_moves:
        if move.move_type == "attack":
            print(f"- {move.name} (Power: {move.power})")
    
    print(f"\n{Fore.BLUE}Defense Moves:{Style.RESET_ALL}")
    for move in special_moves:
        if move.move_type == "defense":
            print(f"- {move.name} (Power: {move.power})")
    
    print(f"\n{Fore.MAGENTA}Critical Moves:{Style.RESET_ALL}")
    for move in special_moves:
        if move.move_type == "critical":
            print(f"- {move.name} (Power: {move.power})")
    
    return Beyblade(
        name=beyblade_data["name"],
        type=beyblade_data["type"],
        power=beyblade_data["power"],
        defense=beyblade_data["defense"],
        special_moves=special_moves
    )

class Commentator:
    def __init__(self):
        self.phrases = {
            "battle_start": [
                "🎙️ The battle is about to begin! Let's see who will emerge victorious!",
                "🎙️ Get ready for an epic Beyblade battle! The stadium is set!",
                "🎙️ The stadium is set, the Beyblades are ready. Let's begin!",
                "🎙️ This is going to be an intense match! Let's get started!"
            ],
            "critical_hit": [
                "🎙️ INCREDIBLE! A critical hit! That was absolutely devastating!",
                "🎙️ WOW! That was a perfect critical strike! The crowd is going wild!",
                "🎙️ AMAZING! A critical hit at the perfect moment!",
                "🎙️ SPECTACULAR! That critical hit was absolutely perfect! The opponent is reeling!"
            ],
            "defense": [
                "🎙️ A solid defense move! They're playing it safe!",
                "🎙️ Excellent defensive strategy! They're biding their time!",
                "🎙️ That defense might just save them! Smart play!",
                "🎙️ A well-timed defensive maneuver! They're not going down easily!"
            ],
            "low_health": [
                "🎙️ They're on their last legs! Can they make a comeback?",
                "🎙️ This could be the end! They're barely hanging on!",
                "🎙️ They're struggling to maintain their spin! One more hit might finish them!",
                "🎙️ The Beyblade is wobbling! They need to make their move now!"
            ],
            "low_stamina": [
                "🎙️ Their stamina is running low! They need to finish this quickly!",
                "🎙️ The Beyblade is losing momentum! They're running out of steam!",
                "🎙️ They're struggling to maintain their spin speed!",
                "🎙️ The Beyblade is slowing down! They need to act fast!"
            ],
            "environmental": [
                "🎙️ The environment is affecting the battle! This could change everything!",
                "🎙️ The stadium conditions are becoming a major factor!",
                "🎙️ The environmental effects are taking their toll!",
                "🎙️ The battle conditions are getting intense! How will they adapt?"
            ],
            "victory": [
                "🎙️ AND THE WINNER IS...",
                "🎙️ VICTORY HAS BEEN DECIDED!",
                "🎙️ THE BATTLE IS OVER!",
                "🎙️ WE HAVE A CHAMPION!"
            ],
            "turn_start": [
                "🎙️ The Beyblades are spinning at full power!",
                "🎙️ Both competitors are ready for the next round!",
                "🎙️ The battle continues with intense momentum!",
                "🎙️ The stadium is shaking with the power of these Beyblades!"
            ],
            "move_selection": [
                "🎙️ What move will they choose?",
                "🎙️ The tension is high as they prepare their next move!",
                "🎙️ The crowd is waiting in anticipation!",
                "🎙️ This could be a crucial decision!"
            ]
        }
    
    def comment(self, event_type: str) -> str:
        """Get a random comment for the given event type"""
        if event_type in self.phrases:
            return random.choice(self.phrases[event_type])
        return ""

def save_game(player: Player, player_beyblade: Beyblade, opponent_name: str, opponent_beyblade: Beyblade, current_turn: int):
    """Save the current game state"""
    save_data = {
        "player": {
            "name": player.name,
            "beyblade": {
                "name": player_beyblade.name,
                "type": player_beyblade.type,
                "health": player_beyblade.health,
                "stamina": player_beyblade.stamina,
                "spin_speed": player_beyblade.spin_speed,
                "defense_count": player_beyblade.defense_count,
                "critical_used": player_beyblade.critical_used
            }
        },
        "opponent": {
            "name": opponent_name,
            "beyblade": {
                "name": opponent_beyblade.name,
                "type": opponent_beyblade.type,
                "health": opponent_beyblade.health,
                "stamina": opponent_beyblade.stamina,
                "spin_speed": opponent_beyblade.spin_speed,
                "defense_count": opponent_beyblade.defense_count,
                "critical_used": opponent_beyblade.critical_used
            }
        },
        "current_turn": current_turn
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/save_game.json", "w") as f:
        json.dump(save_data, f, indent=2)
    print(f"{Fore.GREEN}Game saved successfully!{Style.RESET_ALL}")

def get_starter_beyblade_moves(beyblade_name: str, all_moves: list) -> list:
    """Starter bir beyblade için özel hareketleri filtreler"""
    
    # Öncelikle, eğer beyblade adı bir custom beyblade gibi görünüyorsa (tek karakter veya rakam),
    # o zaman özel filtreleme yapmıyoruz ve boş liste döndürüyoruz böylece özel hareketler korunur
    if len(beyblade_name) <= 2 or beyblade_name.isdigit():
        return []
        
    # Tüm olası beyblade isimleri ve bunların özel hareketleri
    beyblade_moves = {
        "L-Drago Destructor": ["Dragon Emperor Soaring Bite Strike", "Dragon Emperor Shield", "Dragon Emperor Supreme Flight"],
        "Storm Pegasus": ["Pegasus Starblast Attack", "Pegasus Shield", "Pegasus Stardust Driver"],
        "Rock Lion": ["Lion Wild Wind Fang Dance", "Lion Shield", "Lion King Tearing Blast"],
        "Rock Leone": ["Lion Wild Wind Fang Dance", "Lion Shield", "Lion King Tearing Blast"],
        "Dark Bull": ["Bull Upper Attack", "Bull Defense Wall", "Bull Destruction"],
        "Draciel": ["Turtle Shell Attack", "Turtle Shell Defense", "Turtle Shell Counter"],
        "Dragoon": ["Dragon Emperor Strike", "Dragon Emperor Shield", "Dragon Emperor Critical"],
        "Dranzer": ["Phoenix Wing Attack", "Phoenix Wing Shield", "Phoenix Wing Critical"],
        "Driger": ["Tiger Claw Attack", "Tiger Claw Shield", "Tiger Claw Critical"]
    }
    
    # Beyblade adına göre hareketleri filtrele
    if beyblade_name in beyblade_moves:
        moves = beyblade_moves[beyblade_name]
        return [move for move in all_moves if move.name in moves]
    
    # Eğer beyblade adı bulunamazsa boş liste döndür
    return []

def load_game(player_manager: PlayerManager) -> tuple:
    """Load a saved game"""
    try:
        with open("data/save_game.json", "r") as f:
            save_data = json.load(f)
        
        # Load player data
        player = player_manager.get_player(save_data["player"]["name"])
        if not player:
            raise ValueError("Saved player not found")
        
        # Moves data ve all_moves değişkenlerini fonksiyonun başında tanımlayalım
        # ki tüm kapsamda erişilebilir olsun
        moves_data = load_moves()
        all_moves = []
        for move_type in ['attack_moves', 'defense_moves', 'critical_moves']:
            for move in moves_data[move_type]:
                all_moves.append(create_move_from_data(move))
                
        # Get the original beyblade data with stored moves (if exists)
        original_beyblade = None
        custom_beyblades = player_manager.get_custom_beyblades(save_data["player"]["name"])
        if custom_beyblades:
            for beyblade in custom_beyblades:
                if beyblade["name"] == save_data["player"]["beyblade"]["name"]:
                    original_beyblade = beyblade
                    break
        
        # Create moves list from saved beyblade or fallback to starter-specific moves
        special_moves = []
        player_beyblade_name = save_data["player"]["beyblade"]["name"]
        
        if original_beyblade and "special_moves" in original_beyblade:
            # Use the original beyblade's special moves
            for move_type in ["attack_moves", "defense_moves", "critical_moves"]:
                if move_type in original_beyblade["special_moves"]:
                    for move in original_beyblade["special_moves"][move_type]:
                        special_moves.append(SpecialMove(
                            name=move["name"],
                            power=move["power"],
                            move_type=move["move_type"]
                        ))
        else:
            # Check if this is a starter beyblade and load its specific moves
            # all_moves değişkeni zaten yukarıda tanımlandı, tekrar oluşturmaya gerek yok
            # Filter moves for this specific starter beyblade
            special_moves = get_starter_beyblade_moves(player_beyblade_name, all_moves)
            
            # If no moves were found (perhaps not a starter), use generic ones
            if not special_moves:
                special_moves = all_moves.copy()  # all_moves'ı kopyala
        
        player_beyblade = Beyblade(
            name=save_data["player"]["beyblade"]["name"],
            type=save_data["player"]["beyblade"]["type"],
            power=75,  # Default power
            defense=75,  # Default defense
            special_moves=special_moves
        )
        player_beyblade.health = save_data["player"]["beyblade"]["health"]
        player_beyblade.stamina = save_data["player"]["beyblade"]["stamina"]
        player_beyblade.spin_speed = save_data["player"]["beyblade"]["spin_speed"]
        player_beyblade.defense_count = save_data["player"]["beyblade"]["defense_count"]
        player_beyblade.critical_used = save_data["player"]["beyblade"]["critical_used"]
        
        opponent_name = save_data["opponent"]["name"]
        
        # For opponent: if it's not "Computer", try to get original beyblade data
        original_opponent_beyblade = None
        if opponent_name != "Computer":
            opponent_custom_beyblades = player_manager.get_custom_beyblades(opponent_name)
            if opponent_custom_beyblades:
                for beyblade in opponent_custom_beyblades:
                    if beyblade["name"] == save_data["opponent"]["beyblade"]["name"]:
                        original_opponent_beyblade = beyblade
                        break
                        
            # Kayıtsız oyuncu için beyblade special_moves kaydını findBeyblade ile doğrudan veritabanında arayalım  
            if not original_opponent_beyblade:
                # Tüm oyuncuların kayıtlarını incele
                all_players = player_manager.players
                for player_name, _ in all_players.items():
                    player_beyblades = player_manager.get_custom_beyblades(player_name)
                    if player_beyblades:
                        for beyblade in player_beyblades:
                            if beyblade["name"] == save_data["opponent"]["beyblade"]["name"]:
                                original_opponent_beyblade = beyblade
                                break
        
        # Create moves list for opponent
        opponent_special_moves = []
        opponent_beyblade_name = save_data["opponent"]["beyblade"]["name"]
        
        if original_opponent_beyblade and "special_moves" in original_opponent_beyblade:
            # Use the original beyblade's special moves
            for move_type in ["attack_moves", "defense_moves", "critical_moves"]:
                if move_type in original_opponent_beyblade["special_moves"]:
                    for move in original_opponent_beyblade["special_moves"][move_type]:
                        opponent_special_moves.append(SpecialMove(
                            name=move["name"],
                            power=move["power"],
                            move_type=move["move_type"]
                        ))
        else:
            # Check if this is a starter beyblade and load its specific moves
            # Filter moves for this specific starter beyblade
            opponent_special_moves = get_starter_beyblade_moves(opponent_beyblade_name, all_moves)
            
            # If no moves were found, use generic ones
            if not opponent_special_moves:
                # Eğer beyblade tek karakterli veya sayı ise özel filtreleme yapmak için tekrar kontrol et
                # Bu kontrole ulaşıyorsa, bu beyblade muhtemelen bir custom beyblade idi
                if len(opponent_beyblade_name) <= 2 or opponent_beyblade_name.isdigit():
                    # Eğer bu opponent için kaydedilmiş özel hareketleri varsa, o hareketleri bul
                    # veya isimdeki son charı kullanarak hareket oluştur (basit bir çözüm)
                    custom_moves = []
                    custom_moves.append(SpecialMove(f"Dragon Destructor Assault (Double Attack)", 95, "attack"))
                    custom_moves.append(SpecialMove(f"Short Sharp Strike", 80, "attack"))
                    custom_moves.append(SpecialMove(f"Dragon Destructor Shield", 60, "defense"))
                    if not save_data["opponent"]["beyblade"]["critical_used"]:
                        custom_moves.append(SpecialMove(f"Dragon Destructor Short Ultimate", 100, "critical"))
                    
                    opponent_special_moves = custom_moves
                else:
                    opponent_special_moves = all_moves.copy()
        
        opponent_beyblade = Beyblade(
            name=save_data["opponent"]["beyblade"]["name"],
            type=save_data["opponent"]["beyblade"]["type"],
            power=75,  # Default power
            defense=75,  # Default defense
            special_moves=opponent_special_moves
        )
        opponent_beyblade.health = save_data["opponent"]["beyblade"]["health"]
        opponent_beyblade.stamina = save_data["opponent"]["beyblade"]["stamina"]
        opponent_beyblade.spin_speed = save_data["opponent"]["beyblade"]["spin_speed"]
        opponent_beyblade.defense_count = save_data["opponent"]["beyblade"]["defense_count"]
        opponent_beyblade.critical_used = save_data["opponent"]["beyblade"]["critical_used"]
        
        return player, player_beyblade, opponent_name, opponent_beyblade, save_data["current_turn"]
    except Exception as e:
        print(f"Error loading saved game: {e}")
        return None

def main():
    print(f"{Fore.GREEN}Welcome to Beyblade Battle Simulator!{Style.RESET_ALL}")
    print("Let it rip! 🏃‍♂️")
    
    # Initialize managers
    player_manager = PlayerManager()
    parts_manager = BeybladePartsManager()
    environment_manager = EnvironmentManager()
    commentator = Commentator()
    
    # Check for saved game
    if os.path.exists("data/save_game.json"):
        print("\n1. Start New Game")
        print("2. Load Saved Game")
        choice = get_user_choice("Enter your choice: ", 2)
        
        if choice == 2:
            saved_game = load_game(player_manager)
            if saved_game:
                player, player_beyblade, opponent_name, opponent_beyblade, current_turn = saved_game
                print(f"\n{Fore.GREEN}Loaded saved game!{Style.RESET_ALL}")
                print(f"Battle between {player.name} and {opponent_name}")
                print(f"Current turn: {current_turn}")
                print(f"{player.name}'s Beyblade: {player_beyblade}")
                print(f"{opponent_name}'s Beyblade: {opponent_beyblade}")
                
                # Continue with the battle
                battle_loop(player, player_beyblade, opponent_name, opponent_beyblade, 
                          current_turn, player_manager, environment_manager, commentator)
                return
    
    # Player registration/login
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = get_user_choice("Enter your choice: ", 3)
        
        if choice == 3:
            return
        
        name = input("Enter your name: ")
        if choice == 1:
            player = player_manager.get_player(name)
            if player is None:
                print(f"Player {name} not found!")
                continue
        else:  # Register
            try:
                player = player_manager.create_player(name)
                print(f"Welcome, {name}!")
            except ValueError as e:
                print(e)
                continue
        
        break
    
    try:
        # Beyblade selection
        print("\nChoose your Beyblade:")
        print("1. Use a starter Beyblade")
        print("2. Create a custom Beyblade")
        print("3. Use a saved custom Beyblade")
        choice = get_user_choice("Enter your choice: ", 3)
        
        if choice == 1:
            beyblade_list = create_starter_beyblades()
            print_beyblade_list(beyblade_list)
            beyblade_choice = get_user_choice("Enter the number of your choice: ", len(beyblade_list))
            player_beyblade = beyblade_list[beyblade_choice - 1]
        elif choice == 2:
            player_beyblade = create_custom_beyblade(parts_manager)
            # Save the custom beyblade with its special moves
            # Extract move data to save
            saved_moves = {"attack_moves": [], "defense_moves": [], "critical_moves": []}
            for move in player_beyblade.special_moves:
                if move.move_type == "attack":
                    saved_moves["attack_moves"].append({"name": move.name, "power": move.power, "move_type": move.move_type})
                elif move.move_type == "defense":
                    saved_moves["defense_moves"].append({"name": move.name, "power": move.power, "move_type": move.move_type})
                elif move.move_type == "critical":
                    saved_moves["critical_moves"].append({"name": move.name, "power": move.power, "move_type": move.move_type})
            
            player_manager.add_custom_beyblade(player.name, {
                "name": player_beyblade.name,
                "type": player_beyblade.type,
                "power": player_beyblade.power,
                "defense": player_beyblade.defense,
                "special_moves": saved_moves
            })
        else:  # Use saved custom beyblade
            custom_beyblades = player_manager.get_custom_beyblades(player.name)
            if not custom_beyblades:
                print("Kayıtlı beyblade bulunamadı.")
                print("\nLütfen seçim yapın:")
                print("1. Use a starter Beyblade")
                print("2. Create a custom Beyblade")
                new_choice = get_user_choice("Enter your choice: ", 2)
                
                if new_choice == 1:
                    beyblade_list = create_starter_beyblades()
                    print_beyblade_list(beyblade_list)
                    beyblade_choice = get_user_choice("Enter the number of your choice: ", len(beyblade_list))
                    player_beyblade = beyblade_list[beyblade_choice - 1]
                else:  # new_choice == 2
                    player_beyblade = create_custom_beyblade(parts_manager)
                    # Save the custom beyblade with its special moves
                    saved_moves = {"attack_moves": [], "defense_moves": [], "critical_moves": []}
                    for move in player_beyblade.special_moves:
                        if move.move_type == "attack":
                            saved_moves["attack_moves"].append({"name": move.name, "power": move.power, "move_type": move.move_type})
                        elif move.move_type == "defense":
                            saved_moves["defense_moves"].append({"name": move.name, "power": move.power, "move_type": move.move_type})
                        elif move.move_type == "critical":
                            saved_moves["critical_moves"].append({"name": move.name, "power": move.power, "move_type": move.move_type})
                    
                    player_manager.add_custom_beyblade(player.name, {
                        "name": player_beyblade.name,
                        "type": player_beyblade.type,
                        "power": player_beyblade.power,
                        "defense": player_beyblade.defense,
                        "special_moves": saved_moves
                    })
            else:
                print("\nYour saved custom beyblades:")
                for i, beyblade in enumerate(custom_beyblades, 1):
                    print(f"{i}. {beyblade['name']} ({beyblade['type']})")
                
                choice = get_user_choice("Enter the number of your choice: ", len(custom_beyblades))
                saved_beyblade = custom_beyblades[choice - 1]
                
                # Create Beyblade object from saved data with custom moves
                custom_moves = []
                
                # First check if special_moves exists in saved beyblade (for backward compatibility)
                if "special_moves" in saved_beyblade:
                    # Use saved custom moves
                    for move_type in ['attack_moves', 'defense_moves', 'critical_moves']:
                        if move_type in saved_beyblade["special_moves"]:
                            for move in saved_beyblade["special_moves"][move_type]:
                                custom_moves.append(SpecialMove(
                                    name=move["name"],
                                    power=move["power"],
                                    move_type=move["move_type"]
                                ))
                else:
                    # Use generic moves as fallback
                    moves_data = load_moves()
                    for move_type in ['attack_moves', 'defense_moves', 'critical_moves']:
                        for move in moves_data[move_type]:
                            custom_moves.append(create_move_from_data(move))
                
                player_beyblade = Beyblade(
                    name=saved_beyblade["name"],
                    type=saved_beyblade["type"],
                    power=saved_beyblade["power"],
                    defense=saved_beyblade["defense"],
                    special_moves=custom_moves
                )
        
        # Opponent selection
        print("\nChoose your opponent:")
        print("1. Computer")
        print("2. Another player")
        choice = get_user_choice("Enter your choice: ", 2)
        
        if choice == 1:
            # Computer opponent
            beyblade_list = create_starter_beyblades()
            opponent_beyblade = random.choice(beyblade_list)
            opponent_name = "Computer"
        else:
            # Human opponent
            opponent_name = input("Enter opponent's name: ")
            opponent = player_manager.get_player(opponent_name)
            is_registered = True
            if opponent is None:
                print(f"Player {opponent_name} not found!")
                register_choice = input("Would you like to register this player? (y/n): ")
                if register_choice.lower() == 'y':
                    try:
                        opponent = player_manager.create_player(opponent_name)
                        print(f"Welcome, {opponent_name}!")
                    except ValueError as e:
                        print(e)
                        return
                else:
                    print("Continuing without registration...")
                    is_registered = False
                    # Create a temporary player object for the battle
                    from player import Player
                    opponent = Player(opponent_name)
            
            print("\nChoose opponent's Beyblade:")
            print("1. Use a starter Beyblade")
            print("2. Create a custom Beyblade")
            print("3. Use a saved custom Beyblade")
            choice = get_user_choice("Enter your choice: ", 3)
            
            if choice == 1:
                beyblade_list = create_starter_beyblades()
                print_beyblade_list(beyblade_list)
                beyblade_choice = get_user_choice("Enter the number of your choice: ", len(beyblade_list))
                opponent_beyblade = beyblade_list[beyblade_choice - 1]
            elif choice == 2:
                opponent_beyblade = create_custom_beyblade(parts_manager)
                if is_registered:  # Only save custom beyblade if player is registered
                    # Save with special moves
                    saved_moves = {"attack_moves": [], "defense_moves": [], "critical_moves": []}
                    for move in opponent_beyblade.special_moves:
                        if move.move_type == "attack":
                            saved_moves["attack_moves"].append({"name": move.name, "power": move.power, "move_type": move.move_type})
                        elif move.move_type == "defense":
                            saved_moves["defense_moves"].append({"name": move.name, "power": move.power, "move_type": move.move_type})
                        elif move.move_type == "critical":
                            saved_moves["critical_moves"].append({"name": move.name, "power": move.power, "move_type": move.move_type})
                    
                    player_manager.add_custom_beyblade(opponent_name, {
                        "name": opponent_beyblade.name,
                        "type": opponent_beyblade.type,
                        "power": opponent_beyblade.power,
                        "defense": opponent_beyblade.defense,
                        "special_moves": saved_moves
                    })
            else:  # Use saved custom beyblade
                # Initialize flag
                skip_saved_beyblade = False
                
                if not is_registered:
                    print("Kayıtlı olmayan oyuncular için kaydedilmiş beyblade bulunmuyor.")
                    print("\nLütfen seçim yapın:")
                    print("1. Use a starter Beyblade")
                    print("2. Create a custom Beyblade")
                    new_choice = get_user_choice("Enter your choice: ", 2)
                    
                    if new_choice == 1:
                        beyblade_list = create_starter_beyblades()
                        print_beyblade_list(beyblade_list)
                        beyblade_choice = get_user_choice("Enter the number of your choice: ", len(beyblade_list))
                        opponent_beyblade = beyblade_list[beyblade_choice - 1]
                    else:  # new_choice == 2
                        opponent_beyblade = create_custom_beyblade(parts_manager)
                    # Skip the rest of the "else" block using a flag
                    skip_saved_beyblade = True
                
                                # Only proceed with saved beyblade logic if not skipping
                if not skip_saved_beyblade:
                    # Only registered players reach this point
                    custom_beyblades = player_manager.get_custom_beyblades(opponent_name)
                    if not custom_beyblades:
                        print("Opponent doesn't have any saved custom beyblades!")
                        # Show alternative options instead of returning
                        print("\nLütfen seçim yapın:")
                        print("1. Use a starter Beyblade")
                        print("2. Create a custom Beyblade")
                        new_choice = get_user_choice("Enter your choice: ", 2)
                        
                        if new_choice == 1:
                            beyblade_list = create_starter_beyblades()
                            print_beyblade_list(beyblade_list)
                            beyblade_choice = get_user_choice("Enter the number of your choice: ", len(beyblade_list))
                            opponent_beyblade = beyblade_list[beyblade_choice - 1]
                        else:  # new_choice == 2
                            opponent_beyblade = create_custom_beyblade(parts_manager)
                    else:
                        # Continue with saved beyblades flow
                        print("\nOpponent's saved custom beyblades:")
                        for i, beyblade in enumerate(custom_beyblades, 1):
                            print(f"{i}. {beyblade['name']} ({beyblade['type']})")
                        
                        choice = get_user_choice("Enter the number of your choice: ", len(custom_beyblades))
                        saved_beyblade = custom_beyblades[choice - 1]
                        
                        # Create Beyblade object from saved data with custom moves
                        custom_moves = []
                        
                        # First check if special_moves exists in saved beyblade (for backward compatibility)
                        if "special_moves" in saved_beyblade:
                            # Use saved custom moves
                            for move_type in ['attack_moves', 'defense_moves', 'critical_moves']:
                                if move_type in saved_beyblade["special_moves"]:
                                    for move in saved_beyblade["special_moves"][move_type]:
                                        custom_moves.append(SpecialMove(
                                            name=move["name"],
                                            power=move["power"],
                                            move_type=move["move_type"]
                                        ))
                        else:
                            # Use generic moves as fallback
                            moves_data = load_moves()
                            for move_type in ['attack_moves', 'defense_moves', 'critical_moves']:
                                for move in moves_data[move_type]:
                                    custom_moves.append(create_move_from_data(move))
                        
                        opponent_beyblade = Beyblade(
                            name=saved_beyblade["name"],
                            type=saved_beyblade["type"],
                            power=saved_beyblade["power"],
                            defense=saved_beyblade["defense"],
                            special_moves=custom_moves
                        )
        
        # Battle loop
        current_turn = 1
        
        while not player_beyblade.is_defeated() and not opponent_beyblade.is_defeated():
            print(f"\n{Fore.CYAN}=== Turn {current_turn} ==={Style.RESET_ALL}")
            print(f"{commentator.comment('turn_start')}")
            
            # Check for environmental events
            event = environment_manager.check_for_event()
            if event:
                print(f"\n{Fore.YELLOW}Environmental Event: {event.description}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{commentator.comment('environmental')}{Style.RESET_ALL}")
                # Apply event effects to both beyblades
                player_stats = environment_manager.apply_event_effects(
                    player_beyblade.power,
                    player_beyblade.defense,
                    player_beyblade.spin_speed,
                    player_beyblade.stamina
                )
                opponent_stats = environment_manager.apply_event_effects(
                    opponent_beyblade.power,
                    opponent_beyblade.defense,
                    opponent_beyblade.spin_speed,
                    opponent_beyblade.stamina
                )
            
            # Reset defense status at the start of each turn
            player_beyblade.start_turn()
            opponent_beyblade.start_turn()
            
            # Player move selection
            print(f"\n{player.name} ({player_beyblade.name}), choose your move!")
            print(f"{commentator.comment('move_selection')}")
            print_moves_list(player_beyblade)
            
            # Get player choice
            total_options = len(player_beyblade.available_moves) + 2  # +2 for save and exit options
            choice = get_user_choice("Enter your choice: ", total_options)
            
            # Handle save/exit options
            if choice > len(player_beyblade.available_moves):
                if choice == len(player_beyblade.available_moves) + 1:  # Save game
                    save_game(player, player_beyblade, opponent_name, opponent_beyblade, current_turn)
                    continue
                else:  # Exit game
                    if input("Are you sure you want to exit? (y/n): ").lower() == 'y':
                        return
            
            # Get the selected move
            move1 = player_beyblade.available_moves[choice - 1]
            
            # Opponent move selection
            if opponent_name == "Computer":
                # Computer AI move selection
                available_moves = [m for m in opponent_beyblade.special_moves if m.move_type == "attack"]
                if opponent_beyblade.defense_count > 0:
                    available_moves.extend([m for m in opponent_beyblade.special_moves if m.move_type == "defense"])
                if not opponent_beyblade.critical_used:
                    available_moves.extend([m for m in opponent_beyblade.special_moves if m.move_type == "critical"])
                
                # Simple AI: 30% chance to defend if health is low, 20% chance to use critical if available
                if opponent_beyblade.health < 30 and opponent_beyblade.defense_count > 0:
                    defense_moves = [m for m in available_moves if m.move_type == "defense"]
                    if defense_moves:
                        move2 = random.choice(defense_moves)
                    else:
                        move2 = random.choice(available_moves)
                elif not opponent_beyblade.critical_used and random.random() < 0.2:
                    critical_moves = [m for m in available_moves if m.move_type == "critical"]
                    if critical_moves:
                        move2 = random.choice(critical_moves)
                    else:
                        move2 = random.choice(available_moves)
                else:
                    move2 = random.choice(available_moves)
            else:
                print(f"\n{opponent_name} ({opponent_beyblade.name}), choose your move!")
                print_moves_list(opponent_beyblade)
                move2_choice = get_user_choice("Enter the number of your move: ", len(opponent_beyblade.available_moves))
                move2 = opponent_beyblade.available_moves[move2_choice - 1]
            
            # Track defense status
            player_defending = move1.move_type == "defense"
            opponent_defending = move2.move_type == "defense"
            
            # Execute moves
            if player_defending:
                result1 = player_beyblade.use_special_move(move1, player_beyblade)
                
                if 'error' in result1 and result1['error'] == 'no_defense_moves_left':
                    attack_moves = [m for m in player_beyblade.special_moves if m.move_type == "attack"]
                    if attack_moves:
                        move1 = attack_moves[0]
                        print(f"\nAutomatically selected alternative move: {move1.name}")
                        result1 = player_beyblade.use_special_move(move1, opponent_beyblade)
                        opponent_beyblade.health -= result1['damage']
                        print(f"\n{player_beyblade.name} used {move1.name}!")
                        if result1['critical']:
                            print(f"🔥 CRITICAL HIT!")
                            print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                        print(f"Damage dealt: {result1['damage']}")
                    else:
                        print(f"\n{player_beyblade.name} could not make a move this turn!")
                        result1 = {'damage': 0}
                else:
                    print(f"\n{player_beyblade.name} used {move1.name}!")
                    print(f"{Fore.BLUE}{commentator.comment('defense')}{Style.RESET_ALL}")
                    print(f"🛡️ Defense activated! Next attack damage will be reduced by 30%")
                    print(f"Remaining defense moves: {result1.get('defense_remaining', player_beyblade.defense_count)}")
            else:
                if opponent_defending:
                    result1 = player_beyblade.use_special_move(move1, opponent_beyblade)
                    original_damage = result1['damage']
                    reduction = int(original_damage * 0.3)
                    final_damage = original_damage - reduction
                    final_damage = max(1, final_damage)
                    
                    opponent_beyblade.health -= final_damage
                    
                    print(f"\n{player_beyblade.name} used {move1.name}!")
                    if result1['critical']:
                        print(f"🔥 CRITICAL HIT!")
                        print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                    print(f"Original damage: {original_damage}")
                    print(f"🛡️ Defense reduced damage by: {reduction} (30%)")
                    print(f"Final damage: {final_damage}")
                else:
                    result1 = player_beyblade.use_special_move(move1, opponent_beyblade)
                    opponent_beyblade.health -= result1['damage']
                    
                    print(f"\n{player_beyblade.name} used {move1.name}!")
                    if result1['critical']:
                        print(f"🔥 CRITICAL HIT!")
                        print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                    print(f"Damage dealt: {result1['damage']}")
            
            if not opponent_beyblade.is_defeated():
                if opponent_defending:
                    result2 = opponent_beyblade.use_special_move(move2, opponent_beyblade)
                    
                    if 'error' in result2 and result2['error'] == 'no_defense_moves_left':
                        attack_moves = [m for m in opponent_beyblade.special_moves if m.move_type == "attack"]
                        if attack_moves:
                            move2 = attack_moves[0]
                            print(f"\nAutomatically selected alternative move: {move2.name}")
                            result2 = opponent_beyblade.use_special_move(move2, player_beyblade)
                            player_beyblade.health -= result2['damage']
                            print(f"\n{opponent_beyblade.name} used {move2.name}!")
                            if result2['critical']:
                                print(f"🔥 CRITICAL HIT!")
                                print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                            print(f"Damage dealt: {result2['damage']}")
                        else:
                            print(f"\n{opponent_beyblade.name} could not make a move this turn!")
                            result2 = {'damage': 0}
                    else:
                        print(f"\n{opponent_beyblade.name} used {move2.name}!")
                        print(f"🛡️ Defense activated! Next attack damage will be reduced by 30%")
                        print(f"Remaining defense moves: {result2.get('defense_remaining', opponent_beyblade.defense_count)}")
                else:
                    if player_defending:
                        result2 = opponent_beyblade.use_special_move(move2, player_beyblade)
                        original_damage = result2['damage']
                        reduction = int(original_damage * 0.3)
                        final_damage = original_damage - reduction
                        final_damage = max(1, final_damage)
                        
                        player_beyblade.health -= final_damage
                        
                        print(f"\n{opponent_beyblade.name} used {move2.name}!")
                        if result2['critical']:
                            print(f"🔥 CRITICAL HIT!")
                            print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                        print(f"Original damage: {original_damage}")
                        print(f"🛡️ Defense reduced damage by: {reduction} (30%)")
                        print(f"Final damage: {final_damage}")
                    else:
                        result2 = opponent_beyblade.use_special_move(move2, player_beyblade)
                        player_beyblade.health -= result2['damage']
                        
                        print(f"\n{opponent_beyblade.name} used {move2.name}!")
                        if result2['critical']:
                            print(f"🔥 CRITICAL HIT!")
                            print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                        print(f"Damage dealt: {result2['damage']}")
            
            # Show status after both moves
            print(f"\n{Fore.CYAN}=== Status ==={Style.RESET_ALL}")
            print(f"{player.name}: {player_beyblade}")
            print(f"{opponent_name}: {opponent_beyblade}")
            
            if opponent_beyblade.health < 30:
                print(f"{Fore.YELLOW}{commentator.comment('low_health')}{Style.RESET_ALL}")
            
            current_turn += 1
        
        # Battle end
        if player_beyblade.is_defeated():
            print(f"\n{Fore.RED}{opponent_name} wins!{Style.RESET_ALL}")
            if opponent_name != "Computer":
                opponent = player_manager.get_player(opponent_name)
                opponent.wins += 1
                player.losses += 1
                player_manager.update_player(opponent)
                player_manager.update_player(player)
            print(f"\n{Fore.MAGENTA}{commentator.comment('victory')}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}{player.name} wins!{Style.RESET_ALL}")
            player.wins += 1
            if opponent_name != "Computer":
                opponent = player_manager.get_player(opponent_name)
                opponent.losses += 1
                player_manager.update_player(player)
                player_manager.update_player(opponent)
            print(f"\n{Fore.MAGENTA}{commentator.comment('victory')}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def battle_loop(player, player_beyblade, opponent_name, opponent_beyblade, 
               current_turn, player_manager, environment_manager, commentator):
    """Main battle loop"""
    while not player_beyblade.is_defeated() and not opponent_beyblade.is_defeated():
        print(f"\n{Fore.CYAN}=== Turn {current_turn} ==={Style.RESET_ALL}")
        print(f"{commentator.comment('turn_start')}")
        
        # Check for environmental events
        event = environment_manager.check_for_event()
        if event:
            print(f"\n{Fore.YELLOW}Environmental Event: {event.description}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{commentator.comment('environmental')}{Style.RESET_ALL}")
            # Apply event effects to both beyblades
            player_stats = environment_manager.apply_event_effects(
                player_beyblade.power,
                player_beyblade.defense,
                player_beyblade.spin_speed,
                player_beyblade.stamina
            )
            opponent_stats = environment_manager.apply_event_effects(
                opponent_beyblade.power,
                opponent_beyblade.defense,
                opponent_beyblade.spin_speed,
                opponent_beyblade.stamina
            )
        
        # Reset defense status at the start of each turn
        player_beyblade.start_turn()
        opponent_beyblade.start_turn()
        
        # Player move selection
        print(f"\n{player.name} ({player_beyblade.name}), choose your move!")
        print(f"{commentator.comment('move_selection')}")
        print_moves_list(player_beyblade)
        
        # Get player choice
        total_options = len(player_beyblade.available_moves) + 2  # +2 for save and exit options
        choice = get_user_choice("Enter your choice: ", total_options)
        
        # Handle save/exit options
        if choice > len(player_beyblade.available_moves):
            if choice == len(player_beyblade.available_moves) + 1:  # Save game
                save_game(player, player_beyblade, opponent_name, opponent_beyblade, current_turn)
                continue
            else:  # Exit game
                if input("Are you sure you want to exit? (y/n): ").lower() == 'y':
                    return
        
        # Get the selected move
        move1 = player_beyblade.available_moves[choice - 1]
        
        # Opponent move selection
        if opponent_name == "Computer":
            # Computer AI move selection
            available_moves = [m for m in opponent_beyblade.special_moves if m.move_type == "attack"]
            if opponent_beyblade.defense_count > 0:
                available_moves.extend([m for m in opponent_beyblade.special_moves if m.move_type == "defense"])
            if not opponent_beyblade.critical_used:
                available_moves.extend([m for m in opponent_beyblade.special_moves if m.move_type == "critical"])
            
            # Simple AI: 30% chance to defend if health is low, 20% chance to use critical if available
            if opponent_beyblade.health < 30 and opponent_beyblade.defense_count > 0:
                defense_moves = [m for m in available_moves if m.move_type == "defense"]
                if defense_moves:
                    move2 = random.choice(defense_moves)
                else:
                    move2 = random.choice(available_moves)
            elif not opponent_beyblade.critical_used and random.random() < 0.2:
                critical_moves = [m for m in available_moves if m.move_type == "critical"]
                if critical_moves:
                    move2 = random.choice(critical_moves)
                else:
                    move2 = random.choice(available_moves)
            else:
                move2 = random.choice(available_moves)
        else:
            print(f"\n{opponent_name} ({opponent_beyblade.name}), choose your move!")
            print_moves_list(opponent_beyblade)
            move2_choice = get_user_choice("Enter the number of your move: ", len(opponent_beyblade.available_moves))
            move2 = opponent_beyblade.available_moves[move2_choice - 1]
        
        # Track defense status
        player_defending = move1.move_type == "defense"
        opponent_defending = move2.move_type == "defense"
        
        # Execute moves
        if player_defending:
            result1 = player_beyblade.use_special_move(move1, player_beyblade)
            
            if 'error' in result1 and result1['error'] == 'no_defense_moves_left':
                attack_moves = [m for m in player_beyblade.special_moves if m.move_type == "attack"]
                if attack_moves:
                    move1 = attack_moves[0]
                    print(f"\nAutomatically selected alternative move: {move1.name}")
                    result1 = player_beyblade.use_special_move(move1, opponent_beyblade)
                    opponent_beyblade.health -= result1['damage']
                    print(f"\n{player_beyblade.name} used {move1.name}!")
                    if result1['critical']:
                        print(f"🔥 CRITICAL HIT!")
                        print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                    print(f"Damage dealt: {result1['damage']}")
                else:
                    print(f"\n{player_beyblade.name} could not make a move this turn!")
                    result1 = {'damage': 0}
            else:
                print(f"\n{player_beyblade.name} used {move1.name}!")
                print(f"{Fore.BLUE}{commentator.comment('defense')}{Style.RESET_ALL}")
                print(f"🛡️ Defense activated! Next attack damage will be reduced by 30%")
                print(f"Remaining defense moves: {result1.get('defense_remaining', player_beyblade.defense_count)}")
        else:
            if opponent_defending:
                result1 = player_beyblade.use_special_move(move1, opponent_beyblade)
                original_damage = result1['damage']
                reduction = int(original_damage * 0.3)
                final_damage = original_damage - reduction
                final_damage = max(1, final_damage)
                
                opponent_beyblade.health -= final_damage
                
                print(f"\n{player_beyblade.name} used {move1.name}!")
                if result1['critical']:
                    print(f"🔥 CRITICAL HIT!")
                    print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                print(f"Original damage: {original_damage}")
                print(f"🛡️ Defense reduced damage by: {reduction} (30%)")
                print(f"Final damage: {final_damage}")
            else:
                result1 = player_beyblade.use_special_move(move1, opponent_beyblade)
                opponent_beyblade.health -= result1['damage']
                
                print(f"\n{player_beyblade.name} used {move1.name}!")
                if result1['critical']:
                    print(f"🔥 CRITICAL HIT!")
                    print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                print(f"Damage dealt: {result1['damage']}")
            
            if not opponent_beyblade.is_defeated():
                if opponent_defending:
                    result2 = opponent_beyblade.use_special_move(move2, opponent_beyblade)
                    
                    if 'error' in result2 and result2['error'] == 'no_defense_moves_left':
                        attack_moves = [m for m in opponent_beyblade.special_moves if m.move_type == "attack"]
                        if attack_moves:
                            move2 = attack_moves[0]
                            print(f"\nAutomatically selected alternative move: {move2.name}")
                            result2 = opponent_beyblade.use_special_move(move2, player_beyblade)
                            player_beyblade.health -= result2['damage']
                            print(f"\n{opponent_beyblade.name} used {move2.name}!")
                            if result2['critical']:
                                print(f"🔥 CRITICAL HIT!")
                                print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                            print(f"Damage dealt: {result2['damage']}")
                        else:
                            print(f"\n{opponent_beyblade.name} could not make a move this turn!")
                            result2 = {'damage': 0}
                    else:
                        print(f"\n{opponent_beyblade.name} used {move2.name}!")
                        print(f"🛡️ Defense activated! Next attack damage will be reduced by 30%")
                        print(f"Remaining defense moves: {result2.get('defense_remaining', opponent_beyblade.defense_count)}")
                else:
                    if player_defending:
                        result2 = opponent_beyblade.use_special_move(move2, player_beyblade)
                        original_damage = result2['damage']
                        reduction = int(original_damage * 0.3)
                        final_damage = original_damage - reduction
                        final_damage = max(1, final_damage)
                        
                        player_beyblade.health -= final_damage
                        
                        print(f"\n{opponent_beyblade.name} used {move2.name}!")
                        if result2['critical']:
                            print(f"🔥 CRITICAL HIT!")
                            print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                        print(f"Original damage: {original_damage}")
                        print(f"🛡️ Defense reduced damage by: {reduction} (30%)")
                        print(f"Final damage: {final_damage}")
                    else:
                        result2 = opponent_beyblade.use_special_move(move2, player_beyblade)
                        player_beyblade.health -= result2['damage']
                        
                        print(f"\n{opponent_beyblade.name} used {move2.name}!")
                        if result2['critical']:
                            print(f"🔥 CRITICAL HIT!")
                            print(f"{Fore.RED}{commentator.comment('critical_hit')}{Style.RESET_ALL}")
                        print(f"Damage dealt: {result2['damage']}")
            
            # Show status after both moves
            print(f"\n{Fore.CYAN}=== Status ==={Style.RESET_ALL}")
            print(f"{player.name}: {player_beyblade}")
            print(f"{opponent_name}: {opponent_beyblade}")
            
            # Check for low stamina
            if player_beyblade.stamina < 30:
                print(f"{Fore.YELLOW}{commentator.comment('low_stamina')}{Style.RESET_ALL}")
            if opponent_beyblade.stamina < 30:
                print(f"{Fore.YELLOW}{commentator.comment('low_stamina')}{Style.RESET_ALL}")
            
            current_turn += 1
        
        # Battle end
        if player_beyblade.is_defeated():
            print(f"\n{Fore.RED}{opponent_name} wins!{Style.RESET_ALL}")
            if opponent_name != "Computer":
                opponent = player_manager.get_player(opponent_name)
                if opponent:  # Only update stats if opponent is registered
                    opponent.wins += 1
                    player.losses += 1
                    player_manager.update_player(opponent)
                    player_manager.update_player(player)
        else:
            print(f"\n{Fore.GREEN}{player.name} wins!{Style.RESET_ALL}")
            player.wins += 1
            if opponent_name != "Computer":
                opponent = player_manager.get_player(opponent_name)
                if opponent:  # Only update stats if opponent is registered
                    opponent.losses += 1
                    player_manager.update_player(player)
                    player_manager.update_player(opponent)
        
        print(f"\n{Fore.MAGENTA}{commentator.comment('victory')}{Style.RESET_ALL}")
        
        # Delete save file after battle ends
        if os.path.exists("data/save_game.json"):
            os.remove("data/save_game.json")

if __name__ == "__main__":
    main() 