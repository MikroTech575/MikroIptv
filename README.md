# 📺 MikroIptv

A lightweight IPTV player built with Python.  
Play IPTV streams from a URL or M3U file — **no VLC required**.  
Everything works in a single window with built-in video and audio.

![MikroIptv](screenshot.png)

---

## ✨ Features

- 🎬 Play IPTV streams by URL
- 📂 Open M3U playlists from files
- 🖥️ Built-in video player (no external dependencies)
- 🔊 Built-in audio support
- 📺 Channel list panel (right side)
- 📅 Program schedule (EPG) — right-click on channel
- 🔉 Volume control (100–200)
- 🖼️ Single-window experience
- ⚡ Lightweight and fast
- 🖥️ Fullscreen video stretching (4:3 → 16:9)
- ❌ Close with ESC or window close button

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Install dependencies
```bash
pip install python-vlc pillow
```

### Install VLC (required for playback)
- **Windows:** https://www.videolan.org/vlc/
- **Linux:** `sudo apt install vlc`
- **macOS:** `brew install vlc`

---

## 🎮 Usage

```bash
python mikroiptv.py
```

### Controls
| Action | Description |
|--------|-------------|
| **Open File** | Load M3U playlist |
| **Open URL** | Play stream by URL |
| **Double-click** on channel | Play selected channel |
| **Right-click** on channel | Show program schedule |
| **+ / -** | Volume control (100–200) |
| **Stop** | Stop playback |
| **ESC** | Close schedule or exit app |
| **Close window** | Exit app |

---

## 📺 Supported Formats

- M3U / M3U8 playlists
- HTTP / HTTPS streams
- HLS streams
- MPEG-TS streams

---

## 🛠️ Planned Features

- [x] M3U parser with channel list
- [x] Audio support
- [x] Fullscreen stretching
- [x] Channel switching
- [x] Volume control
- [x] Program schedule (EPG)
- [ ] Real EPG data from XMLTV
- [ ] Favorites list
- [ ] Keyboard shortcuts
- [ ] Recording

---

## 📷 Screenshots

![MikroIptv Main](screenshot.png)

*(Add more screenshots here)*

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to open issues or submit pull requests.

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**MikroTechMic**  
GitHub: [mikrotechmic](https://github.com/mikrotechmic)
