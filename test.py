#Web VPython 3.2
from vpython import *
import random

# 환경 설정
scene.title = "분리수거 시뮬레이션"
scene.background = vector(1, 1, 1)  # 배경색 설정

# 분류 박스 생성 (파스텔톤)
boxes = {
    '종이': box(pos=vector(-4, 0, 0), size=vector(1, 1, 1), color=vector(0.85, 0.68, 0.45)),  # 부드러운 갈색
    '플라스틱': box(pos=vector(-2, 0, 0), size=vector(1, 1, 1), color=vector(0.68, 0.85, 0.85)),  # 부드러운 청록색
    '비닐': box(pos=vector(0, 0, 0), size=vector(1, 1, 1), color=vector(0.85, 1, 0.85)),  # 부드러운 초록색
    '캔': box(pos=vector(2, 0, 0), size=vector(1, 1, 1), color=vector(1, 0.68, 0.68))   # 부드러운 빨간색
}

# 박스 이름 표시
labels = {
    '종이': label(pos=vector(-4, 1.2, 0), text='종이', height=12, color=vector(0, 0, 0)),
    '플라스틱': label(pos=vector(-2, 1.2, 0), text='플라스틱', height=12, color=vector(0, 0, 0)),
    '비닐': label(pos=vector(0, 1.2, 0), text='비닐', height=12, color=vector(0, 0, 0)),
    '캔': label(pos=vector(2, 1.2, 0), text='캔', height=12, color=vector(0, 0, 0))
}

# 쓰레기 아이템 생성 (어려운 아이템 추가)
items = [
    ('신문지', '종이'),
    ('페트병', '플라스틱'),
    ('비닐봉지', '비닐'),
    ('캔', '캔'),
    ('종이컵', '종이'),
    ('플라스틱 용기', '플라스틱'),
    ('알루미늄 캔', '캔'),
    ('과자 봉지', '비닐'),
    ('종이 상자', '종이'),
    ('우유 팩', '종이'),  # 어려운 아이템
    ('식용유 페트병', '플라스틱'),  # 어려운 아이템
    ('스티로폼 용기', '비닐'),  # 어려운 아이템
    ('세제 용기', '플라스틱'),  # 어려운 아이템
    ('포장지', '종이'),  # 어려운 아이템
    ('유리병', '캔'),  # 어려운 아이템
    ('비닐 포장재', '비닐'),  # 어려운 아이템
    ('페인트 통', '캔')  # 어려운 아이템
]

# 게임 시작
def create_trash():
    if items:
        item = random.choice(items)
        items.remove(item)  # 선택한 아이템 제거
        trash = sphere(pos=vector(3, 0, 0), radius=0.2, color=vector(1, 1, 1))  # 흰색 쓰레기
        trash_label = label(pos=trash.pos, text=item[0], height=12, color=vector(0, 0, 0))  # 물건 이름 레이블
        return trash, item[1], trash_label  # 물건과 종류, 레이블
    else:
        return None, None, None  # 더 이상 아이템이 없으면 None 반환

trash, correct_type, trash_label = create_trash()

# 점수와 시행 횟수 초기화
score = 0
attempts = 0

# 사용자가 클릭할 때 처리
def mouse_click(evt):
    global trash, correct_type, score, trash_label, attempts
    mouse_pos = scene.mouse.pos.x

    # 박스 간격에 맞게 클릭 위치 판단
    if mouse_pos < -3.5:  # 종이 박스
        user_type = '종이'
    elif mouse_pos < -1.5:  # 플라스틱 박스
        user_type = '플라스틱'
    elif mouse_pos < 0.5:  # 비닐 박스
        user_type = '비닐'
    elif mouse_pos < 2.5:  # 캔 박스
        user_type = '캔'
    else:
        return  # 클릭이 유효하지 않음

    attempts += 1  # 시도 횟수 증가

    if user_type == correct_type:
        print(f"정확히 분리수거되었습니다! '{trash_label.text}'가 {correct_type}로 분리되었습니다.")
        score += 1  # 점수 증가
        score_display.text = f"점수: {score}"  # 점수 업데이트
    else:
        print(f"잘못된 분리수거! '{trash_label.text}'는 {correct_type}입니다.")
    
    trash.visible = False  # 쓰레기 객체 숨기기
    trash_label.visible = False  # 레이블 숨기기
    trash, correct_type, trash_label = create_trash()  # 새로운 쓰레기 생성

    # 15번 시행 후 결과 출력
    if attempts >= 15:
        if score >= 10:
            print("당신은 분리수거 고수!😎 앞으로도 환경을 위해 열심히 분리수거 해주세요😊")
        else:
            print("당신은 분리수거 허수ㅡㅡ 올바른 분리수거 방법을 배워보세요😎")
        scene.unbind('click', mouse_click)  # 클릭 이벤트 해제

# 점수 디스플레이
score_display = label(pos=vector(0, 2, 0), text=f"점수: {score}", height=20, color=vector(0, 0, 0))

# 마우스 클릭 이벤트 등록
scene.bind('click', mouse_click)

# 계속해서 실행
while True:
    rate(60)