# Development Notes

## Recent Improvements

### Bug Fixes
1. **Fixed undefined variable error** in `music_player.py` (line 394)
   - Changed variable name from `e` to `error` with proper lambda capture
   
2. **Fixed invalid escape sequences** in file paths
   - Changed from string concatenation with backslashes to `os.path.join()`
   - Ensures cross-platform compatibility

3. **Improved error handling** for bare except clauses
   - Changed `except:` to `except Exception:` for better exception handling
   
4. **Fixed pygame.error comparison**
   - Changed `== False` to `not` for more Pythonic code

### Code Quality Improvements
1. **Removed unused imports**
   - Removed `tkinter.simpledialog` from `music_player.py`
   - Removed `json` from `modules/online_music_manager.py`
   
2. **Fixed f-string issues**
   - Removed unnecessary f-string prefixes where no placeholders were used
   - Added proper spacing in f-string format specifications

3. **Enhanced Audio Device Initialization**
   - Added try-except handling for `pygame.mixer.init()`
   - Falls back to dummy audio driver when no audio device is available
   - Displays warning messages to users when audio initialization fails
   - Allows application to run in headless/cloud environments

### Project Structure
```
MusicPlay/
├── music_player.py              # Main application entry point
├── modules/
│   ├── local_music_manager.py   # Local music file management
│   └── online_music_manager.py  # Online music search and download
├── requirements.txt             # Python dependencies
├── config.json                  # User configuration (created on first run)
├── test_modules.py             # Module unit tests
├── .gitignore                  # Git ignore patterns
├── README.md                   # User documentation
└── DEVELOPMENT.md              # This file

```

## Testing

### Module Tests
Run the included test script to verify all modules work correctly:

```bash
python test_modules.py
```

This will test:
- Local music manager functionality
- Online music manager functionality
- File format detection
- Filename sanitization
- Mock music search

### Manual Testing
1. Start the application:
   ```bash
   python music_player.py
   ```

2. Test local music features:
   - Click "选择音乐文件夹" to select a folder with music files
   - Double-click a song to play it
   - Test playback controls (play, pause, next, previous)
   - Test volume control
   - Test repeat and shuffle modes

3. Test online music features:
   - Switch to "在线音乐" tab
   - Enter a search term and click "搜索"
   - Select a result and click "下载选中音乐"
   - Choose a download location

## Known Limitations

1. **Audio Device**: In cloud/headless environments without audio hardware, the application uses a dummy audio driver. Actual audio playback will not work, but the application will run without crashing.

2. **Online Music API**: The current implementation uses mock/demo data. To use real music APIs:
   - Update `modules/online_music_manager.py`
   - Replace the `_search_music_demo()` method with actual API calls
   - Ensure compliance with music licensing and copyright laws

3. **Audio Metadata**: Currently extracts basic info from filenames. For better metadata support:
   - Install `mutagen` library: `pip install mutagen`
   - Update `local_music_manager.py` to use mutagen for ID3 tag parsing

## Code Style

The project follows PEP 8 style guidelines with some minor deviations:
- Maximum line length: 79 characters (some violations exist)
- Indentation: 4 spaces
- Encoding: UTF-8

To check code style:
```bash
# Install flake8 if not already installed
pip install flake8

# Check code style
flake8 music_player.py modules/
```

## Future Enhancements

1. **Playlist Management**
   - Save and load custom playlists
   - Create playlists from search results

2. **Audio Visualization**
   - Add frequency spectrum visualization
   - Waveform display

3. **Equalizer**
   - Implement audio equalization controls
   - Preset equalizer settings

4. **Theme Support**
   - Dark mode
   - Custom color schemes

5. **Keyboard Shortcuts**
   - Global hotkeys for playback control
   - Media key support

6. **Real Music API Integration**
   - Integrate with Spotify, YouTube Music, or other legal APIs
   - Proper authentication and authorization

## Contributing

When contributing to this project:

1. Run tests before committing:
   ```bash
   python test_modules.py
   ```

2. Check for common issues:
   ```bash
   flake8 --select=E,W,F music_player.py modules/
   ```

3. Test in both normal and headless environments

4. Update documentation as needed

## Dependencies

- **pygame 2.5.2**: Audio playback and mixing
- **requests 2.31.0**: HTTP requests for online features
- **tkinter**: GUI framework (included with Python)

Optional:
- **mutagen**: Audio metadata parsing (recommended for better file info)
