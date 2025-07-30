import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player with Editable Lyrics")
        self.root.geometry("900x500")
        
        pygame.mixer.init()
        
        self.current_song = None
        self.lyrics_text = ""
        self.edit_mode = False
        self.lyrics_file = None
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_frame = tk.LabelFrame(main_frame, text="Lyrics", padx=5, pady=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.edit_btn = tk.Button(left_frame, text="✏️", command=self.toggle_edit, font=("Arial", 12))
        self.edit_btn.pack(anchor="ne", pady=5)
        
        self.lyrics_display = tk.Text(left_frame, height=20, state=tk.DISABLED, font=("Arial", 11))
        self.lyrics_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_frame = tk.LabelFrame(main_frame, text="Music Player", padx=5, pady=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(10, 0))
        
        self.cover_img = Image.new("RGB", (250, 250), "gray")
        self.cover_photo = ImageTk.PhotoImage(self.cover_img)
        self.cover_label = tk.Label(right_frame, image=self.cover_photo)
        self.cover_label.pack(pady=10)
        
        self.song_label = tk.Label(right_frame, text="No song selected", font=("Arial", 10))
        self.song_label.pack(pady=5)
        
        controls_frame = tk.Frame(right_frame)
        controls_frame.pack(pady=10)
        
        self.play_btn = tk.Button(controls_frame, text="▶️", command=self.play_music, font=("Arial", 14))
        self.play_btn.grid(row=0, column=0, padx=5)
        
        self.pause_btn = tk.Button(controls_frame, text="⏸️", command=self.pause_music, font=("Arial", 14))
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        self.stop_btn = tk.Button(controls_frame, text="⏹️", command=self.stop_music, font=("Arial", 14))
        self.stop_btn.grid(row=0, column=2, padx=5)
        
        load_btn = tk.Button(right_frame, text="Load Song", command=self.load_music, width=15)
        load_btn.pack(pady=10)
    
    def toggle_edit(self):
        self.edit_mode = not self.edit_mode
        
        if self.edit_mode:
            self.lyrics_display.config(state=tk.NORMAL)
            self.edit_btn.config(text="💾", fg="green")
        else:
            self.lyrics_text = self.lyrics_display.get("1.0", tk.END)
            self.save_lyrics()
            self.lyrics_display.config(state=tk.DISABLED)
            self.edit_btn.config(text="✏️", fg="black")
    
    def save_lyrics(self):
        if self.lyrics_file:
            try:
                with open(self.lyrics_file, "w", encoding="utf-8") as f:
                    f.write(self.lyrics_text)
            except Exception as e:
                messagebox.showerror("Error", f"Save failed:\n{str(e)}")
    
    def load_music(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        self.current_song = file_path
        song_name = os.path.basename(file_path)
        self.song_label.config(text=song_name)
        
        self.lyrics_file = os.path.splitext(file_path)[0] + ".txt"
        if os.path.exists(self.lyrics_file):
            with open(self.lyrics_file, "r", encoding="utf-8") as f:
                self.lyrics_text = f.read()
        else:
            self.lyrics_text = f"Lyrics for:\n{song_name}"
        
        self.lyrics_display.config(state=tk.NORMAL)
        self.lyrics_display.delete("1.0", tk.END)
        self.lyrics_display.insert(tk.END, self.lyrics_text)
        self.lyrics_display.config(state=tk.DISABLED)
    
    def play_music(self):
        if self.current_song:
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
    
    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
    
    def stop_music(self):
        pygame.mixer.music.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()