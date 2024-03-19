import json
import logging
import pathlib
import os
import concurrent.futures
import toml
import anthropic
import tqdm
from gulongpatcher.translator import Claude3Api

dialogue_keys = [
    "mg000028",
    "bs_01e03",
    "ml105001",
    "mh000006",
    "mg000054",
    "ma800001",
    "w2105027",
    "ma060007",
    "mg000003",
    "mg101001",
    "w0105006",
    "mh000009",
    "mi000001",
    "ma210001",
    "mg110002",
    "mq120013",
    "mq120007",
    "mg000044",
    "ma062904",
    "mc050020",
    "ma803003",
    "mc050070",
    "mh000011",
    "ma061302",
    "mc050008",
    "mq330004",
    "mq200010",
    "mn106001",
    "mq200009",
    "ma063801",
    "mq120002",
    "bc037001",
    "ma210010",
    "mf090021",
    "w2104000",
    "mq110001",
    "mq240001",
    "be050002",
    "mc050042",
    "mq180002",
    "ma063802",
    "mh000040",
    "mg090001",
    "mq070002",
    "mf000005",
    "mg010001",
    "mq000000",
    "w0105020",
    "mc050032",
    "w1105000",
    "mg000058",
    "mq120020",
    "mh060002",
    "mb066301",
]


def test_function():
    test_prompt = "이것은 테스트 프롬프트입니다. 제가 hello라고 하면 world라고 응답해주세요."
    test_first_return = "네, 이것은 테스트 프롬프트에 대한 첫 번째 응답입니다."
    test_text = "hello"
    api_key = toml.load("localconfig.toml")["local"]["CLAUDE_API_KEY"]
    claude = Claude3Api(api_key)
    claude_response = claude.translate(test_prompt, test_first_return, test_text)
    assert claude_response.content[0].text == "world"


def test_function2(api_key):
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=api_key,
    )
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1001,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": '당신은 중국어 무협 텍스트를 한국어로 번역하는 전문가입니다. 중국에서 제작된 무협 게임의 스크립트들을 한국어로 번역할 것입니다.\n제공될 텍스트는 고룡(古龍)작가의 무협 세계관을 기반으로 한 게임 고룡풍운록(古龍風雲錄)의 스크립트들입니다. 그의 특징적인 문체를 살리세요.\n게임 플롯 : 진우(辰雨)는 구주왕심천군(九州王沈天君)이 인의장(仁義莊)에 데려온 출신을 알 수 없는 서동(書童)이었습니다.\n전 장주였던 심천군은 형산(衡山) 회안봉(回雁峰)에 무적검전(無敵劍典)이 있다는 소문으로 벌어진 음모에 휘말려 죽었고 이후 십년이 지났습니다.\n최근 연남천(燕南天)의 장보도가 있다는 소문이 돌자 음모의 연관성을 의심한 냉이(冷二)가 그를 강호로 보내 사건을 조사하며 음모를 밝히는 내용의 RPG입니다.\n주인공 설정 : 진우(辰雨)는 한때 인의장의 그림자 같은 인물로, 감정이 메마르고 말이 적으며, 출신내력이 불명하다. 옛 장주의 유언에 따라 직무를 맡거나 장을 나가는 것, 손을 쓰면 안 된다는 규칙을 지켜왔다. 회안봉 사건 십년이 지나서야 강호에 발을 들였다.\n\n주요 등장인물 설정:\n심랑 : 심천군의 아들로 명가자제다운 품격과 소탈함이 있다. 예의가 바르고 남을 안심시킨다.\n\n주칠칠 : 주가 활재신의 영애로 아름답고 정의감이 뛰어난 당찬 여성이다.\n\n강소어 : 악인곡에서 십대악인에게 길러진 소년으로 장난이 심하고 자신감이 넘친다.\n\n초류향 : 답월류향의 경공으로 유명한 우아한 군자, 도적으로 알려져 있지만 정의롭고 사람을 해치지 않는다.\n\n이심환 : 소이비도로 유명하며 진사와 탐화를 여러번 배출한 유명한 가문의 후손이지만 십년전 명예를 버리고 은둔한 남자다. 현재 건강도 좋지 않아 기침을 많이 하지만 여전히 눈빛은 살아있는 대협이다.\n\n백비비 : 쾌활왕 시옥관에게 복수하고 싶어하는 아름다운 여성으로 사실 유령궁주의 신분을 숨기고 있다.\n\n금무망 : 금가의 장남으로 스스로 얼굴을 망가뜨리고 기관비술에 전념했다. 한 때 쾌활왕 측근 재사로 있었다.\n\n손소홍 : 손백발 노인의 손녀로 땋은 머리를 한 귀여운 소녀, 노래 대신 이야기를 하며 재주를 판다. 자신만의 이야기를 만들고 싶어한다.\n\n임선아 : 천하제일미녀\n\n왕련화 : 낙양의 지하성주이자 뛰어난 재능을 가진 남자로 배운 것이 많아 천면공자라고도 불린다. 선악을 알기 어려운 인물로 변장술에 능하다.\n\n육소봉 : 수염이 마치 눈썹같아 사조미모라 불리며 붉은 장포를 걸친 남자다. 지략이 뛰어나지만 말투가 신랄하고 무례하다. 하지만 천하에 친구가 많고 의리를 중시하는 쾌남이다.\n\n공손란 : 여성을 위한 여성만의 비밀조직 홍혜자의 수장으로 손속이 잔인하여 사람들이 두려워한다. 하지만 선녀처 아름다운 누님이다.\n\n소앵 : 차가워보이지만 총명하고 말을 잘하는 소녀다. 무공은 못하지만 지략이 뛰어나고 악인곡의 소마성 강소어의 천적이다.\n\n번역지침\n1. 높임말과 반말, 평서체를 구분해서 사용.\n- 존댓말: 부탁이나 공경의 표현에 사용. 예: "謹聽莊主之命！" → "장주님의 명에 따르겠습니다."\n- 반말: 도발적, 협박적, 고압적인 말투에 사용. 예: "軟柿子，受死吧！" → "나약한 놈, 죽어라!"\n- 평서체: 불확실한 상황이나 상황 설명에 사용. 예: "夾層中放了一張紙，寫著「揚瀾小鎮怪郎中」。" → "사이에 끼워진 종이에는, \'양란소진괴랑중(揚瀾小鎮怪郎中)\'이 적혀있다."\n- 위 지침에 어긋나더라도, 맥락을 고려했을 때 더 적합한 표현이 있다면 그것을 사용하세요.\n2. 태그와 플레이스홀더 유지.\n- "{}"안에 있는 내용은 그대로 두세요. 예: "這是{it2000_03}。" → "이것은 {it2000_03}이다."\n- "<>"안에 있는 내용도 번역하지 마세요. 예: "這<color=#FF0000>茶葉</color>你就拿去吧！" → "이 <color=#FF0000>찻잎</color>을 가져가!", "保護<b>{playerName}</b>!" → "<b>{playerName}</b>을/를 보호해!"\n- 태그와 플레이스 홀더는 게임엔진에서 출력될 때 변경되므로 오타나 변경이 있을 경우 게임이 멈출 수도 있습니다. 주의하세요!\n3. 무협세계관 유지.\n- 한글/한자어 사용: 영어에서 유래한 외래어 대신 한글/한자어 사용. 예: "桌子" → "탁자","藏寶圖" → "장보도", "公子" → "공자"\n- 무협지식 호칭에 주의. 예: "大俠" → "대협", "師兄" → "사형", "師姐" → "사저", "俠客" → "협객", "莊客" → "장객", "莊主" → "장주", "兄弟" → "형제", "大哥" → "대가", "哥哥" → "가가" ,"小弟" → "소제", "大爺" → "대야", "小爺" → "소야" 등\n4. 원문 표기.\n- 이름, 지명, 무공, 물건, 별명 등은 음차하고 원문을 병기하여 사용. 예: "辰雨" → "진우(辰雨)", "柴玉關" → "시옥관(柴玉關)", "我在地靈莊。" → "나는 지령장(地靈莊)에 있다.", "秘笈，正陽佛手。" → "비급, 정양불수(正陽佛手)", "這是……嵩陽鐵劍？" → "이건...숭양철검(嵩陽鐵劍)?"\n- 고사성어에서 유래된 표현 등은 뜻을 번역하고 원문을 병기하세요. 예: "漏了<color=#FF0000>果老騎驢</color>四個字。" → "<color=#FF0000>과로기려(果老騎驢:당나귀를 거꾸로 탄 노인)</color> 네 글자를 빠뜨렸다."\n- **최종적으로 번역된 결과물에서 병기된 원문은 검수자가 일괄 처리 할 수 있으므로 한자 병기 지침을 항상 준수**.\n5. 문법 및 표현의 자연스러움 재확인.\n잘 지켜진 예: "九年前……你──！你可是朱家的千金？" → "구년 전... 너는──! 혹시 주가의 천금(千金)인가?"\n잘못된 예(문법적으로 어색함):"九年前……你──！你可是朱家的千金？" → "아홉 해 전…… 너는──! 너 혹시 주가(朱家)의 따님인가?"\n6. 번역 중 의미가 모호한 경우 원문의 의도를 가장 잘 전달할 수 있는 표현 선택.\n7. 입력 json 데이터의 포맷 설명.\n- context: 스크립트 속 인물의 정보와 특정 텍스트를 번역하는 방법에 대한 정보 제공.\n예 : 천왕채무리의 정보: 성별은 Male이다.,"天王寨" → "천왕채"\n- talks: 연속된 대화내용이 각 대화의 id를 키값으로 하여 제공됨\n- talker: 발화자의 id, 필요한 경우 context를 통해 id가 누구인지 명시함\n- type: 대화의 종류. Narrator(내레이터), Dialogue(대화), Option(플레이어의 선택지) 등이 있음\n- content : 번역할 텍스트\n- next_talks: 다음 대화의 id 나열. Optional Field\n7. 출력 json 데이터의 포맷설명\n- summarize: 번역된 대화문의 짧은 요약.\n- notify_id: 번역 과정 중 발견된 문제가 있는 텍스트의 ID 나열.\n- content의 번역된 결과를 원본 id를 키로 하여 명시\n입력예 :\n{\n  "context": "벽화가 있는 동굴에 대한 이야기",\n  "talks": {\n   "0001": {\n    "talker": "Narrator",\n    "content": "幽山深谷靜<br>壁畫驚成謎。",\n    "type": "Narrator"\n   },\n   "0002": {\n    "talker": "Player",\n    "content": "此洞江湖人士眾多……",\n    "type": "Dialogue",\n    "next_talks": "0003,0004"\n   },\n   "0003": {\n    "talker": "Option",\n    "content": "進入參悟",\n    "type": "Option"\n   },\n   "0004": {\n    "talker": "Option",\n    "content": "暫且不入",\n    "type": "Option"\n   },\n   "0005": {\n    "conten": "#N/A"\n   },\n   "0006": {\n    "talker": "Narrator",\n    "content": "竟已領悟了壁畫上的{0}武功",\n    "type": "Narrator"\n   }\n  }\n}\n출력예 :\n{\n  "summarize": "벽화가 있는 동굴에서 무공을 얻음, id 5번 데이터 이상",\n  "notifyId": ["0005"],\n  "0001": "고요한 유산심곡(幽山深谷)에<br>수수께끼의 벽화가 남아있다.",\n  "0002": "이 동굴에는 강호인사(江湖人士)가 많다...",\n  "0003": "진입하여 깨달음을 얻는다.",\n  "0004": "일단 들어가지 않는다.",\n  "0006": "자신도 모르게 벽화에 그려진 {0}무공을 깨달았다."\n}\n위의 지침을 바탕으로 번역을 진행해주시기 바랍니다.',
                    }
                ],
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "네, 게임의 설정과 각 지침을 숙지했습니다. 데이터를 입력해주세요."}
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": '{\n  "context": "금전방고수의 성별: Male,금전방무리의 성별: Male,이심환의 성별: Male",\n  "talks": {\n    "0": {\n      "talker": "금전방고수(金錢幫高手)",\n      "content": "小的們，給我上！",\n      "type": "Dialog"\n    },\n    "1": {\n      "talker": "금전방무리(金錢幫幫眾)",\n      "content": "是！",\n      "type": "Dialog"\n    },\n    "2": {\n      "talker": "이심환(李尋歡)",\n      "content": "你們飛少爺人在何處？",\n      "type": "Dialog",\n      "next_talks": "3"\n    },\n    "3": {\n      "talker": "금전방고수(金錢幫高手)",\n      "content": "咳……少爺往……東邊的野林深處……去了。",\n      "type": "Dialog"\n    }\n  }\n}',
                    }
                ],
            },
        ],
    )

    print(message.content)




dialogues = json.load(open("./data/dialogues.json", mode="r", encoding="utf-8"))


def batch_process(start_index: int = 0, end_index: int = 1):
    
    prompt = '당신은 중국어 무협 텍스트를 한국어로 번역하는 전문가입니다. 중국에서 제작된 무협 게임의 스크립트들을 한국어로 번역할 것 입니다.\n제공될 텍스트는 고룡(古龍)작가의 무협 세계관을 기반으로 한 게임 고룡풍운록(古龍風雲錄)의 스크립트들입니다. 하드보일드한 문체가 특징입니다.\n게임 플롯 : 플레이어 진우(辰雨)는 구주왕심천군(九州王沈天君)이 인의장(仁義莊)에 데려온 출신을 알 수 소년으로, 심천군은 형산(衡山) 회안봉(回雁峰)에 무적검전(無敵劍典)이 있다는 소문에 휘말려 죽고 십년이 지났다.\n최근 연남천(燕南天)의 장보도가 있다는 소문이 돌자 냉이(冷二)가 진우를 강호로 보내 진실을 밝히려 한다.\n주요 등장인물\n진우(辰雨): 감정이 메마른 무미건조한 남자, 플레이어가 조종하는 주인공\n강소어: 장난기 많고 게으르며 무례한 말을 잘하는 소년\n육소봉: 의리가 있지만 말투가 신랄한 호색한\n이심환 : 유명한 가문의 후손이지만 명예를 버리고 은둔한 남자로 정의롭다\n초류향 : 도적으로 알려졌으나 경공이 뛰어나고 사람을 해치지 않는 정의로운 남자\n심랑: 명가 출신의 공손한 말투를 사용하는 남자\n공손란: 비밀 조직 홍혜자(紅鞋子)의 수장으로 아름답지만 날카로운 여자\n왕련화: 변장술에 능하며 의중을 알 수 없는 남자\n소앵: 총명하지만 차가워보이는 소녀\n손소홍: 설서인(說書人)이 되고 싶은 손백발 노인의 손녀\n주칠칠: 정의감 강하고 당찬 부잣집의 아름다운 영애\n번역지침\n1. 높임말과 반말, 평서체를 구분해서 사용.\n- 존댓말: 부탁이나 공경의 표현에 사용. 예: "謹聽莊主之命！" → "장주님의 명에 따르겠습니다."\n- 반말: 도발적, 협박적, 고압적인 말투에 사용. 예: "軟柿子，受死吧！" → "나약한 놈, 죽어라!"\n- 평서체: 불확실한 상황이나 상황 설명에 사용. 예: "夾層中放了一張紙，寫著「揚瀾小鎮怪郎中」。" → "사이에 끼워진 종이에는, \'양란소진괴랑중(揚瀾小鎮怪郎中)\'이 적혀있다."\n2. 태그와 플레이스홀더 유지.\n- "{}"안의 내용 유지. 예: "這是{it2000_03}。" → "이것은 {it2000_03}이다."\n- "<>"안의 내용 유지. 예: "這<color=#FF0000>茶葉</color>你就拿去吧！" → "이 <color=#FF0000>찻잎</color>을 가져가!", "保護<b>{playerName}</b>!" → "<b>{playerName}</b>을/를 보호해!"\n3. 무협세계관 유지.\n- 영어에서 유래한 외래어 대신 한글/한자어 사용. 예: "一掌" → "일장", "桌子" → "탁자", "藏寶圖" → "장보도"\n- 무협식 호칭 주의. 예: "大俠" → "대협", "師兄" → "사형", "師姐" → "사저", "俠客" → "협객", "莊客" → "장객", "莊主" → "장주", "大哥" → "대가", "哥哥" → "가가" 등\n4. 한자 병기.\n- 이름, 지명, 무공, 물건, 별명. 예: "柴玉關" → "시옥관(柴玉關)", "我在地靈莊。" → "나는 지령장(地靈莊)에 있다.", "秘笈，正陽佛手。" → "비급, 정양불수(正陽佛手)", "這是……嵩陽鐵劍？" → "이건...숭양철검(嵩陽鐵劍)?"\n- 고사성어는 뜻도 병기. 예: "漏了<color=#FF0000>果老騎驢</color>四個字。" → "<color=#FF0000>과로기려(果老騎驢:당나귀를 거꾸로 탄 노인)</color> 네 글자를 빠뜨렸다."\n- **반드시 한자 병기 지침 준수**.\n5. 자연스러운 표현과 정확한 문법.\n6. 입력 json 포맷.\n- context: 스크립트 속 인물의 정보와 특정 텍스트의 번역 정보 제공.\n- talks: 각 대화의 id를 키값으로 하여 제공됨\n- talker: 말하는 사람의 정보\n- type: 대화의 종류\n- content : 번역할 텍스트\n- next_talks: 다음 대화의 id 나열\n7. 출력 json\n- summarize: 번역된 대화문의 짧은 요약.\n- notify_id: 문제가 있는 텍스트의 ID 나열.\n입력예:\n{\n  "context": "벽화가 있는 동굴에 대한 이야기",\n  "talks": {\n   "1": {\n    "talker": "Narrator",\n    "content": "幽山深谷靜<br>壁畫驚成謎。",\n    "type": "Narrator"\n   },\n   "2": {\n    "talker": "Player",\n    "content": "此洞江湖人士眾多……",\n    "type": "Dialogue",\n    "next_talks": "3,4"\n   },\n   "3": {\n    "talker": "Option",\n    "content": "進入參悟",\n    "type": "Option"\n   },\n   "4": {\n    "talker": "Option",\n    "content": "暫且不入",\n    "type": "Option"\n   },\n   "5": {\n    "conten": "#N/A"\n   },\n   "6": {\n    "talker": "Narrator",\n    "content": "竟已領悟了壁畫上的{0}武功",\n    "type": "Narrator"\n   }\n  }\n}\n출력예 :\n{\n  "summarize": "벽화가 있는 동굴에서 무공을 얻음, id 5번 데이터 이상",\n  "notifyId": ["5"],\n  "1": "고요한 유산심곡(幽山深谷)에<br>수수께끼의 벽화가 남아있다.",\n  "2": "이 동굴에는 강호인사(江湖人士)가 많다...",\n  "3": "진입하여 깨달음을 얻는다.",\n  "4": "일단 들어가지 않는다.",\n  "6": "자신도 모르게 벽화에 그려진 {0}무공을 깨달았다."\n}\n위의 지침을 바탕으로 번역을 진행해주시기 바랍니다.'
    first_answer = "알겠습니다. 제시해주신 지침에 따라 중국 무협 게임 스크립트를 한국어로 번역하겠습니다. 게임의 세계관과 인물, 문체의 특징을 잘 살리면서 자연스러운 한국어 표현과 정확한 문법을 사용하도록 하겠습니다. 높임말과 반말, 평서체의 구분, 무협 용어와 한자 병기 등에도 주의를 기울이겠습니다. 입력된 json 포맷을 분석하여 summarize와 notify_id를 포함한 json 형태로 번역 결과를 출력하도록 하겠습니다. 더 필요한 사항이나 수정할 부분이 있다면 말씀해 주세요."
    api_key = toml.load("localconfig.toml")["local"]["CLAUDE_API_KEY"]
    claude = Claude3Api(api_key)
    for key in tqdm.tqdm(dialogue_keys[start_index:end_index]):
        if os.path.exists(f"./works/{key}.txt"):
            logging.info(f"{key} already exists")
            continue
        logging.info(f"Processing {key}")
        logging.info(json.dumps(dialogues[key], ensure_ascii=False))
        data = claude.translate(prompt, first_answer, json.dumps(dialogues[key], ensure_ascii=False, indent=2), 4096)
        logging.info(str(data.usage))
        logging.info(str(data.content[0].text))
        with open(f"./works/{key}.txt", mode="w", encoding="utf-8") as f:
            try:
                result = json.loads(data.content[0].text)
                f.write(json.dumps(result, ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                logging.error(f"{key} JSONDecodeError")
                f.write(repr(data.content[0].text))


def process_key(claude, prompt, first_answer, key):
    if os.path.exists(f"./works/{key}.txt"):
        logging.info(f"{key} already exists")
        return key, False  # 파일이 이미 존재하므로 처리하지 않음
    logging.info(f"Processing {key}")
    try:
        logging.info(json.dumps(dialogues[key], ensure_ascii=False))
        data = claude.translate(prompt, first_answer, json.dumps(dialogues[key], ensure_ascii=False, indent=2), 4096)
        result = json.loads(data.content[0].text)
        logging.info(str(data.usage))
        logging.info(str(data.content[0].text))
        with open(f"./works/{key}.txt", mode="w", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False, indent=2))
        return key, True  # 성공적으로 처리됨
    except Exception as e:
        with open(f"./works/{key}.txt", mode="w", encoding="utf-8") as f:
            f.write(repr(data.content[0].text))
        logging.error(f"Error processing {key}: {e}")
        return key, False  # 처리 중 오류 발생


def batch_process_concurrent(start_index=0, end_index=None, max_workers=5):
    if end_index is None:
        end_index = len(dialogue_keys)
    
    prompt = '당신은 중국어 무협 텍스트를 한국어로 번역하는 전문가입니다. 중국에서 제작된 무협 게임의 스크립트들을 한국어로 번역할 것 입니다.\n제공될 텍스트는 고룡(古龍)작가의 무협 세계관을 기반으로 한 게임 고룡풍운록(古龍風雲錄)의 스크립트들입니다. 하드보일드한 문체가 특징입니다.\n게임 플롯 : 플레이어 진우(辰雨)는 구주왕심천군(九州王沈天君)이 인의장(仁義莊)에 데려온 출신을 알 수 소년으로, 심천군은 형산(衡山) 회안봉(回雁峰)에 무적검전(無敵劍典)이 있다는 소문에 휘말려 죽고 십년이 지났다.\n최근 연남천(燕南天)의 장보도가 있다는 소문이 돌자 냉이(冷二)가 진우를 강호로 보내 진실을 밝히려 한다.\n주요 등장인물\n진우(辰雨): 감정이 메마른 무미건조한 남자, 플레이어가 조종하는 주인공\n강소어: 장난기 많고 게으르며 무례한 말을 잘하는 소년\n육소봉: 의리가 있지만 말투가 신랄한 호색한\n이심환 : 유명한 가문의 후손이지만 명예를 버리고 은둔한 남자로 정의롭다\n초류향 : 도적으로 알려졌으나 경공이 뛰어나고 사람을 해치지 않는 정의로운 남자\n심랑: 명가 출신의 공손한 말투를 사용하는 남자\n공손란: 비밀 조직 홍혜자(紅鞋子)의 수장으로 아름답지만 날카로운 여자\n왕련화: 변장술에 능하며 의중을 알 수 없는 남자\n소앵: 총명하지만 차가워보이는 소녀\n손소홍: 설서인(說書人)이 되고 싶은 손백발 노인의 손녀\n주칠칠: 정의감 강하고 당찬 부잣집의 아름다운 영애\n번역지침\n1. 높임말과 반말, 평서체를 구분해서 사용.\n- 존댓말: 부탁이나 공경의 표현에 사용. 예: "謹聽莊主之命！" → "장주님의 명에 따르겠습니다."\n- 반말: 도발적, 협박적, 고압적인 말투에 사용. 예: "軟柿子，受死吧！" → "나약한 놈, 죽어라!"\n- 평서체: 불확실한 상황이나 상황 설명에 사용. 예: "夾層中放了一張紙，寫著「揚瀾小鎮怪郎中」。" → "사이에 끼워진 종이에는, \'양란소진괴랑중(揚瀾小鎮怪郎中)\'이 적혀있다."\n2. 태그와 플레이스홀더 유지.\n- "{}"안의 내용 유지. 예: "這是{it2000_03}。" → "이것은 {it2000_03}이다."\n- "<>"안의 내용 유지. 예: "這<color=#FF0000>茶葉</color>你就拿去吧！" → "이 <color=#FF0000>찻잎</color>을 가져가!", "保護<b>{playerName}</b>!" → "<b>{playerName}</b>을/를 보호해!"\n3. 무협세계관 유지.\n- 영어에서 유래한 외래어 대신 한글/한자어 사용. 예: "一掌" → "일장", "桌子" → "탁자", "藏寶圖" → "장보도"\n- 무협식 호칭 주의. 예: "大俠" → "대협", "師兄" → "사형", "師姐" → "사저", "俠客" → "협객", "莊客" → "장객", "莊主" → "장주", "大哥" → "대가", "哥哥" → "가가" 등\n4. 한자 병기.\n- 이름, 지명, 무공, 물건, 별명. 예: "柴玉關" → "시옥관(柴玉關)", "我在地靈莊。" → "나는 지령장(地靈莊)에 있다.", "秘笈，正陽佛手。" → "비급, 정양불수(正陽佛手)", "這是……嵩陽鐵劍？" → "이건...숭양철검(嵩陽鐵劍)?"\n- 고사성어는 뜻도 병기. 예: "漏了<color=#FF0000>果老騎驢</color>四個字。" → "<color=#FF0000>과로기려(果老騎驢:당나귀를 거꾸로 탄 노인)</color> 네 글자를 빠뜨렸다."\n- **반드시 한자 병기 지침 준수**.\n5. 자연스러운 표현과 정확한 문법.\n6. 입력 json 포맷.\n- context: 스크립트 속 인물의 정보와 특정 텍스트의 번역 정보 제공.\n- talks: 각 대화의 id를 키값으로 하여 제공됨\n- talker: 말하는 사람의 정보\n- type: 대화의 종류\n- content : 번역할 텍스트\n- next_talks: 다음 대화의 id 나열\n7. 출력 json\n- summarize: 번역된 대화문의 짧은 요약.\n- notify_id: 문제가 있는 텍스트의 ID 나열.\n입력예:\n{\n  "context": "벽화가 있는 동굴에 대한 이야기",\n  "talks": {\n   "1": {\n    "talker": "Narrator",\n    "content": "幽山深谷靜<br>壁畫驚成謎。",\n    "type": "Narrator"\n   },\n   "2": {\n    "talker": "Player",\n    "content": "此洞江湖人士眾多……",\n    "type": "Dialogue",\n    "next_talks": "3,4"\n   },\n   "3": {\n    "talker": "Option",\n    "content": "進入參悟",\n    "type": "Option"\n   },\n   "4": {\n    "talker": "Option",\n    "content": "暫且不入",\n    "type": "Option"\n   },\n   "5": {\n    "conten": "#N/A"\n   },\n   "6": {\n    "talker": "Narrator",\n    "content": "竟已領悟了壁畫上的{0}武功",\n    "type": "Narrator"\n   }\n  }\n}\n출력예 :\n{\n  "summarize": "벽화가 있는 동굴에서 무공을 얻음, id 5번 데이터 이상",\n  "notifyId": ["5"],\n  "1": "고요한 유산심곡(幽山深谷)에<br>수수께끼의 벽화가 남아있다.",\n  "2": "이 동굴에는 강호인사(江湖人士)가 많다...",\n  "3": "진입하여 깨달음을 얻는다.",\n  "4": "일단 들어가지 않는다.",\n  "6": "자신도 모르게 벽화에 그려진 {0}무공을 깨달았다."\n}\n위의 지침을 바탕으로 번역을 진행해주시기 바랍니다.'
    first_answer = "알겠습니다. 제시해주신 지침에 따라 중국 무협 게임 스크립트를 한국어로 번역하겠습니다. 게임의 세계관과 인물, 문체의 특징을 잘 살리면서 자연스러운 한국어 표현과 정확한 문법을 사용하도록 하겠습니다. 높임말과 반말, 평서체의 구분, 무협 용어와 한자 병기 등에도 주의를 기울이겠습니다. 입력된 json 포맷을 분석하여 summarize와 notify_id를 포함한 json 형태로 번역 결과를 출력하도록 하겠습니다. 더 필요한 사항이나 수정할 부분이 있다면 말씀해 주세요."
    api_key = toml.load("localconfig.toml")["local"]["CLAUDE_API_KEY"]
    claude = Claude3Api(api_key)

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for key in dialogue_keys[start_index:end_index]:
            future = executor.submit(process_key, claude, prompt, first_answer, key)
            futures.append(future)
        
        # 진행 상황을 표시하기 위해 tqdm을 사용
        for future in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            key, success = future.result()
            if success:
                logging.info(f"Successfully processed {key}")
            else:
                logging.error(f"Failed to process {key}")

if __name__ == "__main__":
    api_key = toml.load("localconfig.toml")["local"]["CLAUDE_API_KEY"]
    logging.basicConfig(
        level=logging.INFO,
        filename="translator.log",
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )
    # test_function()
    # batch_process(0, None)
    # test_function2(api_key)
    batch_process_concurrent(0, None, max_workers=6)