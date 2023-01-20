# Pesonal GameDev Asset Tools

## Requirements
- Python 3.9 or above and nothing else: All of this is build on top of the stdlib

## Features so far
- Create sprite sheets using FFmpeg. Tested on Linux only but it should also work on Windows and Mac
- Recovers individual sprites (images) and sounds from a Game Maker Studio 2 project (tested only with GMS2 v2.2.5.481 projects). Recovery will also try and create a sprite sheet with FFmpeg but only if you're on Linux and have FFmpeg installed
