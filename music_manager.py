import pygame
import os

class MusicManager:
    def __init__(self):
        print("Initializing MusicManager...")
        pygame.mixer.init(frequency=44100)
        # Try both MP3 and WAV formats
        self.background_music_path_mp3 = os.path.join("Music", "background_music.mp3")
        self.background_music_path_wav = os.path.join("Music", "background_music.wav")
        print(f"MP3 file exists: {os.path.exists(self.background_music_path_mp3)}")
        print(f"WAV file exists: {os.path.exists(self.background_music_path_wav)}")
        self.is_playing = False
        self.volume = 0.1  # Default volume (0.0 to 1.0)
        
    def play_background_music(self, loop=True):
        """Play the background music"""
        try:
            print("Attempting to load music...")
            # Try WAV first, then fall back to MP3
            if os.path.exists(self.background_music_path_wav):
                pygame.mixer.music.load(self.background_music_path_wav)
                print("WAV music loaded successfully")
            else:
                pygame.mixer.music.load(self.background_music_path_mp3)
                print("MP3 music loaded successfully")
            
            pygame.mixer.music.set_volume(self.volume)
            if loop:
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            else:
                pygame.mixer.music.play()
            print("Music started playing")
            self.is_playing = True
        except Exception as e:
            print(f"Error playing music: {e}")
            print(f"Current working directory: {os.getcwd()}")
    
    def stop_music(self):
        """Stop the background music"""
        pygame.mixer.music.stop()
        self.is_playing = False
    
    def pause_music(self):
        """Pause the background music"""
        if self.is_playing:
            pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause the background music"""
        if self.is_playing:
            pygame.mixer.music.unpause()
    
    def set_volume(self, volume):
        """Set the music volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
        pygame.mixer.music.set_volume(self.volume)
    
    def is_music_playing(self):
        """Check if music is currently playing"""
        return self.is_playing 