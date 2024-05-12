from pathlib import Path

def choose_file_path_video():
    download_path_video = str(Path.home() / "Downloads/Youtube_Downloader/Video")
    return download_path_video

def choose_file_path_audio():
    download_path_audio = str(Path.home()/ "Downloads/Youtube_Downloader/Audio")
    return download_path_audio
