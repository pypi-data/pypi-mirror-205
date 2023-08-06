import json
import shutil
from pathlib import Path

import hydra
import requests
from loguru import logger
from omegaconf import DictConfig
from yt_dlp import YoutubeDL


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    output_path = Path(cfg.scraper.output_folder)
    output_path.mkdir(exist_ok=True)
    tmp_path = output_path / 'tmp'

    urls_path = Path(cfg.search.output_folder) / cfg.search.result_file
    with open(urls_path) as f:
        urls = list(dict.fromkeys(s.strip() for s in f.readlines()))

    ydl_opts = {
        # 'subtitleslangs': ['ru'],
        # 'writesubtitles': True,
        'chapter': True,
        'format': 'm4a/bestaudio/best',
        # 'postprocessors': [{  # Extract audio using ffmpeg
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'm4a',
        # }]
        'paths': dict(home=str(tmp_path)),
        'outtmpl': 'audio.%(ext)s'
    }
    with YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            if tmp_path.exists():
                shutil.rmtree(tmp_path)
            tmp_path.mkdir()

            video_info = ydl.extract_info(url, download=False)
            video_id = video_info['id']
            path = output_path / video_id
            if path.exists():
                logger.warning(f'Video {video_info.get("id")} downloaded. Skipping.')
                continue

            chapters = video_info['chapters']
            auto_subs = True
            if video_info.get('subtitles') is None or video_info.get('subtitles').get('ru') is None:
                subs_data = video_info['automatic_captions']['ru-orig']
            else:
                subs_data = video_info['subtitles']['ru']
                auto_subs = False

            try:
                subs_link = [s for s in subs_data if s['ext'] == 'json3'][0]['url']
            except IndexError:
                logger.error(f'Incorrect subs type: {video_id}')
                continue

            summary = dict(
                auto_subs=auto_subs,
                id=video_info['id'],
                title=video_info['title'],
                description=video_info['description'],
                url=video_info['webpage_url'],
                categories=video_info['categories'],
                tags=video_info['tags'],
                date=video_info['upload_date'],
                duration=video_info['duration_string'],
                chapters=chapters,
            )
            json.dump(summary, open(tmp_path / 'info.json', 'w', encoding='utf8'), ensure_ascii=False, indent=2)

            subs = requests.get(subs_link).json()
            json.dump(subs, open(tmp_path / 'subs.json', 'w', encoding='utf8'), ensure_ascii=False)

            ydl.download(url)

            shutil.move(tmp_path, path)


if __name__ == '__main__':
    main()
