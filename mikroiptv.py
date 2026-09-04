import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import vlc
import customtkinter as ctk
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MikroIptv(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MikroIptv")
        self.geometry("1400x800")
        self.minsize(900, 600)

        self.channels = []
        self.volume = 100
        self.fullscreen = False

        self.instance = vlc.Instance("--no-video-title-show", "--quiet")
        self.player = self.instance.media_player_new()

        self.create_ui()
        self.protocol("WM_DELETE_WINDOW", self.cleanup)
        self.bind("<Escape>", self.on_escape)
        self.bind("<F11>", self.toggle_fullscreen)

        # Fix: use self.after instead of self.root.after
        self.after(100, self.update_video_handle)

    def update_video_handle(self):
        """Keep video handle stable."""
        try:
            if self.player:
                self.player.set_hwnd(self.video_frame.winfo_id())
        except:
            pass
        self.after(500, self.update_video_handle)

    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        # Video area
        self.video_frame = ctk.CTkFrame(self.main_frame, fg_color="black", corner_radius=10)
        self.video_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_frame, width=220, corner_radius=10)
        self.sidebar.pack(side="right", fill="y", padx=(5, 10), pady=10)
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="📺 Channels",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))

        self.channel_list = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.channel_list.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="⛶ Fullscreen",
            height=35,
            command=self.toggle_fullscreen
        ).pack(fill="x", padx=10, pady=(0, 15))

        # Controls
        self.controls = ctk.CTkFrame(self, height=55, corner_radius=10)
        self.controls.pack(fill="x", side="bottom", padx=10, pady=(0, 10))

        ctk.CTkButton(self.controls, text="📂 File", width=90, command=self.open_file).pack(side="left", padx=(15, 5), pady=10)
        ctk.CTkButton(self.controls, text="🔗 URL", width=90, command=self.open_url).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(self.controls, text="⏹ Stop", width=90, fg_color="#d32f2f", hover_color="#b71c1c", command=self.stop).pack(side="left", padx=5, pady=10)

        self.volume_label = ctk.CTkLabel(self.controls, text=f"🔊 {self.volume}")
        self.volume_label.pack(side="right", padx=(0, 10))

        ctk.CTkButton(self.controls, text="+", width=40, command=self.volume_up).pack(side="right", padx=2, pady=10)
        ctk.CTkButton(self.controls, text="-", width=40, command=self.volume_down).pack(side="right", padx=2, pady=10)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            self.sidebar.pack_forget()
            self.controls.pack_forget()
            self.video_frame.pack_forget()
            self.video_frame.pack(fill="both", expand=True, padx=0, pady=0)
            self.attributes("-fullscreen", True)
        else:
            self.attributes("-fullscreen", False)
            self.video_frame.pack_forget()
            self.video_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
            self.sidebar.pack(side="right", fill="y", padx=(5, 10), pady=10)
            self.controls.pack(fill="x", side="bottom", padx=10, pady=(0, 10))

        self.after(100, self.update_video_handle)

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Select IPTV Playlist",
            filetypes=[("IPTV", "*.m3u *.m3u8"), ("All Files", "*.*")]
        )
        if path:
            self.parse_m3u(path)

    def parse_m3u(self, path):
        self.channels.clear()
        for widget in self.channel_list.winfo_children():
            widget.destroy()

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            pattern = r'#EXTINF:.*?,(.*?)\n(.*?)\n'
            matches = re.findall(pattern, content)

            for name, url in matches:
                name = name.strip()
                url = url.strip()
                if url and not url.startswith("#"):
                    self.channels.append((name, url))
                    self.add_channel_button(name)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_channel_button(self, name):
        btn = ctk.CTkButton(
            self.channel_list,
            text=name,
            anchor="w",
            height=30,
            fg_color="transparent",
            hover_color="#333333",
            corner_radius=5,
            font=ctk.CTkFont(size=11)
        )
        btn.pack(fill="x", pady=1)
        btn.bind("<Button-1>", lambda e, n=name: self.play_channel(n))
        btn.bind("<Button-3>", lambda e, n=name: self.show_epg(n))

    def open_url(self):
        url = simpledialog.askstring("URL", "Enter stream URL:")
        if url:
            self.channels.append(("Stream", url))
            self.add_channel_button("Stream")
            self.play(url)

    def play_channel(self, name):
        for ch_name, url in self.channels:
            if ch_name == name:
                self.play(url)
                break

    def play(self, source):
        self.player.stop()
        media = self.instance.media_new(source)
        self.player.set_media(media)
        self.player.set_hwnd(self.video_frame.winfo_id())
        self.player.audio_set_volume(self.volume)
        self.player.play()
        self.after(200, self.update_video_handle)

    def show_epg(self, channel_name):
        epg_window = ctk.CTkToplevel(self)
        epg_window.title(f"EPG — {channel_name}")
        epg_window.geometry("500x600")

        ctk.CTkLabel(
            epg_window,
            text=f"📅 {channel_name}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15)

        epg_text = ctk.CTkTextbox(epg_window, font=ctk.CTkFont(size=13))
        epg_text.pack(fill="both", expand=True, padx=15, pady=10)

        schedule = ""
        for hour in range(24):
            schedule += f"{hour:02d}:00 — Program\n"

        epg_text.insert("1.0", schedule)
        epg_text.configure(state="disabled")
        epg_window.bind("<Escape>", lambda e: epg_window.destroy())

    def volume_up(self):
        if self.volume < 200:
            self.volume += 10
            self.volume_label.configure(text=f"🔊 {self.volume}")
            self.player.audio_set_volume(self.volume)

    def volume_down(self):
        if self.volume > 100:
            self.volume -= 10
            self.volume_label.configure(text=f"🔊 {self.volume}")
            self.player.audio_set_volume(self.volume)

    def stop(self):
        self.player.stop()

    def on_escape(self, event):
        if self.fullscreen:
            self.toggle_fullscreen()
        else:
            self.cleanup()

    def cleanup(self):
        self.player.stop()
        self.destroy()


if __name__ == "__main__":
    app = MikroIptv()
    app.mainloop()
