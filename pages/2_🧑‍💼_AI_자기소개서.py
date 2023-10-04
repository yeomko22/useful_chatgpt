import openai
import streamlit as st

st.title("🧑‍💼 기업별 맞춤형 자기소개서")
st.text("기업별 인재상과 질문에 맞춰서 자기소개서 초안을 작성해줍니다. 예시를 채운 다음 자소서 작성 버튼을 눌러보세요!")
openai.api_key = st.secrets["OPENAI_API_KEY"]


def request_chat_completion(messages, system_role=None):
    if system_role:
        messages = [{"role": "system", "content": system_role}] + messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
        timeout=3
    )
    return response


def generate_prompt(company, position, question, experience, max_length):
    prompt = f"""
기업 입사용 자기소개서를 작성해야합니다.
답변해야하는 질문과 이에 관련된 유저의 경험을 참고해서 자기소개서를 작성해주세요.
반드시 공백을 포함해서 {max_length}자 이내로 작성해주세요.
---
지원 회사: {company}
지원 직무: {position}
질문: {question}
관련 경험: {experience}
---
    """.strip()
    return prompt


def print_streaming_response(response):
    message = ""
    placeholder = st.empty()
    for chunk in response:
        delta = chunk.choices[0]["delta"]
        if "content" in delta:
            message += delta["content"]
            placeholder.markdown(message + "▌")
        else:
            break
    placeholder.markdown(message)
    return message


auto_complete = st.toggle(label="예시로 채우기", value=False)
with st.form(f"form_{auto_complete}"):
    col1, col2, col3 = st.columns(3)
    with col1:
        example_company = "LG uplus"
        company = st.text_input(
            label="지원 기업",
            placeholder="지원 기업",
            value=example_company if auto_complete else ""
        )
    with col2:
        example_position = "기업부문 B2B 국내영업"
        position = st.text_input(
            label="지원 직무",
            placeholder="지원 직무",
            value=example_position if auto_complete else ""
        )
    with col3:
        max_length = st.number_input(label="최대 길이", value=500, min_value=100, max_value=2000, step=100)
    example_question = "소속된 조직의 공동과업을 달성하는 과정에서 발생했던 어려움과 그 어려움을 극복하기 위해 기울인 노력에 대해 구체적인 사례를 바탕으로 기술해 주십시오."
    question = st.text_area(
        label="질문",
        value=example_question if auto_complete else ""
    )
    example_experience = """
대학교 3학년 때 축구부 주장 역임
총장배 대회 우승이라는 공동의 목표로 함께 노력. 
주전 선수진 부상으로 어려움 겪었으나, 극복하고 8강 진출이라는 성과 달성
""".strip()
    experience = st.text_area(
        label="질문과 관련 자신의 경험",
        placeholder="답변에 소재로 사용할 본인의 경험을 간략하게 서술해주세요.\nex) 팀장으로서 마케팅 공모전을 이끔",
        value=example_experience if auto_complete else ""
    )
    submit = st.form_submit_button("✍️ 자소서 작성하기")

if submit:
    prompt = generate_prompt(company, position, question, experience, max_length)
    with st.spinner("답변 생성 중..."):
        response = request_chat_completion(messages=[{"role": "user", "content": prompt}])
    message = print_streaming_response(response)
    st.markdown(f"**공백 포함 {len(message)}자**")
