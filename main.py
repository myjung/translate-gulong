import pathlib
import logging
import zipfile
import os
from datetime import datetime

# pypi packages
import toml
import argparse

# custom packages
from gulongpatcher.extractor import GulongMetaInfo, GulongPatcher, PatchHelper


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Translate Gulong CLI")

    # Add the arguments
    parser.add_argument("-b", "--backup", action="store_true", help="Extract files")
    parser.add_argument("-e", "--extract", action="store_true", help="Extract Keywords")
    parser.add_argument("-p", "--patch", action="store_true", help="Make patch")

    # Parse the command-line arguments
    args = parser.parse_args()
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()],
    )

    setting_path = pathlib.Path("localconfig.toml")
    gulong_patcher = GulongPatcher(pathlib.Path("./extracted_assets/config"))
    patch_helper = PatchHelper(GulongMetaInfo, gulong_patcher)
    if args.backup:
        # Extract config files
        GulongPatcher.backup_asset(setting_path)

    if args.extract:
        # Extract keywords
        patch_helper.extract_every_keywords_to_file("./data/extracted_strings.csv")

    if args.patch:
        # Make patch
        patch_helper.patch("./data/translated.csv", "./build/config")
        current_time = datetime.now().strftime("%y%m%d%H%M")
        zipf = zipfile.ZipFile(f"GulongPatch{current_time}.zip", "w", zipfile.ZIP_DEFLATED)
        zipf.write("readme-patchInfo.txt")

        # ./build 경로의 모든 파일을 /古龙风云录/AssetBundles/ 경로에 추가
        for root, dirs, files in os.walk("./build"):
            for file in files:
                # 파일의 전체 경로를 가져옵니다
                full_path = os.path.join(root, file)
                # zip 파일 내의 경로를 설정합니다
                in_zip_path = os.path.join("古龙风云录/AssetBundles", os.path.relpath(full_path, "./build"))
                # 파일을 zip 파일에 추가합니다
                zipf.write(full_path, in_zip_path)

        # zip 파일을 닫습니다
        zipf.close()
    if not args.backup and not args.extract and not args.patch:
        parser.print_help()


if __name__ == "__main__":
    main()
