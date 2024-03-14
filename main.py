import pathlib
import logging
import zipfile
import os
from datetime import datetime
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

    # patch_helper = PatchHelper(GulongMetaInfo, gulong_patcher)
    # 키워드 추출
    # patch_helper.extract_every_keywords_to_file("./data/extracted_strings.csv")
    
    # 스트링 교체
    # patch_helper.patch("./data/translated.csv", "./build/config")
    # readme 파일을 zip 파일의 루트에 추가
    current_time = datetime.now().strftime("%y%m%d%H%M")
    zipf = zipfile.ZipFile(f'GulongPatch{current_time}.zip', 'w', zipfile.ZIP_DEFLATED)
    zipf.write('readme-patchInfo.txt')

    # ./build 경로의 모든 파일을 /古龙风云录/AssetBundles/ 경로에 추가
    for root, dirs, files in os.walk('./build'):
        for file in files:
            # 파일의 전체 경로를 가져옵니다
            full_path = os.path.join(root, file)
            # zip 파일 내의 경로를 설정합니다
            in_zip_path = os.path.join('古龙风云录/AssetBundles', os.path.relpath(full_path, './build'))
            # 파일을 zip 파일에 추가합니다
            zipf.write(full_path, in_zip_path)

    # zip 파일을 닫습니다
    zipf.close()