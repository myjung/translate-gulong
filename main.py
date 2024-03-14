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
    GulongPatcher.backup_asset(setting_path)
    gulong_patcher = GulongPatcher(pathlib.Path("./extracted_assets/config"))
    patch_helper = PatchHelper(GulongMetaInfo, gulong_patcher)
    # patch_helper.extract_every_keywords_to_file("./data/extracted_strings.csv")
    
    # 스트링 교체
    patch_helper.patch("./data/translated.csv", "./build/config")
