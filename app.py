from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# --- [통계 분석 엔진] ---
def is_statistical_valid(numbers):
    # 1. 총합 합계 필터 (가장 당첨 확률이 높은 100 ~ 170 구간)
    total_sum = sum(numbers)
    if not (100 <= total_sum <= 170):
        return False
    
    # 2. 홀짝 비율 필터 (통계적으로 가장 흔한 2:4, 3:3, 4:2 비율만 허용)
    odds = len([n for n in numbers if n % 2 != 0])
    if odds not in [2, 3, 4]:
        return False
        
    return True

def generate_statistical_lotto():
    # 통계적 임계치를 만족할 때까지 무한 루프를 돌며 번호 추출
    while True:
        candidate = sorted(random.sample(range(1, 46), 6))
        if is_statistical_valid(candidate):
            return candidate

# --- [웹 라우팅] ---

# 1. 메인 화면 (접속 시 보여줄 페이지)
@app.route('/')
def index():
    # templates 폴더 안의 index.html을 띄워줍니다.
    return render_template('index.html')

# 2. 번호 생성 API (버튼 클릭 시 데이터를 보내주는 역할)
@app.route('/generate')
def generate():
    # 전문가의 추천 방식인 5게임(1세트)을 한 번에 생성합니다.
    lotto_sets = []
    for _ in range(5):
        lotto_sets.append(generate_statistical_lotto())
    
    # JSON 형태로 프론트엔드(화면)에 전달
    return jsonify({"status": "success", "data": lotto_sets})

# --- [서버 실행] ---
if __name__ == '__main__':
    # 클라우드 배포를 위해 host를 '0.0.0.0'으로 설정합니다.
    app.run(host='0.0.0.0', port=5000, debug=True)
