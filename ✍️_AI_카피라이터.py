import openai
import streamlit as st

st.set_page_config(page_title="칼퇴를 부르는 chatGPT 활용법", page_icon="✨")

st.title("✍️ AI_카피라이터")
st.subheader("AI를 이용하여 손쉽게 마케팅 문구를 생성해요.")
openai.api_key = st.secrets["OPENAI_TOKEN"]


def request_chat_completion(messages, system_role, buffersize: int = 8):
    if len(messages) > buffersize:
        messages = messages[-buffersize:]
    if system_role:
        messages = [{"role": "system", "content": system_role}] + messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
        timeout=3
    )
    return response


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


def generate_prompt(name, description, max_length, generate_num, keywords):
    prompt = f""" 
제품 혹은 브랜드를 SNS에 광고하기 위한 문구를 {generate_num}개 생성해주세요.
키워드가 주어질 경우, 반드시 키워드 중 하나를 포함해야 합니다.
반드시 {max_length} 단어 이내로 작성해주세요.
창의적이고 자극적으로 작성하세요.
명사 위주로 간결하게 작성하세요.
완결된 문장이 아니라도 괜찮습니다.
절대로 해쉬태그를 사용하지 마세요.
---
제품/브랜드 이름: {name}
제품 간단 정보: {description}
---
키워드: {keywords}
"""
    return prompt.strip()


with st.form("form"):
    col1, col2, col3 = st.columns([0.5, 0.25, 0.25])
    with col1:
        name = st.text_input("제품/브랜드 이름(필수)")
    with col2:
        max_length = st.number_input("최대 단어 수", min_value=5, max_value=20, step=1, value=10)
    with col3:
        generate_num = st.number_input("생성할 문구 수", min_value=1, max_value=10, step=1, value=5)
    desc = st.text_input("제품 간단 정보(필수)")

    st.text("포함할 키워드(최대 3개까지 허용)")
    col1, col2, col3 = st.columns(3)
    with col1:
        keyword_one = st.text_input(placeholder="키워드 1", label="keyword_1", label_visibility="collapsed")
    with col2:
        keyword_two = st.text_input(placeholder="키워드 2", label="keyword_2", label_visibility="collapsed")
    with col3:
        keyword_three = st.text_input(placeholder="키워드 3", label="keyword_3", label_visibility="collapsed")
    submitted = st.form_submit_button("Submit")
if submitted:
    if not name:
        st.error("브랜드 혹은 제품의 이름을 입력해주세요")
    elif not desc:
        st.error("제품의 간단한 정보를 입력해주세요")
    else:
        with st.spinner('AI 카피라이터가 광고 문구를 생성 중입니다...'):
            keywords = [keyword_one, keyword_two, keyword_three]
            keywords = [x for x in keywords if x]
            prompt = generate_prompt(name, desc, max_length, generate_num, keywords)
            system_role = "당신은 전문 카피라이터입니다."
            response = request_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                system_role=system_role
            )
        print_streaming_response(response)
