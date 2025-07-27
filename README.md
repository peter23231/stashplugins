# Stash CommunityScripts Repository

This repository contains plugins, themes, userscripts, and utility scripts for StashApp, following the CommunityScripts structure.

## Index
The plugin index is built using `build_site.sh` and published as `index.yml` for plugin manager installation. Add your plugin YAML to the `plugins/` folder and run the build script to update the index. [See it here](https://peter23231.github.io/stashplugins/stable/index.yml)

## Example Plugin: Subtitle Extractor
Extracts embedded subtitles from video files during scan and via retroactive tasks. Subtitles are saved as SRT or VTT files using the naming convention:

    {scene_file_name}.{language_code}.ext
    {scene_file_name}.ext

Where `language_code` is ISO-639-1 (2 letters) and `ext` is the file extension (srt or vtt).
