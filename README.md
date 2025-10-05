# chart-downloader
Download PJSK charts from Sonolus and sekai.best (official)

# Outputs
The output will always be an editor-compatible score file type.

Here are the list of possible files:
- NSLevelData.json.gz [next-sekai](https://next-sekai-editor.sonolus.com/)
- .usc [MMW4CC](https://github.com/sevenc-nanashi/MikuMikuWorld4CC) [next-sekai](https://next-sekai-editor.sonolus.com/)
- .sus [MMW](https://github.com/crash5band/MikuMikuWorld) [MMW YarNix Fork](https://github.com/YarNix/MikuMikuWorld) [MMW4CC](https://github.com/sevenc-nanashi/MikuMikuWorld4CC)

There are other types of LevelData, but they are not openable in editors.

Additionally, the downloader will export the audio, jacket, and preview files for the level (if exists). We attempt to automatically determine the file type, however if there is no extension, we did not detect it.