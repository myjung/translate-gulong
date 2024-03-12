# 고룡풍운록 한글화 프로젝트
본 프로젝트의 목적은 하락공작실의 게임 고룡풍운록(古龍風雲錄)을 한글화하는 것입니다. 네이버 카페 소요객잔(https://cafe.naver.com/beemu) 회원들의 자발적인 지원을 받았습니다.

## 프로젝트 환경설정
```bash
pip install -r requirements.txt
# 만약 openai를 번역 백엔드로 사용할 경우 openai, titoken을 추가 설치
pip install openai titoken
```
## 프로젝트 구조
/build/ : 최종적으로 패치가 완료된 결과물

/data/ : 게임과 관련된 각 데이터들이 들어있는 폴더

/gulongpatcher : 구룡풍운록 번역에 사용할 파이썬 패키지

/sampleconfig.toml : 패치 구동환경에 따른 로컬 설정 샘플

## 패치 방식
1. 고룡풍운록의 config 패키지의 내부 텍스트를 전부 추출
2. AI와 각종 사람이 번역한 텍스트 테이블 제작
3. 2번 데이터의 id,텍스트를 기준으로 게임 내 텍스트 교체

config 파일을 교체하면 게임 내 텍스트가 한글로 출력됩니다.


## 추가로 구현이 필요한 부분
ui 패키지에 font파일을 추가 삽입하거나 본 게임을 후킹하여 폰트를 변경하는 작업을 수행해야 합니다. 고룡풍운록의 대화 텍스트등은 TMP(Text mesh pro)를 사용하여 한자와 아스키 문자 외 글자가 표시 되지 않습니다.

## 번역 정보
Papago 무료버전, Papago 유료버전(용어집 사용 가능), GPT API 세가지를 사용했습니다. 다음 패치제공시 Claude를 사용하도록 변경할 계획입니다.

https://docs.google.com/spreadsheets/d/1YMTLtGJsH9q6_FW-r24AnhjLsstFIhxHWPf2JEjgK_Q

구글 시트에서 오역 제보가 가능합니다.

## 고룡풍운록의 데이터 구조
고룡풍운록은 유니티 2020.1.6 버전으로 개발되었으며 게임 루트폴더 하위에 있는 AssetBundles 폴더에 있는 패키지 파일들에 번역할 데이터가 있습니다. 중요한 파일은 config, ui 패키지입니다.
- /AssetBundles/config 에는 textasset으로 게임 내부 텍스트들이 저장되어 있으며 간체와 번체 텍스트가 들어 있습니다. 
- config file내에는 전투 목표 및 패배 조건이 기록되어 있는 json 파일들이 있으며 이는 따로 처리해야 합니다.
- json이 아닌 텍스트들은 주석을 포함할 수 있으며 tab으로 구분된 CSV로 모두 Id필드가 존재합니다.
- /AssetBundles/ui 에는 게임 내 출력될 이미지들과 폰트가 들어 있습니다.
- /GuLong_Data/StreamingAssets 에는 게임 내에 출력되는 영상들이 들어가 있습니다.

코드 내에는 번역할 텍스트 정의가 포함되어 있습니다. 
```Python
    battle_field = ("WinCondition", "LoseCondition", "SecondaryCondition") # 전장 목표
    achivement = PatchAsset("achievementitem", ("Name", "Description")) # 업적
    album = PatchAsset("albumitem", ("Name",)) # 앨범
    avatar = PatchAsset("avataritem", ("WorldTitle", "Surname", "Name", "Description")) # 인물 이름 및 별호, 묘사
    bene_buff = PatchAsset("benevolencebuffitem", ("Name", "Effect")) # 인의장 버프
    bene_village_build = PatchAsset(
        "benevolencevillagebuilditem",
        ("Name", "Description", "Direction1Name", "Direction2Name", "Direction3Name", "Direction4Name"),
    ) # 인의장 건설
    bene_village_enhance = PatchAsset("benevolencevillageenhanceitem", ("EnhanceName", "Description")) # 인의장 건설 업그레이드
    buffer = PatchAsset("bufferitem", ("Name", "Desc")) # 이펙트
    buff_string_table = PatchAsset("buffstringtable", ("Text",)) # 이펙트에 나오는 효과 설명
    relationship = PatchAsset("characterbloodrelationship", ("NameText", "NameBrief")) # 인물 관계도
    character_trait = PatchAsset("charactertraititem", ("Name",)) # 인물 특성
    clue = PatchAsset("clueitem", ("Title", "Description")) # 단서
    conspiracy = PatchAsset("conspiracyitem", ("Title", "EventBrief", "EventTip", "EventEffect")) # 밀모 이벤트
    crafting_formula = PatchAsset("craftingformulaitem", ("Name", "Story")) # 제조공식
    detective_stage_info = PatchAsset(
        "detectivestageinfoitem",
        ("SlotText", "Failure", "ConclusionHint", "InferenceHint", "CompositeHint", "ClueHint", "RepeatedHint"),
    ) # 추리
    dispatch_worker = PatchAsset("dispatchworkeritem", ("Name", "Content", "RewardText")) # 장객 파견
    equipment = PatchAsset("equipment", ("Name", "Story")) # 장비
    event_cube = PatchAsset("eventcubeitem", ("Name",)) # 이벤트 발생 트리거의 이름
    exercise = PatchAsset("exerciseitem", ("Name",)) # 연마
    forging = PatchAsset("forgingitem", ("Name",)) # 단조
    gang = PatchAsset("gangitem", ("Name", "Description")) # 적 정보
    gift = PatchAsset("giftitem", ("Name", "Story")) # 선물
    harvest_point = PatchAsset("harvestpoint", ("Name",)) # 대지도 채집
    harvest_point_item = PatchAsset("harvestpointitem", ("Name",)) # 채집장소 이름
    help_title = PatchAsset("helpitem", ("Name",)) # 인게임 도움말 제목
    historical_event = PatchAsset("historicaleventitem", ("Name", "Description")) # 역사 이벤트
    inference = PatchAsset("inferenceitem", ("Title", "Description", "Murmur")) # 추론
    invensify = PatchAsset("invensifyitem", ("ItemName", "Desc"))
    manor_buff = PatchAsset("manorbuffitem", ("Name", "Description")) # 분위기 효과
    manor_crafting_blueprint = PatchAsset("manorcraftingblueprintitem", ("Name", "Description")) # 제조법
    map_debuff = PatchAsset("mapdebuffitem", ("Name", "Description")) # 맵 디버프 효과
    mini_map = PatchAsset("minimapitem", ("Name",)) # 미니맵
    mosaic = PatchAsset("mosaicitem", ("Name", "Story")) # 투로물(쉬화, 제련 용) 아이템
    inventory = PatchAsset("normalinventoryitem", ("Name", "Story")) # 행낭 물품
    npc = PatchAsset("npcitem", ("LevelUpDialog",)) # npc 정보
    dialogue = PatchAsset("npctalkitem", ("Content",)) # 가장 중요한 모든 게임 내 대화 스크립트
    perception_effect_group = PatchAsset("perceptioneffectgroupitem", ("Name",)) # 감오
    perception_point = PatchAsset("perceptionpointitem", ("Name",)) # 감오점
    quest = PatchAsset("questitem", ("QuestName", "QuestBrief")) # 임무, 소문
    shop = PatchAsset("shopitem", ("Name", "Dialog")) # 상점
    skill = PatchAsset("skillitem", ("Name", "Description")) # 무공
    small_map_location = PatchAsset("smallmaplocationitem", ("LocationName",)) # 소지도
    smelt = PatchAsset("smeltitem", ("Name",)) # 제련 아이템
    string_table = PatchAsset("stringtable", ("Text",)) # 인게임 ui 텍스트
    transfer = PatchAsset("transferitem", ("MapWord", "ToMapWord")) # 지도 내 이동지점 텍스트
    trick_card = PatchAsset("trickcarditem", ("Name", "Description")) # 도감
    village = PatchAsset("villageitem", ("Name", "Description")) # 대지도 위치
    wanted = PatchAsset("wanteditem", ("Description",)) # 현상방
```

# Special Thanks
소요객잔(https://cafe.naver.com/beemu) 대협들의 지원을 받았습니다.

무명대협들께서 지원해주신 금액은 모두 번역의 퀄리티를 향상시키기 위해 사용될 것입니다.