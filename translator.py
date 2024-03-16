import json
import logging
import toml
import anthropic


class Claude3Api:
    def __init__(self, api_key: str, max_tokens: int = 1001, temperature: int = 0):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.max_tokens = max_tokens
        self.temperature = temperature

    def translate(
        self, prompt: str, first_answer: str, text: str, input_max_tokens: int = None, input_temperature: int = None
    ):
        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=input_max_tokens or self.max_tokens,
            temperature=input_temperature or self.temperature,
            messages=[
                {"role": "user", "content": [{"type": "text", "text": prompt}]},
                {"role": "assistant", "content": [{"type": "text", "text": first_answer}]},
                {"role": "user", "content": [{"type": "text", "text": text}]},
            ],
        )
        return message.content

def test_function():
    test_prompt = "이것은 테스트 프롬프트입니다. 제가 hello라고 하면 world라고 응답해주세요."
    test_first_return = "네, 이것은 테스트 프롬프트에 대한 첫 번째 응답입니다."
    test_text = "hello"
    api_key = toml.load("localconfig.toml")["local"]["CLAUDE_API_KEY"]
    claude = Claude3Api(api_key)
    claude_response = claude.translate(test_prompt, test_first_return, test_text)
    assert(claude_response[0].text == "world")

if __name__ == "__main__":
    # prompt = '당신은 중국어 무협 텍스트를 한국어로 번역하는 전문가입니다. 중국에서 제작된 무협 게임의 스크립트들을 한국어로 번역할 것입니다.\n제공될 텍스트는 고룡(古龍)작가의 무협 세계관을 기반으로 한 게임 고룡풍운록(古龍風雲錄)의 스크립트들입니다. 그의 특징적인 문체를 살리세요.\n게임 플롯 : 진우(辰雨)는 구주왕심천군(九州王沈天君)이 인의장(仁義莊)에 데려온 출신을 알 수 없는 서동(書童)이었습니다.\n전 장주였던 심천군은 형산(衡山) 회안봉(回雁峰)에 무적검전(無敵劍典)이 있다는 소문으로 벌어진 음모에 휘말려 죽었고 이후 십년이 지났습니다.\n최근 연남천(燕南天)의 장보도가 있다는 소문이 돌자 음모의 연관성을 의심한 냉이(冷二)가 그를 강호로 보내 사건을 조사하며 음모를 밝히는 내용의 RPG입니다.\n주인공 설정 : 진우(辰雨)는 한때 인의장의 그림자 같은 인물로, 감정이 메마르고 말이 적으며, 출신내력이 불명하다. 옛 장주의 유언에 따라 직무를 맡거나 장을 나가는 것, 손을 쓰면 안 된다는 규칙을 지켜왔다. 회안봉 사건 십년이 지나서야 강호에 발을 들였다.\n번역지침\n1. 높임말과 반말, 평서체를 구분해서 사용.\n- 존댓말: 부탁이나 공경의 표현에 사용. 예: "謹聽莊主之命！" → "장주님의 명에 따르겠습니다."\n- 반말: 도발적, 협박적, 고압적인 말투에 사용. 예: "軟柿子，受死吧！" → "나약한 놈, 죽어라!"\n- 평서체: 불확실한 상황이나 상황 설명에 사용. 예: "夾層中放了一張紙，寫著「揚瀾小鎮怪郎中」。" → "사이에 끼워진 종이에는, \'양란소진괴랑중(揚瀾小鎮怪郎中)\'이 적혀있다."\n- 위 지침에 어긋나더라도, 맥락을 고려했을 때 더 적합한 표현이 있다면 그것을 사용하세요.\n2. 태그와 플레이스홀더 유지.\n- "{}"안에 있는 내용은 그대로 두세요. 예: "這是{it2000_03}。" → "이것은 {it2000_03}이다."\n- "<>"안에 있는 내용도 번역하지 마세요. 예: "這<color=#FF0000>茶葉</color>你就拿去吧！" → "이 <color=#FF0000>찻잎</color>을 가져가!", "保護<b>{playerName}</b>!" → "<b>{playerName}</b>을/를 보호해!"\n- 태그와 플레이스 홀더는 게임엔진에서 출력될 때 변경되므로 오타나 변경이 있을 경우 게임이 멈출 수도 있습니다. 주의하세요!\n3. 무협세계관 유지.\n- 한글/한자어 사용: 영어에서 유래한 외래어 대신 한글/한자어 사용. 예: "桌子" → "탁자","藏寶圖" → "장보도", "公子" → "공자"\n- 무협지식 호칭에 주의. 예: "大俠" → "대협", "師兄" → "사형", "師姐" → "사저", "俠客" → "협객", "莊客" → "장객", "莊主" → "장주" 등\n4. 원문 표기.\n- 이름, 지명, 무공, 물건, 별명 등은 음차하고 원문을 병기하여 사용. 예: "辰雨" → "진우(辰雨)", "柴玉關" → "시옥관(柴玉關)", "我在地靈莊。" → "나는 지령장(地靈莊)에 있다.", "秘笈，正陽佛手。" → "비급, 정양불수(正陽佛手)", "這是……嵩陽鐵劍？" → "이건...숭양철검(嵩陽鐵劍)?"\n- 고사성어에서 유래된 표현등은 뜻을 번역하고 원문을 병기하세요. 예: "漏了<color=#FF0000>果老騎驢</color>四個字。" → "<color=#FF0000>과로기려(果老騎驢:당나귀를 거꾸로 탄 노인)</color> 네 글자를 빠뜨렸다."\n- **최종적으로 번역된 결과물에서 병기된 원문은 검수자가 일괄 처리 할 수 있으므로 한자 병기 지침을 항상 준수**.\n5. 문법 및 표현의 자연스러움 재확인.\n잘 지켜진 예: "九年前……你──！你可是朱家的千金？" → "구년 전... 너는──! 혹시 주가의 천금(千金)인가?"\n잘못된 예(문법적으로 어색함):"九年前……你──！你可是朱家的千金？" → "아홉 해 전…… 너는──! 너 혹시 주가(朱家)의 따님인가?"\n6. 번역 중 의미가 모호한 경우 원문의 의도를 가장 잘 전달할 수 있는 표현 선택.\n7. 입력 json 데이터의 포맷 설명.\n- context: 장소와 발화자가 누구인지 등에 대한 정보 제공.\n- talks: 연속된 대화내용이 각 대화의 id 순으로 제공됨\n- talker: 발화자의 id, 필요한 경우 context를 통해 id가 누구인지 명시함\n- type: 대화의 종류. Narrator(내레이터), Dialogue(대화), Option(플레이어의 선택지) 등이 있음\n- content : 번역할 텍스트\n- next_talks: 다음 대화의 id 나열. Optional Field\n7. 번역결과를 검토하기 위한 다음 필드 명시\n- 입출력 데이터는 유효한 json 포맷.\n- summarize: 번역된 대화문의 요약.\n- notify_id: 번역 과정 중 발견된 문제가 있는 텍스트의 ID 나열.\n입력예 :\n{\n  "context": "벽화가 있는 동굴에 대한 이야기",\n  "talks": {\n   "0001": {\n    "talker": "Narrator",\n    "content": "幽山深谷靜<br>壁畫驚成謎。",\n    "type": "Narrator"\n   },\n   "0002": {\n    "talker": "Player",\n    "content": "此洞江湖人士眾多……",\n    "type": "Dialogue",\n    "next_talks": "0003,0004"\n   },\n   "0003": {\n    "talker": "Option",\n    "content": "進入參悟",\n    "type": "Option"\n   },\n   "0004": {\n    "talker": "Option",\n    "content": "暫且不入",\n    "type": "Option"\n   },\n   "0005": {\n    "conten": "#N/A"\n   },\n   "0006": {\n    "talker": "Narrator",\n    "content": "竟已領悟了壁畫上的{0}武功",\n    "type": "Narrator"\n   }\n  }\n}\n출력예 :\n{\n  "summarize": "벽화가 있는 동굴에서 무공을 얻음, id 5번 데이터 이상",\n  "notifyId": ["0005"],\n  "0001": "고요한 유산심곡(幽山深谷)에<br>수수께끼의 벽화가 남아있다.",\n  "0002": "이 동굴에는 강호인사(江湖人士)가 많다...",\n  "0003": "진입하여 깨달음을 얻는다.",\n  "0004": "일단 들어가지 않는다.",\n  "0006": "자신도 모르게 벽화에 그려진 {0}무공을 깨달았다."\n}\n제대로 숙지했나요?'
    # first_return = "네, 중국어 무협 텍스트를 한국어로 번역하는 전문가로서 주어진 지침을 잘 숙지하였습니다. 고룡 작가의 무협 세계관을 기반으로 한 게임 스크립트를 번역할 때, 그의 특징적인 문체를 살리고 높임말과 반말, 평서체를 구분해서 사용하며, 태그와 플레이스홀더를 유지하고, 무협 세계관을 유지하기 위해 한글/한자어를 사용하고 무협 세계관의 호칭에 주의하겠습니다.\n\n이름, 지명, 무공, 물건, 별명 등은 음차하고 원문을 병기하여 사용하고, 고사성어에서 유래된 표현 등은 뜻을 번역하고 원문을 병기하겠습니다. 문법 및 표현의 자연스러움을 재확인하고, 의미가 모호한 경우 원문의 의도를 가장 잘 전달할 수 있는 표현을 선택하겠습니다.\n\n마지막으로 번역 결과를 검토하기 위해 번역된 대화문의 요약과 번역 과정 중 발견된 문제가 있는 텍스트의 ID를 나열하여 출력하겠습니다. 입출력 데이터는 유효한 json 포맷을 사용할 것입니다. 모든 지침을 준수하여 최선을 다해 번역하겠습니다."
    api_key = toml.load("localconfig.toml")["local"]["CLAUDE_API_KEY"]
    claude = Claude3Api(api_key)
    