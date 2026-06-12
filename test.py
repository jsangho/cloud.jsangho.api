import ollama
from kiwipiepy import Kiwi

# 1. 한국어 형태소 분석기 Kiwi 초기화
kiwi = Kiwi()


def run_korean_ai(user_text):
    print("\n--- [1단계] 입력 문장 전처리 중... ---")

    # kiwipiepy를 활용한 가벼운 전처리 예시 (띄어쓰기 오차 보정)
    kiwi.global_config.space_tolerance = 2
    cleaned_text = kiwi.space(user_text, reset_whitespace=True)
    print(f"원본 문장: {user_text}")
    print(f"정제된 문장: {cleaned_text}")

    # 형태소 분석 결과 예시 출력 (명사만 추출해보기)
    tokens = kiwi.tokenize(cleaned_text)
    nouns = [t.form for t in tokens if t.tag.startswith('NN')]
    print(f"추출된 핵심 명사: {nouns}")

    print("\n--- [2단계] Qwen2.5 3B 모델 추론 중... ---")

    # 2. Ollama에 설치된 qwen2.5:3b 모델에 질문 던지기
    response = ollama.chat(
        model='qwen2.5:3b',
        messages=[
            {
                'role': 'user',
                'content': cleaned_text
            }
        ]
    )

    # 3. 결과 반환
    return response['message']['content']


# 실제 실행 테스트
if __name__ == "__main__":
    question = "영화 타이타닉의 주요 등장인물과 그들의 역할을 설명해줘."
    answer = run_korean_ai(question)

    print("\n--- [3단계] AI 최종 답변 ---")
    print(answer)
