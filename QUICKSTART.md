# Quick Start Guide

## Installation

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd MusicPlay
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Standard Mode (with GUI)
```bash
python music_player.py
```

The application will open in a new window with two tabs:
- **本地音乐 (Local Music)**: Manage and play local music files
- **在线音乐 (Online Music)**: Search and download music online

## Using Local Music Features

### 1. Select Music Folder
- Click **"选择音乐文件夹" (Select Music Folder)** button
- Browse to your music directory
- The app will scan for all supported audio files

### 2. Play Music
- Double-click any song in the list to start playing
- Use the control buttons at the bottom:
  - **播放/暂停** (Play/Pause)
  - **上一曲** (Previous)
  - **下一曲** (Next)

### 3. Playback Controls
- **Volume**: Use the slider on the right to adjust volume
- **Progress Bar**: Drag to seek to different positions
- **重复** (Repeat): Enable to repeat current song
- **随机** (Shuffle): Enable shuffle mode for random playback

## Using Online Music Features

### 1. Search for Music
- Switch to **"在线音乐" (Online Music)** tab
- Enter a song name or artist in the search box
- Click **"搜索" (Search)** button

### 2. Download Music
- Select a song from the search results
- Click **"下载选中音乐" (Download Selected Music)**
- Choose a download location
- Wait for the download to complete

**Note**: The online music feature currently uses mock/demo data. For real music downloads, you need to integrate with a legitimate music API.

## Supported Audio Formats

- MP3
- WAV
- FLAC
- AAC
- OGG
- WMA
- M4A
- OPUS
- AMR
- MIDI

## Keyboard Shortcuts

Currently, the application primarily uses mouse controls. Keyboard shortcuts may be added in future versions.

## Configuration

The application saves your settings in `config.json`:
- Default music folder
- Download folder
- Volume level

You can manually edit this file to change default settings.

## Troubleshooting

### No Audio Output
If you're running in a cloud or headless environment:
- The application will use a dummy audio driver
- Visual controls will work, but no sound will play
- This is normal behavior for environments without audio hardware

### Audio Device Error
If you see "ALSA: Couldn't open audio device":
- This is normal in cloud environments
- The app will automatically fall back to dummy audio
- All other features will work normally

### Can't Find Music Files
Make sure:
- Your music files are in supported formats (see list above)
- The folder path is accessible
- File permissions allow reading

### Search Returns No Results
The online search currently uses mock data:
- Real results depend on API integration
- See `DEVELOPMENT.md` for how to integrate real APIs

## Testing

Run the test suite to verify everything works:
```bash
python test_modules.py
```

Expected output:
```
✅ Local Music Manager tests passed!
✅ Online Music Manager tests passed!
🎉 All tests passed successfully!
```

## Getting Help

For more detailed information:
- **README.md**: Project overview and features
- **DEVELOPMENT.md**: Developer documentation
- **SUMMARY.md**: Latest changes and improvements

## Next Steps

1. **Add your music**: Copy your music files to a folder
2. **Start the player**: Run `python music_player.py`
3. **Select folder**: Click the folder selection button
4. **Enjoy**: Double-click to play your favorite songs!

Happy listening! 🎵
