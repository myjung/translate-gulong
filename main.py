import pathlib
import logging

# pypi packages
import toml

# custom packages
from gulongpatcher.extractor import GulongMetaInfo, GulongPatcher, PatchHelper

if __name__ == "__main__":
    setting_path = pathlib.Path("localconfig.toml")
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()],
    )
    # 스트링 추출
    gulong_patcher = GulongPatcher(setting_path)
    patch_helper = PatchHelper(GulongMetaInfo, gulong_patcher)
    # patch_helper.extract_every_keywords_to_file("./data/all_strings.csv")
    
    # 스트링 교체
    patch_helper.patch("./data/translated.csv", "./build/config")
