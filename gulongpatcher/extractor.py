from dataclasses import dataclass
from io import StringIO
import toml as tomllib
import hashlib
import pathlib
import json
import os
import csv
from shutil import copyfile

import UnityPy
from UnityPy.enums import ClassIDType


@dataclass
class PatchAsset:
    asset_name: str
    fields: tuple[str]

    def __str__(self):
        return f"{self.asset_name} : {self.fields}"


@dataclass
class GulongMetaInfo:
    config_path = pathlib.PurePosixPath("assets/config")
    ui_path = pathlib.PurePosixPath("assets/ui")
    textfiles = config_path.joinpath("textfiles")
    battle = config_path.joinpath("battle", "area")
    battle_sc = config_path.joinpath("battle", "area(sc)")
    textfiles_sc = config_path.joinpath("textfiles(sc)")
    battle_field = ("WinCondition", "LoseCondition", "SecondaryCondition")
    achivement = PatchAsset("achievementitem", ("Name", "Description"))
    album = PatchAsset("albumitem", ("Name",))
    avatar = PatchAsset("avataritem", ("WorldTitle", "Surname", "Name", "Description"))
    bene_buff = PatchAsset("benevolencebuffitem", ("Name", "Effect"))
    bene_village_build = PatchAsset(
        "benevolencevillagebuilditem",
        ("Name", "Description", "Direction1Name", "Direction2Name", "Direction3Name", "Direction4Name"),
    )
    bene_village_enhance = PatchAsset("benevolencevillageenhanceitem", ("EnhanceName", "Description"))
    buffer = PatchAsset("bufferitem", ("Name", "Desc"))
    buff_string_table = PatchAsset("buffstringtable", ("Text",))
    relationship = PatchAsset("characterbloodrelationship", ("NameText", "NameBrief"))
    character_trait = PatchAsset("charactertraititem", ("Name",))
    clue = PatchAsset("clueitem", ("Title", "Description"))
    conspiracy = PatchAsset("conspiracyitem", ("Title", "EventBrief", "EventTip", "EventEffect"))
    crafting_formula = PatchAsset("craftingformulaitem", ("Name", "Story"))
    detective_stage_info = PatchAsset(
        "detectivestageinfoitem",
        ("SlotText", "Failure", "ConclusionHint", "InferenceHint", "CompositeHint", "ClueHint", "RepeatedHint"),
    )
    dispatch_worker = PatchAsset("dispatchworkeritem", ("Name", "Content", "RewardText"))
    equipment = PatchAsset("equipment", ("Name", "Story"))
    event_cube = PatchAsset("eventcubeitem", ("Name",))
    exercise = PatchAsset("exerciseitem", ("Name",))
    forging = PatchAsset("forgingitem", ("Name",))
    gang = PatchAsset("gangitem", ("Name", "Description"))
    gift = PatchAsset("giftitem", ("Name", "Story"))
    harvest_point = PatchAsset("harvestpoint", ("Name",))
    harvest_point_item = PatchAsset("harvestpointitem", ("Name",))
    help_title = PatchAsset("helpitem", ("Name",))
    historical_event = PatchAsset("historicaleventitem", ("Name", "Description"))
    # illustration = PatchAsset("illustrationitem", ("Name",))
    inference = PatchAsset("inferenceitem", ("Title", "Description", "Murmur"))
    invensify = PatchAsset("invensifyitem", ("ItemName", "Desc"))
    manor_buff = PatchAsset("manorbuffitem", ("Name", "Description"))
    manor_crafting_blueprint = PatchAsset("manorcraftingblueprintitem", ("Name", "Description"))
    map_debuff = PatchAsset("mapdebuffitem", ("Name", "Description"))
    mini_map = PatchAsset("minimapitem", ("Name",))
    mosaic = PatchAsset("mosaicitem", ("Name", "Story"))
    inventory = PatchAsset("normalinventoryitem", ("Name", "Story"))
    npc = PatchAsset("npcitem", ("LevelUpDialog",))
    dialogue = PatchAsset("npctalkitem", ("Content",))
    perception_effect_group = PatchAsset("perceptioneffectgroupitem", ("Name",))
    perception_point = PatchAsset("perceptionpointitem", ("Name",))
    quest = PatchAsset("questitem", ("QuestName", "QuestBrief"))
    shop = PatchAsset("shopitem", ("Name", "Dialog"))
    skill = PatchAsset("skillitem", ("Name", "Description"))
    small_map_location = PatchAsset("smallmaplocationitem", ("LocationName",))
    smelt = PatchAsset("smeltitem", ("Name",))
    string_table = PatchAsset("stringtable", ("Text",))
    transfer = PatchAsset("transferitem", ("MapWord", "ToMapWord"))
    trick_card = PatchAsset("trickcarditem", ("Name", "Description"))
    village = PatchAsset("villageitem", ("Name", "Description"))
    wanted = PatchAsset("wanteditem", ("Description",))
    targets = (
        achivement,
        album,
        avatar,
        bene_buff,
        bene_village_build,
        bene_village_enhance,
        buffer,
        buff_string_table,
        relationship,
        character_trait,
        clue,
        conspiracy,
        crafting_formula,
        detective_stage_info,
        dispatch_worker,
        equipment,
        event_cube,
        exercise,
        forging,
        gang,
        gift,
        harvest_point,
        harvest_point_item,
        help_title,
        historical_event,
        inference,
        invensify,
        manor_buff,
        manor_crafting_blueprint,
        map_debuff,
        mini_map,
        mosaic,
        inventory,
        npc,
        dialogue,
        perception_effect_group,
        perception_point,
        quest,
        shop,
        skill,
        small_map_location,
        smelt,
        string_table,
        transfer,
        trick_card,
        village,
        wanted,
    )
    for target in targets:
        target.path = str(textfiles.joinpath(f"{target.asset_name}.txt"))
        target.sc_path = str(textfiles_sc.joinpath(f"{target.asset_name}.txt"))
    conatiner_paths = tuple(target.path for target in targets)
    sc_conatiner_paths = tuple(target.sc_path for target in targets)


class GulongPatcher:
    @staticmethod
    def backup_asset(setting_path: pathlib.Path, target_path=pathlib.Path("./extracted_assets")) -> None:
        settings = tomllib.load(setting_path)["local"]
        GULONG_PATH = pathlib.Path(settings["GULONG_PATH"])
        assetbundle_path = GULONG_PATH.joinpath("AssetBundles")
        config = assetbundle_path.joinpath("config")
        copyfile(config, target_path.joinpath("config"))


    def __init__(self, config_path:pathlib.Path) -> None:
        self.env = UnityPy.load(str(config_path))


    def get_text(self, path: pathlib.Path | str) -> str:
        asset = self.env.container[path]
        t = ""
        if not asset.type == ClassIDType.TextAsset:
            raise Exception("Not Text Asset")
        try:
            t = asset.read().text
        except UnicodeDecodeError:
            t = bytes(asset.read().script).decode("big5hkscs")
        if t[:1] == "\ufeff":
            return t[1:]
        else:
            return t

    def set_text(self, path: pathlib.Path | str, text: str) -> None:
        asset = self.env.container[path]
        if not asset.type == ClassIDType.TextAsset:
            raise Exception("Not Text Asset")
        data = asset.read()
        data.script = text.encode("utf-8")
        data.save()

    def save_asset(self, path: str) -> None:
        print(f"try to save {path}")
        with open(path, mode="wb") as f:
            f.write(self.env.file.save())

    def get_battle_text(self, path: pathlib.PurePath) -> list:
        output = []
        for key in self.env.container:
            if pathlib.PurePosixPath(key).parent == path:
                output.append(key)
        return output


class CustomCsvDict:

    def __init__(self, csv_text: str) -> None:
        self.csv = self.heoluo_string_csv_parser(csv_text)

    @staticmethod
    def heoluo_string_csv_parser(text: str) -> list[dict[str, str]]:
        output = list()
        headers = None
        for line in text.split("\n"):
            if line.endswith("\r"):
                line = line[:-1]
            if line.startswith("#"):
                print("comment find")
                print(line)
                continue
            if not headers:
                headers = line.split("\t")
                continue
            if line == "":
                continue
            output.append(dict(zip(headers, line.split("\t"))))
        return output

    def to_csv_string(self) -> str:
        headers = self.csv[0].keys()
        output = StringIO()
        output.write("\t".join(headers))
        output.write("\r\n")
        for row in self.csv:
            output.write("\t".join(row.values()))
            output.write("\r\n")
        return output.getvalue()

    def __getitem__(self, key: str) -> dict[str, str]:
        return self.csv[key]


def translated_string_loader(path: pathlib.Path | str) -> dict:
    retvar = dict()
    with open(path, mode="r", encoding="utf-8") as f:
        f.readline()
        for line in f:
            if line.startswith("#"):
                continue
            if line.endswith("\r"):
                line = line[:-1]
            if line == "":
                continue
            if line.strip() == "":
                continue
            line = line.split("\t")
            finder = line[4]
            korean = line[5].rstrip().replace("\\\\n", "\n").replace("\\\\r", "\r").replace("\\\\t", "\t")
            retvar[finder] = korean
        return retvar


class PatchHelper:

    def __init__(self, patch_target: GulongMetaInfo, patcher: GulongPatcher) -> None:

        self.patch_target = patch_target
        self.patcher = patcher

    def remove_duplicate_keywords_and_save(self, file_name: str):
        duplicate_remove_texts = dict()
        with open(file_name, mode="w", encoding="utf-8") as f:
            for k in self.extract_keywords():
                duplicate_remove_texts.setdefault(k[2], 0)
                duplicate_remove_texts[k[2]] += 1
            # duplicate_remove_texts = {k[2]:"" for k in self.extract_keywords()}
            for keyword, count in duplicate_remove_texts.items():
                f.write(f"{keyword}")
                f.write("\n")

    def get_proper_noun_keywords_and_save(self, file_name: str):
        duplicate_remove_texts = dict()
        with open(file_name, mode="w", encoding="utf-8") as f:
            for k in self.extract_keywords():
                duplicate_remove_texts.setdefault(k[2], 0)
                duplicate_remove_texts[k[2]] += 1
            for keyword, count in duplicate_remove_texts.items():
                f.write(f"{keyword}")
                f.write("\n")

    def extract_every_keywords_to_file(self, file_name: str):
        def escape_str(s: str) -> str:
            return s.replace("\n", "\\\\n").replace("\r", "\\\\r").replace("\t", "\\\\t")

        with open(file_name, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(["asset_name", "id", "field", "content"])
            for target in GulongMetaInfo.targets:
                print(f"load {target.asset_name} : {target.path}")
                csv_instance = CustomCsvDict(self.patcher.get_text(target.path))
                for row in csv_instance.csv:
                    for field in target.fields:
                        if value := row[field].strip():
                            writer.writerow([target.asset_name, row["Id"], field, escape_str(value)])

            for battle_target in self.patcher.get_battle_text(self.patch_target.battle):
                if battle_target.endswith(".json"):
                    print(f"load {battle_target}")
                    battle_dict = json.loads(self.patcher.get_text(battle_target))
                    for field in self.patch_target.battle_field:
                        if value := battle_dict.get(field, ""):
                            writer.writerow(
                                [
                                    "battleCondition",
                                    battle_target,
                                    field,
                                    escape_str(value),
                                ]
                            )

    def patch(self, input_keywords_path: str, output_path: str):
        keyword_dictionary = translated_string_loader(input_keywords_path)
        for target in GulongMetaInfo.targets:
            print(target.asset_name, "Common String Replacer Start")
            str_csv = self.patcher.get_text(target.path)
            csv_dict = CustomCsvDict(str_csv)
            for row in csv_dict:
                for field in target.fields:
                    finder = f"{target.asset_name}{row['Id']}{field}{row[field]}"
                    if finder in keyword_dictionary:
                        row[field] = keyword_dictionary[finder]
            self.patcher.set_text(target.path, csv_dict.to_csv_string())
            print(target.asset_name, "Done")
        for battle_target in self.patcher.get_battle_text(self.patch_target.battle):
            if battle_target.endswith(".json"):
                print(battle_target, "Battle condtion String Replacer Start")
                battle_dict = json.loads(self.patcher.get_text(battle_target))
                for field in self.patch_target.battle_field:
                    if not field in battle_dict:
                        continue
                    finder = f"battleCondition{battle_target}{field}{battle_dict[field]}"
                    if finder in keyword_dictionary:
                        battle_dict[field] = keyword_dictionary[finder]
                self.patcher.set_text(battle_target, json.dumps(battle_dict, ensure_ascii=False))
                print(battle_target, "Done")

        self.patcher.save_asset(output_path)


if __name__ == "__main__":
    current_file_path = pathlib.Path(__file__)
    local_config_path = current_file_path.parent.joinpath("..", "localconfig.toml")
    patcher = GulongPatcher(local_config_path)
    # ph = PatchHelper(PatchTargets, patcher)
    # ph.patch("translated2403082200.csv","config")
    # ph.extract_every_keywords_to_file("2403082000.csv")
