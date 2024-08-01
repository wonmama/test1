import textwrap
import google.generativeai as genai
import streamlit as st

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

api_key = "AIzaSyBnNnRwhtqiNBrY4e2ZA4EnGgb5erBC93Y"

# few-shot 프롬프트 구성 함수 수정
def try_generate_content(api_key, prompt):
    # API 키를 설정
    genai.configure(api_key=api_key)
   
    # 설정된 모델 변경
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config={
                                      "temperature": 0.9,
                                      "top_p": 1,
                                      "top_k": 1,
                                      "max_output_tokens": 2048,
                                  },
                                  safety_settings=[
                                      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  ])
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 예외 발생시 None 반환
        print(f"API 호출 실패: {e}")
        return None

st.title("적정 기술 사례")

tech_options = [
    "태양열 조리기", "바이오가스 생산기", "로켓 스토브", "태양광 전등", "수동식 물 펌프", 
    "저비용 의족", "압축 흙 벽돌", "적정 기술 화장실", "태양광 정수기", "드럼 컴포스터", 
    "풍력 발전기", "자전거 동력 세척기", "피복 재활용 기술", "저비용 안경", "솔라키트 학교", 
    "태양열 물 히터", "휴대용 태양광 충전기", "저비용 주택 건설", "소형 수력 발전기", "저비용 냉장고"
]

selected_tech = st.selectbox("원하는 적정 기술을 선택하세요:", tech_options)

if st.button("선택한 기술에 대한 정보 보기"):
    prompt = f"적정 기술인 '{selected_tech}'의 개발배경, 장점, 단점, 개선할점, 사용 사례에 대해 알려줘."
    result = try_generate_content(api_key, prompt)
    
    if result:
        st.markdown(to_markdown(result))
    else:
        st.error("정보를 불러오지 못했습니다. 다시 시도해주세요.")
