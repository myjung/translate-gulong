from uuid import uuid4
import re
from time import time
import hmac
import base64
import hashlib
import logging
import json
import requests
import aiohttp
import anthropic

class FreePapagoTranslator:
    def __init__(self):
        self.uuid = str(uuid4())
        self.url = "https://papago.naver.com/apis/n2mt/translate"
        self.version = self.setup_version()  # autmoatically set the version

    def setup_version(self):
        # Extract Javascript URL from Papago Page
        main_page_response = requests.get("https://papago.naver.com")
        pattern_source = re.compile(r'/vendors~main[^"]+')
        js_url_match = pattern_source.search(main_page_response.text)

        if not js_url_match:
            raise Exception("Could not find the JavaScript URL on the main page.")

        # Extract version info from javascript file
        js_url = f"https://papago.naver.com{js_url_match.group()}"
        js_response = requests.get(js_url)
        pattern_version = re.compile(r'v\d\.\d\.\d_[^"]+')
        version_match = pattern_version.search(js_response.text)

        if not version_match:
            raise Exception("Could not find the version in the JavaScript file.")

        return version_match.group()

    def generate_auth_header(self):
        timestamp = int(time() * 1000)
        data_string = f"{self.uuid}\n{self.url}\n{timestamp}"
        key = self.version.encode("utf-8")
        data = data_string.encode("utf-8")
        token = hmac.new(key, data, hashlib.md5).digest()
        encoded_token = base64.b64encode(token).decode("utf-8")
        auth_header = f"PPG {self.uuid}:{encoded_token}"
        return auth_header, timestamp

    def translate(self, text) -> dict:
        auth_header, timestamp = self.generate_auth_header()
        headers = {
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "device-type": "pc",
            "DNT": "1",
            "Accept-Language": "ko",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json",
            "Referer": "https://papago.naver.com/",
            "x-apigw-partnerid": "papago",
            "sec-ch-ua-platform": '"Windows"',
            "Authorization": auth_header,
            "Timestamp": str(timestamp),
        }

        data = {
            "locale": "ko",
            "agree": "false",
            "dict": "true",
            "dictDisplay": "30",
            "honorific": "true",
            "instant": "false",
            "paging": "false",
            "source": "zh-TW",
            "target": "ko",
            "text": text,
        }

        response = requests.post(self.url, headers=headers, data=data)
        return response.json()


async def translate_text(text, api_id: str, api_key: str, glossary_key: str = ""):
    async def make_api_request(url, headers, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                resp = await response.json()
                logging.info(
                    f"len:{len(text)},text:{text}, stat: {response.status} ,translated:{resp['message']['result']['translatedText']}"
                )
                return await response.json()

    api_endpoint = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    api_headers = {
        "X-NCP-APIGW-API-KEY-ID": api_id,
        "X-NCP-APIGW-API-KEY": api_key,
        "Content-Type": "application/json",
        "User-Agent": "local-test",
    }

    data = {"source": "zh-TW", "target": "ko", "text": text}
    if glossary_key:
        data["glossaryKey"] = glossary_key
    response = await make_api_request(api_endpoint, api_headers, data)
    translated_text = response["message"]["result"]["translatedText"]
    return translated_text


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
        return message


class GptChineseTranslator:

    def __init__(self, temperature=0.7) -> None:
        import tiktoken
        import openai

        self.client = openai.OpenAI() # api key is in the system environment
        self.encoding = tiktoken.encoding_for_model("gpt-4-turbo-preview")
        self.max_tokens = 4095  # max token limit
        self.temperature = temperature

    def calculate_tokens(self, content: str) -> int:
        """Calculate the total number of tokens for the messages."""
        tokens = len(self.encoding.encode(content))
        return tokens

    def translate(self, prompt: str, scripts: list[str], context: str = "") -> list:
        messages = [
            {
                "role": "user",
                "content": PROMPT,
            },
            {
                "role": "assistant",
                "content": "네 번역할 데이터를 입력해주세요.",
            },
        ]

        if context:
            user_req = {"context": context, "texts": scripts}
        else:
            user_req = {"texts": scripts}

        translation_request = json.dumps(user_req, ensure_ascii=False)
        messages.append({"role": "user", "content": translation_request})

        req_tokens = self.calculate_tokens(translation_request)
        logging.info(f"req_token : {req_tokens}")
        if req_tokens > 1700:
            logging.error("Total token count exceeds the limit.")
            return []

        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        if len(response.choices) > 0:
            logging.info(
                f"Response ID: {response.id}, finish:{response.choices[0].finish_reason} ,com_token: {response.usage.completion_tokens}, pmpt_token: {response.usage.prompt_tokens}"
            )
            translated_contents = response.choices[0].message.content
            try:
                # 응답 내용에서 번역된 텍스트 추출 및 반환
                return json.loads(translated_contents)
            except json.JSONDecodeError:
                logging.error("Failed to decode translated content.")
                return []

        return []


if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        filename="translator.log",
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    PROMPT = """\
Your mission is Translate Chinese to Korean thinking deeply about meaning between the lines:

- Proper Nouns: Replace with "<r>(original)</r>", including in tags.
- Preserve: HTML tags (<br>, <color>), placeholders ({0}), special characters, numbers, English letters. Only translate text within tags.
- Tone: Keep neutral, martial arts-friendly.
- Format: JSON {"context":"...", "texts":["..."]}; "context" optional.
- Output: ["translated content", ...], ensuring no omissions.
- double quote in translated content need to escape("->\\")

Example
Original: {"context":"dialogues", "texts":["確實"味"道很好……<color=#FF0000>看來阿飛下了很多苦功練習啊。<color>","那快活王竟曾有個名字，叫做<color=#FF0000>柴玉關</color>。"]}
Expected Output: ["확실히 \\"맛\\"이 매우 좋네...<color=#FF0000><r>(阿飛)</r>가 열심히 연습했나 보네<color>.","그 쾌활왕에게는 이름이 있었어, 바로 <color=#FF0000><r>柴玉關</r></color>이었다."]"""
    translator = GptChineseTranslator()
    print(PROMPT)
