from pathlib import Path
from typing import Any

import hydra
from loguru import logger
from omegaconf import DictConfig
from yt_dlp import YoutubeDL


def process(path: str, info: dict[str, Any]) -> None:
    if info.get('chapters') is None:
        return
    # if info.get('subtitles') is None or info.get('subtitles').get('ru') is None:
    #     return
    if info.get('automatic_captions').get('ru-orig') is None:
        return
    url = info.get('original_url')
    logger.info(f"Got url: {url}")
    with open(path, 'a') as f:
        f.write(f'{url}\r\n')


class Wrap(YoutubeDL):
    path: str

    def process_ie_result(self, ie_result, download=True, extra_info=None):
        if ie_result.get('_type', None) is None:
            process(self.path, ie_result)
        return super().process_ie_result(ie_result, download, extra_info)


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    ydl_opts = {
        'writesubtitles': True,
        'subtitleslangs': ['ru'],
        'chapter': True,
        'format': 'm4a/bestaudio/best/ru',
        'default_search': f'ytsearch{cfg.search.cnt}:{cfg.search.query}',
    }
    with Wrap(ydl_opts) as ydl:
        ydl.path = Path(cfg.search.output_folder)
        ydl.path.mkdir(exist_ok=True)
        ydl.path /= cfg.search.result_file
        ydl.extract_info('', download=False)


if __name__ == '__main__':
    main()
