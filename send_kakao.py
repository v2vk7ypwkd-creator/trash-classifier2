import requests
import json
import sys
import os

TOKEN_FILE = "kakao_token.json"

# -------------------------------------------------------------
# [A] 만료된 토큰을 자동으로 만료되지 않게 갱신(Refresh)해주는 함수
# -------------------------------------------------------------
def refresh_token():
    if not os.path.exists(TOKEN_FILE):
        print(f"❌ '{TOKEN_FILE}' 파일이 없습니다.")
        return None

    with open(TOKEN_FILE, "r") as fp:
        tokens = json.load(fp)

    # 카카오 토큰 갱신 API 요청
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": "e4cc1eb9e14b3b69a40c66af369ca5e5",  # 선생님의 REST API 키
        "refresh_token": tokens["refresh_token"]
    }
    
    # 💡 만약 클라이언트 시크릿 키를 쓰신다면 아래 코드 주석(#)을 풀고 쓰세요.
    # data["client_secret"] = "tb00z9kJmEUJ3WScBG4vBq3VrKl0zkZv"

    response = requests.post(url, data=data)
    result = response.json()

    if "access_token" in result:
        # 새로 얻은 키 정보 업데이트
        tokens["access_token"] = result["access_token"]
        if "refresh_token" in result:
            tokens["refresh_token"] = result["refresh_token"]
        
        # 파일에 다시 저장
        with open(TOKEN_FILE, "w") as fp:
            json.dump(tokens, fp)
        print("🔄 [안내] 카카오 토큰이 자동으로 갱신되었습니다.")
        return tokens["access_token"]
    else:
        print("❌ 토큰 갱신 실패:", result)
        return None

# -------------------------------------------------------------
# [B] 실제 카톡 발송 함수
# -------------------------------------------------------------
def send_alert(class_name):
    access_token = refresh_token()
    if not access_token:
        return

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # 선생님 카톡으로 도달할 최종 문구!
    alert_text = f"🏫 [분리수거 체크리스트]\n\n{class_name} 분리수거 완료!"

    template_object = {
        "object_type": "text",
        "text": alert_text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "체크리스트 보기"
    }

    data = {
        "template_object": json.dumps(template_object)
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print(f"📬 [성공] '{class_name} 완료' 알림톡을 발송했습니다!")
    else:
        print("❌ 전송 실패:", response.text)

if __name__ == "__main__":
    # 학생들이 입력한 반(예: '2학년 7반') 정보를 받아와서 실행합니다.
    if len(sys.argv) > 1:
        selected_class = sys.argv[1]
    else:
        selected_class = "2학년 7반"  # 기본값
        
    send_alert(selected_class)
