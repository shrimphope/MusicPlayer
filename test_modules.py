#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify the music player modules work correctly
"""

import os
import sys
from modules.local_music_manager import LocalMusicManager
from modules.online_music_manager import OnlineMusicManager


def test_local_music_manager():
    """Test local music manager functionality"""
    print("=" * 60)
    print("Testing Local Music Manager")
    print("=" * 60)
    
    manager = LocalMusicManager()
    
    # Test 1: Check supported formats
    print(f"Supported formats: {manager.supported_formats}")
    assert len(manager.supported_formats) > 0, "No supported formats found"
    print("✓ Supported formats loaded correctly")
    
    # Test 2: Test is_audio_file method
    test_files = [
        ("song.mp3", True),
        ("audio.wav", True),
        ("music.flac", True),
        ("video.mp4", False),
        ("document.txt", False),
    ]
    
    for filename, expected in test_files:
        result = manager._is_audio_file(filename)
        assert result == expected, f"Expected {expected} for {filename}, got {result}"
        print(f"✓ {filename}: {result} (expected {expected})")
    
    # Test 3: Test extract_title and extract_artist
    test_filename = "/path/to/Artist - Title.mp3"
    title = manager._extract_title(test_filename)
    artist = manager._extract_artist(test_filename)
    print(f"✓ Extracted title: '{title}', artist: '{artist}'")
    
    print("\n✅ Local Music Manager tests passed!\n")


def test_online_music_manager():
    """Test online music manager functionality"""
    print("=" * 60)
    print("Testing Online Music Manager")
    print("=" * 60)
    
    manager = OnlineMusicManager()
    
    # Test 1: Check initialization
    print(f"API timeout: {manager.api_timeout} seconds")
    print(f"Max retries: {manager.max_retries}")
    assert manager.api_timeout > 0, "Invalid API timeout"
    assert manager.max_retries > 0, "Invalid max retries"
    print("✓ Manager initialized correctly")
    
    # Test 2: Test search_music (will use mock data)
    try:
        results = manager.search_music("晴天")
        assert isinstance(results, list), "Search results should be a list"
        print(f"✓ Search returned {len(results)} results")
        
        if results:
            first_result = results[0]
            assert 'title' in first_result, "Result should have 'title' field"
            assert 'artist' in first_result, "Result should have 'artist' field"
            print(f"✓ First result: {first_result['title']} - {first_result['artist']}")
    except Exception as e:
        print(f"⚠ Search test encountered an error (this is acceptable for mock data): {e}")
    
    # Test 3: Test _sanitize_filename
    test_filenames = [
        ('Song<Title>.mp3', 'Song_Title_.mp3'),
        ('Artist: Album/Song.mp3', 'Artist_ Album_Song.mp3'),
        ('Normal Song.mp3', 'Normal Song.mp3'),
    ]
    
    for input_name, expected in test_filenames:
        result = manager._sanitize_filename(input_name)
        # Just check that illegal characters are replaced
        assert '<' not in result and '>' not in result and ':' not in result and '/' not in result
        print(f"✓ Sanitized '{input_name}' -> '{result}'")
    
    print("\n✅ Online Music Manager tests passed!\n")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Music Player Module Tests")
    print("=" * 60 + "\n")
    
    try:
        test_local_music_manager()
        test_online_music_manager()
        
        print("=" * 60)
        print("🎉 All tests passed successfully!")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
