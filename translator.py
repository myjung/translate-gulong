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
    "be020002#0",
    "be020002#1",
    "be020002#2",
    "md060001#0",
    "md060001#1",
    "mg061001#0",
    "mg061001#1",
    "mb063200#0",
    "mb063200#1",
    "mb063200#2",
    "mg061000#0",
    "mg061000#1",
    "mh000003#0",
    "mh000003#1",
    "md060000#0",
    "md060000#1",
    "mc010007#0",
    "mc010007#1",
    "mg000072#0",
    "mg000072#1",
    "mg000072#2",
    "mc050059#0",
    "mc050059#1",
    "mq130007#0",
    "mq130007#1",
    "mq130007#2",
    "ma210008#0",
    "ma210008#1",
    "ma210008#2",
    "w0105004#0",
    "w0105004#1",
    "w0105004#2",
    "w0105004#3",
    "w0105021#0",
    "w0105021#1",
    "w0105021#2",
    "be02100b#0",
    "be02100b#1",
    "be02100b#2",
    "be02100b#3",
    "mc050023#0",
    "mc050023#1",
    "mc050023#2",
    "mh061004#0",
    "mh061004#1",
    "mh061004#2",
    "mq050004#0",
    "mq050004#1",
    "mq050004#2",
    "mc050009#0",
    "mc050009#1",
    "mc050009#2",
    "mg000060#0",
    "mg000060#1",
    "mc050071#0",
    "mc050071#1",
    "mc050071#2",
    "mh061005#0",
    "mh061005#1",
    "mh061005#2",
    "mg060002#0",
    "mg060002#1",
    "mg060002#2",
    "mh130004#0",
    "mh130004#1",
    "mh130004#2",
    "w2205019#0",
    "w2205019#1",
    "w2205019#2",
    "mc050010#0",
    "mc050010#1",
    "mc050010#2",
    "mq120014#0",
    "mq120014#1",
    "mm101000#0",
    "mm101000#1",
    "mm101000#2",
    "ma070003#0",
    "ma070003#1",
    "ma070003#2",
    "mg115002#0",
    "mg115002#1",
    "mg115002#2",
    "md060002#0",
    "md060002#1",
    "md060002#2",
    "mg000031#0",
    "mg000031#1",
    "mh000044#0",
    "mh000044#1",
    "mh000044#2",
    "mh000042#0",
    "mh000042#1",
    "mh000042#2",
    "mq220004#0",
    "mq220004#1",
    "mq220004#2",
    "mh060001#0",
    "mh060001#1",
    "mg000059#0",
    "mg000059#1",
    "mg000059#2",
    "mc050015#0",
    "mc050015#1",
    "mq200007#0",
    "mq200007#1",
    "mq200007#2",
    "mq130005#0",
    "mq130005#1",
    "mq130005#2",
    "mq130005#3",
    "mq120015#0",
    "mq120015#1",
    "mq120015#2",
    "mq120001#0",
    "mq120001#1",
    "mg800001#0",
    "mg800001#1",
    "mg800001#2",
    "ma220009#0",
    "ma220009#1",
    "ma220009#2",
    "mh000026#0",
    "mh000026#1",
    "mh000017#0",
    "mh000017#1",
    "mh000017#2",
    "mq120004#0",
    "mq120004#1",
    "mq120004#2",
    "w2205010#0",
    "w2205010#1",
    "w2205010#2",
    "mc050025#0",
    "mc050025#1",
    "mc050025#2",
    "mc050025#3",
    "mg000062#0",
    "mg000062#1",
    "mg000062#2",
    "mg000062#3",
    "mg010002#0",
    "mg010002#1",
    "mg010002#2",
    "mn060001#0",
    "mn060001#1",
    "mn060001#2",
    "mq050002#0",
    "mq050002#1",
    "mq050002#2",
    "mq050002#3",
    "md060003#0",
    "md060003#1",
    "md060003#2",
    "w1105003#0",
    "w1105003#1",
    "w1105003#2",
    "mq060020#0",
    "mq060020#1",
    "mq060020#2",
    "mq060020#3",
    "mm102001#0",
    "mm102001#1",
    "mm102001#2",
    "mm060000#0",
    "mm060000#1",
    "mm060000#2",
    "mm060000#3",
    "ma800004#0",
    "ma800004#1",
    "ma800004#2",
    "ma800004#3",
    "mh000038#0",
    "mh000038#1",
    "mh000038#2",
    "mh000038#3",
    "mg190001#0",
    "mg190001#1",
    "mg190001#2",
    "mg190001#3",
    "mh000048#0",
    "mh000048#1",
    "mh000048#2",
    "mh000048#3",
    "mh000047#0",
    "mh000047#1",
    "mh000047#2",
    "mh000047#3",
    "e001c004#0",
    "e001c004#1",
    "e001c004#2",
    "e001c004#3",
    "e001c004#4",
    "w1105001#0",
    "w1105001#1",
    "w1105001#2",
    "w1105001#3",
    "mh000034#0",
    "mh000034#1",
    "mh000034#2",
    "mh000034#3",
    "mg280001#0",
    "mg280001#1",
    "mg280001#2",
    "mg280001#3",
    "mg280001#4",
    "mg280001#5",
    "mg370001#0",
    "mg370001#1",
    "mg370001#2",
    "mg370001#3",
    "mg000009#0",
    "mg000009#1",
    "mg000009#2",
    "mg801001#0",
    "mg801001#1",
    "mg801001#2",
    "mg801001#3",
    "mm102000#0",
    "mm102000#1",
    "mm102000#2",
    "mm102000#3",
    "mg110000#0",
    "mg110000#1",
    "mg110000#2",
    "mg110000#3",
    "mg110000#4",
    "mh000032#0",
    "mh000032#1",
    "mh000032#2",
    "mh000032#3",
    "w0105002#0",
    "w0105002#1",
    "w0105002#2",
    "w0105002#3",
    "w0105002#4",
    "w0105002#5",
    "w2105002#0",
    "w2105002#1",
    "w2105002#2",
    "w2105002#3",
    "mq120010#0",
    "mq120010#1",
    "mq120010#2",
    "w2105001#0",
    "w2105001#1",
    "w2105001#2",
    "w2105001#3",
    "mg000061#0",
    "mg000061#1",
    "mg000061#2",
    "mg000061#3",
    "mg000061#4",
    "mm101002#0",
    "mm101002#1",
    "mm101002#2",
    "mm101002#3",
    "mm101002#4",
    "mn060002#0",
    "mn060002#1",
    "mn060002#2",
    "mn060002#3",
    "mn060002#4",
    "w1105002#0",
    "w1105002#1",
    "w1105002#2",
    "w1105002#3",
    "w1105002#4",
    "w1105002#5",
    "mg102001#0",
    "mg102001#1",
    "mg102001#2",
    "mg102001#3",
    "mg102001#4",
    "mg102001#5",
    "mg102001#6",
    "mh170000#0",
    "mh170000#1",
    "mh170000#2",
    "mh170000#3",
    "mh170000#4",
    "mg000000#0",
    "mg000000#1",
    "mg000000#2",
    "mg000000#3",
    "mg000000#4",
    "mg000000#5",
    "mh000033#0",
    "mh000033#1",
    "mh000033#2",
    "mh000033#3",
    "mh000033#4",
    "mh000043#0",
    "mh000043#1",
    "mh000043#2",
    "mh000043#3",
    "mh000043#4",
    "mh000043#5",
    "mh000043#6",
    "mg060008#0",
    "mg060008#1",
    "mg060008#2",
    "mg060008#3",
    "mg060008#4",
    "mg060008#5",
    "mg060008#6",
    "mh130002#0",
    "mh130002#1",
    "mh130002#2",
    "mh130002#3",
    "mh130002#4",
    "mh130002#5",
    "mh130002#6",
    "mh130002#7",
    "mh130002#8",
    "mh000023#0",
    "mh000023#1",
    "mh000023#2",
    "mh000023#3",
    "mh000023#4",
    "mh000023#5",
    "w2205022#0",
    "w2205022#1",
    "w2205022#2",
    "w2205022#3",
    "w2205022#4",
    "w2205022#5",
    "w2205022#6",
    "mg310002#0",
    "mg310002#1",
    "mg310002#2",
    "mg310002#3",
    "mg310002#4",
    "mg310002#5",
    "mh210000#0",
    "mh210000#1",
    "mh210000#2",
    "mh210000#3",
    "mh210000#4",
    "mh210000#5",
    "mh210000#6",
    "mh210000#7",
    "mm102002#0",
    "mm102002#1",
    "mm102002#2",
    "mm102002#3",
    "mm102002#4",
    "mm102002#5",
    "mm102002#6",
    "mm102002#7",
    "mh130003#0",
    "mh130003#1",
    "mh130003#2",
    "mh130003#3",
    "mh130003#4",
    "mh130003#5",
    "mh130003#6",
    "mh000024#0",
    "mh000024#1",
    "mh000024#2",
    "mh000024#3",
    "mh000024#4",
    "mh000024#5",
    "mh000024#6",
    "mh000024#7",
    "mh000024#8",
    "mh000028#0",
    "mh000028#1",
    "mh000028#2",
    "mh000028#3",
    "mh000028#4",
    "mh000028#5",
    "mh000028#6",
    "mg060001#0",
    "mg060001#1",
    "mg060001#2",
    "mg060001#3",
    "mg060001#4",
    "mg060001#5",
    "mg060001#6",
    "mg060001#7",
    "mg060001#8",
    "mn060005#0",
    "mn060005#1",
    "mn060005#2",
    "mn060005#3",
    "mn060005#4",
    "mn060005#5",
    "mn060005#6",
    "mn060005#7",
    "mh000001#0",
    "mh000001#1",
    "mh000001#2",
    "mh000001#3",
    "mh000001#4",
    "mh000001#5",
    "mh000001#6",
    "mh000027#0",
    "mh000027#1",
    "mh000027#2",
    "mh000027#3",
    "mh000027#4",
    "mh000027#5",
    "mh000027#6",
    "mh000027#7",
    "mn060004#0",
    "mn060004#1",
    "mn060004#2",
    "mn060004#3",
    "mn060004#4",
    "mn060004#5",
    "mn060004#6",
    "mn060004#7",
    "mh000016#0",
    "mh000016#1",
    "mh000016#2",
    "mh000016#3",
    "mh000016#4",
    "mh000016#5",
    "mh000016#6",
    "mh000016#7",
    "mh000016#8",
    "mh000021#0",
    "mh000021#1",
    "mh000021#2",
    "mh000021#3",
    "mh000021#4",
    "mh000021#5",
    "mh000021#6",
    "mh000021#7",
    "mh000021#8",
    "mh000021#9",
    "mm101001#0",
    "mm101001#1",
    "mm101001#2",
    "mm101001#3",
    "mm101001#4",
    "mm101001#5",
    "mm101001#6",
    "mm101001#7",
    "mm101001#8",
    "mm101001#9",
    "w2105021#0",
    "w2105021#1",
    "w2105021#2",
    "w2105021#3",
    "w2105021#4",
    "w2105021#5",
    "w2105021#6",
    "w2105021#7",
    "w2105021#8",
    "w2105021#9",
    "w2105021#10",
    "mh000018#0",
    "mh000018#1",
    "mh000018#2",
    "mh000018#3",
    "mh000018#4",
    "mh000018#5",
    "mh000018#6",
    "mh000018#7",
    "mh000018#8",
    "mh000018#9",
    "mh000018#10",
    "mn060003#0",
    "mn060003#1",
    "mn060003#2",
    "mn060003#3",
    "mn060003#4",
    "mn060003#5",
    "mn060003#6",
    "mn060003#7",
    "mn060003#8",
    "mn060003#9",
    "mh000022#0",
    "mh000022#1",
    "mh000022#2",
    "mh000022#3",
    "mh000022#4",
    "mh000022#5",
    "mh000022#6",
    "mh000022#7",
    "mh000022#8",
    "mh000022#9",
    "mh000022#10",
    "mh000020#0",
    "mh000020#1",
    "mh000020#2",
    "mh000020#3",
    "mh000020#4",
    "mh000020#5",
    "mh000020#6",
    "mh000020#7",
    "mh000020#8",
    "mh000020#9",
    "mh000020#10",
    "mh000041#0",
    "mh000041#1",
    "mh000041#2",
    "mh000041#3",
    "mh000041#4",
    "mh000041#5",
    "mh000041#6",
    "mh000041#7",
    "mh000041#8",
    "mh000041#9",
    "mh000041#10",
    "mh000041#11",
    "mh000041#12",
    "mh000041#13",
    "mh000041#14",
    "mh060003#0",
    "mh060003#1",
    "mh060003#2",
    "mh060003#3",
    "mh060003#4",
    "mh060003#5",
    "mh060003#6",
    "mh060003#7",
    "mh060003#8",
    "mh060003#9",
    "mh060003#10",
    "mh060003#11",
    "mn060008#0",
    "mn060008#1",
    "mn060008#2",
    "mn060008#3",
    "mn060008#4",
    "mn060008#5",
    "mn060008#6",
    "mn060008#7",
    "mn060008#8",
    "mn060008#9",
    "mn060008#10",
    "mn060008#11",
    "mn060008#12",
    "mn060008#13",
    "mn060008#14",
    "mn060008#15",
    "mg160001#0",
    "mg160001#1",
    "mg160001#2",
    "mg160001#3",
    "mg160001#4",
    "mg160001#5",
    "mg160001#6",
    "mg160001#7",
    "mg160001#8",
    "mg160001#9",
    "mg160001#10",
    "mg160001#11",
    "mg160001#12",
    "mn060007#0",
    "mn060007#1",
    "mn060007#2",
    "mn060007#3",
    "mn060007#4",
    "mn060007#5",
    "mn060007#6",
    "mn060007#7",
    "mn060007#8",
    "mn060007#9",
    "mn060007#10",
    "mn060007#11",
    "mn060007#12",
    "mn060007#13",
    "mn060007#14",
    "mn060007#15",
    "mn060007#16",
    "mn060007#17",
    "mq200005#0",
    "mq200005#1",
    "mq200005#2",
    "mq200005#3",
    "mq200005#4",
    "mq200005#5",
    "mq200005#6",
    "mq200005#7",
    "mq200005#8",
    "mq200005#9",
    "mq200005#10",
    "mq200005#11",
    "mq200005#12",
    "mq200005#13",
    "mq200005#14",
    "mq200005#15",
    "mq200005#16",
    "mn060006#0",
    "mn060006#1",
    "mn060006#2",
    "mn060006#3",
    "mn060006#4",
    "mn060006#5",
    "mn060006#6",
    "mn060006#7",
    "mn060006#8",
    "mn060006#9",
    "mn060006#10",
    "mn060006#11",
    "mn060006#12",
    "mn060006#13",
    "mn060006#14",
    "mn060006#15",
    "mn060006#16",
    "mh000039#0",
    "mh000039#1",
    "mh000039#2",
    "mh000039#3",
    "mh000039#4",
    "mh000039#5",
    "mh000039#6",
    "mh000039#7",
    "mh000039#8",
    "mh000039#9",
    "mh000039#10",
    "mh000039#11",
    "mh000039#12",
    "mh000039#13",
    "mh000039#14",
    "mh000039#15",
    "mh000039#16",
    "mh000039#17",
    "mh000039#18",
    "mh000039#19",
    "mh000039#20",
    "mh130000#0",
    "mh130000#1",
    "mh130000#2",
    "mh130000#3",
    "mh130000#4",
    "mh130000#5",
    "mh130000#6",
    "mh130000#7",
    "mh130000#8",
    "mh130000#9",
    "mh130000#10",
    "mh130000#11",
    "mh130000#12",
    "mh130000#13",
    "mh130000#14",
    "mh130000#15",
    "mh130000#16",
    "mh130000#17",
    "mh130000#18",
    "mh130000#19",
    "mh130000#20",
    "mh130000#21",
    "mh130000#22",
    "mh130000#23",
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

    prompt = '당신은 중국어 무협 텍스트를 한국어로 번역하는 전문가입니다. 중국에서 제작된 무협 게임의 스크립트들을 한국어로 번역할 것 입니다.\n제공될 텍스트는 고룡(古龍)작가의 무협 세계관을 기반으로 한 게임 고룡풍운록(古龍風雲錄)의 스크립트들입니다. 하드보일드한 문체가 특징입니다.\n게임 플롯 : 플레이어 진우(辰雨)는 구주왕심천군(九州王沈天君)이 인의장(仁義莊)에 데려온 출신을 알 수 소년으로, 심천군은 형산(衡山) 회안봉(回雁峰)에 무적검전(無敵劍典)이 있다는 소문에 휘말려 죽고 십년이 지났다.\n최근 연남천(燕南天)의 장보도가 있다는 소문이 돌자 냉이(冷二)가 진우를 강호로 보내 진실을 밝히려 한다.\n주요 등장인물\n진우(辰雨): 감정이 메마른 무미건조한 남자, 플레이어가 조종하는 주인공\n강소어: 장난기 많고 게으르며 무례한 말을 잘하는 소년\n육소봉: 의리가 있지만 말투가 신랄한 호색한\n이심환 : 유명한 가문의 후손이지만 명예를 버리고 은둔한 남자로 정의롭다\n초류향 : 도적으로 알려졌으나 경공이 뛰어나고 사람을 해치지 않는 정의로운 남자\n심랑: 명가 출신의 공손한 말투를 사용하는 남자\n공손란: 비밀 조직 홍혜자(紅鞋子)의 수장으로 아름답지만 날카로운 여자\n왕련화: 변장술에 능하며 의중을 알 수 없는 남자\n소앵: 총명하지만 차가워보이는 소녀\n손소홍: 설서인(說書人)이 되고 싶은 손백발 노인의 손녀\n주칠칠: 정의감 강하고 당찬 부잣집의 아름다운 영애\n번역지침\n1. 높임말과 반말, 평서체를 구분해서 사용.\n- 존댓말: 부탁이나 공경의 표현에 사용. 예: "謹聽莊主之命！" → "장주님의 명에 따르겠습니다."\n- 반말: 도발적, 협박적, 고압적인 말투에 사용. 예: "軟柿子，受死吧！" → "나약한 놈, 죽어라!"\n- 평서체: 불확실한 상황이나 상황 설명에 사용. 예: "夾層中放了一張紙，寫著「揚瀾小鎮怪郎中」。" → "사이에 끼워진 종이에는, \'양란소진괴랑중(揚瀾小鎮怪郎中)\'이 적혀있다."\n2. 태그와 플레이스홀더 유지.\n- "{}"안의 내용 유지. 예: "這是{it2000_03}。" → "이것은 {it2000_03}이다."\n- "<>"안의 내용 유지. 예: "這<color=#FF0000>茶葉</color>你就拿去吧！" → "이 <color=#FF0000>찻잎</color>을 가져가!", "保護<b>{playerName}</b>!" → "<b>{playerName}</b>을/를 보호해!"\n3. 무협세계관 유지.\n- 영어에서 유래한 외래어 대신 한글/한자어 사용. 예: "一掌" → "일장", "桌子" → "탁자", "藏寶圖" → "장보도"\n- 무협식 호칭 주의. 예: "大俠" → "대협", "師兄" → "사형", "師姐" → "사저", "俠客" → "협객", "莊客" → "장객", "莊主" → "장주", "大哥" → "대가", "哥哥" → "가가" 등\n4. 한자 병기.\n- 이름, 지명, 무공, 물건, 별명. 예: "柴玉關" → "시옥관(柴玉關)", "我在地靈莊。" → "나는 지령장(地靈莊)에 있다.", "秘笈，正陽佛手。" → "비급, 정양불수(正陽佛手)", "這是……嵩陽鐵劍？" → "이건...숭양철검(嵩陽鐵劍)?"\n- 고사성어는 뜻도 병기. 예: "漏了<color=#FF0000>果老騎驢</color>四個字。" → "<color=#FF0000>과로기려(果老騎驢:당나귀를 거꾸로 탄 노인)</color> 네 글자를 빠뜨렸다."\n- **반드시 한자 병기 지침 준수**.\n5. 자연스러운 표현과 정확한 문법.\n6. 입력 json 포맷.\n- context: 스크립트 속 인물의 정보와 특정 텍스트의 번역 정보 제공.\n- talks: 각 대화의 id를 키값으로 하여 제공됨\n- talker: 말하는 사람의 정보\n- type: 대화의 종류\n- content : 번역할 텍스트\n7. 출력 json\n- summarize: 번역된 대화문의 짧은 요약.\n- notify_id: 문제가 있는 텍스트의 ID 나열.\n입력예:\n{\n  "context": "Player:남성, \\"幽山深谷\\" → \\"심산유곡\\"",\n  "talks": {\n   "1": {\n    "talker": "Narrator",\n    "content": "幽山深谷靜<br>壁畫驚成謎。",\n    "type": "Narrator"\n   },\n   "2": {\n    "talker": "Player",\n    "content": "此洞江湖人士眾多……",\n    "type": "Dialogue",\n   },\n   "3": {\n    "talker": "Option",\n    "content": "進入參悟",\n    "type": "Option"\n   },\n   "4": {\n    "talker": "Option",\n    "content": "暫且不入",\n    "type": "Option"\n   },\n   "5": {\n    "conten": "#N/A"\n   },\n   "6": {\n    "talker": "Narrator",\n    "content": "竟已領悟了壁畫上的{0}武功",\n    "type": "Narrator"\n   }\n  }\n}\n출력예 :\n{\n  "summarize": "벽화가 있는 동굴에서 무공을 얻음",\n  "notifyId": ["5"],\n  "1": "고요한 심산유곡(幽山深谷)에<br>수수께끼의 벽화가 남아있다.",\n  "2": "이 동굴에는 강호인사(江湖人士)가 많다...",\n  "3": "진입하여 깨달음을 얻는다.",\n  "4": "일단 들어가지 않는다.",\n  "6": "자신도 모르게 벽화에 그려진 {0}무공을 깨달았다."\n}\n위의 지침을 바탕으로 번역을 진행해주시기 바랍니다.'
    first_answer = "알겠습니다. 지침에 따라 중국어 무협 텍스트를 한국어로 번역하겠습니다. 입력해 주신 json 형식의 텍스트를 받아 번역을 진행하고, 요약문과 문제가 있는 텍스트의 ID를 함께 출력하겠습니다. 번역 시 높임말과 반말, 평서체를 구분하여 사용하고, 태그와 플레이스홀더를 유지하며, 무협 세계관에 맞는 용어를 사용하겠습니다. 또한 한자 병기 지침을 준수하여 이름, 지명, 무공, 물건, 별명 등에 한자를 병기하고, 고사성어의 경우 뜻도 함께 병기하도록 하겠습니다. 자연스러운 표현과 정확한 문법을 사용하여 번역하겠습니다. 중국어 무협 텍스트를 입력해 주시면 바로 번역을 시작하겠습니다."
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
    dialogues = json.load(open("./data/sliced_dialogues.json", mode="r", encoding="utf-8"))
    batch_process_concurrent(12, None, max_workers=10)
