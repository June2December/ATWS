from openai import OpenAI
import base64
import os
import json

# API 키 불러오기
BASE_DIR = os.path.dirname(__file__)   # day2_robot_gui/api
KEY_PATH = os.path.join(BASE_DIR, "api_key.txt")

with open(KEY_PATH, "r", encoding="utf-8") as f:
    api_key = f.read().strip()
client = OpenAI(api_key=api_key)

def get_image_description(image_path, prompt):
    with open(image_path, "rb") as f:
        image_data = f.read()
    base64_image = base64.b64encode(image_data).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            # 모델은 항상 이런 대답
            {"role": "system", "content" : "use just a few word."},
            # user(나)는 항상 이런 입력
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        tools = [
    {
        "type": "function",
        "function": {
            "name": "image_describer",
            "description": "Reasoning what this picture is.",
            "parameters": {
                "type": "object",
                "properties": {
                    "label": {"type": "string", "description":"identify label"},
                    "confidence": {"type": "number", "description":"0~1"}
                },
                "required": ["label", "confidence"]
            }
        }
    }
],
        tool_choice={"type": "function", "function":{"name":"image_describer"}}
        ,
        max_tokens=300
    )
    msg = response.choices[0].message
    print(response)
    
    
    
    if getattr(msg, "tool_calls", None):
        call = msg.tool_calls[0]
        if call.type == "function" and call.function.name == "image_describer":
            args = json.loads(call.function.arguments)  # 문자열 JSON → dict
            label = args.get("label", "unknown")
            conf = args.get("confidence")
            return f"{label}" if conf is None else f"{label} (conf:{conf:.2f})"

    # 폴백: 그래도 없으면 content 사용
    return msg.content or "(설명을 받지 못했습니다)"


    # return response.choices[0].message.content
