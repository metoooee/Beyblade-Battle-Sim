from music_manager import MusicManager
import time

def test_music():
    print("Starting music test...")
    music_manager = MusicManager()
    
    print("\nTrying to play music...")
    music_manager.play_background_music()
    
    # Keep the program running for 5 seconds to hear the music
    print("\nMusic should be playing now. Waiting for 5 seconds...")
    time.sleep(5)
    
    print("\nStopping music...")
    music_manager.stop_music()
    print("Test complete!")

if __name__ == "__main__":
    test_music() 