import os
import requests
import sys

def send_kakao_message():
    # 깃허브 Secrets에 등록한 API 키를 가져옵니다.
    api_key = os.environ.get("KAKAO_API_KEY")
    
    if not api_key:
        print("에러: KAKAO_API_KEY를 찾을 수 없습니다. GitHub Secrets 설정을 확인해 주세요.")
        sys.exit(1)
        
    # 실행할 때 입력받은 학급 이름을 가져옵니다. (기본값: '2학년 7반')
    # 깃허브 액션에서 값을 넘겨받을 때 사용합니다.
    class_name = sys.argv[1] if len(sys.argv) > 1 else "2학년 7반"

    # 카카오톡 메시지 전송 API 주소 (나에게 보내기 기준)
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # 보낼 메시지 내용 설정
    payload = {
        "template_object": f'{{"object_type": "text", "text": "[쓰레기 분류 완료]\\n{class_name}에서 쓰레기 분류가 완료되었습니다!", "link": {{"web_url": "https://v2vk7ypwkd-creator.github.io/trash-classifier2/", "mobile_web_url": "https://v2vk7ypwkd-creator.github.io/trash-classifier2/"}}}}'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        print("🎉 카카오톡 메시지 전송 성공!")
    else:
        print(f"❌ 전송 실패! 에러 코드: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    send_kakao_message()
