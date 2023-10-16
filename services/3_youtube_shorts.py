import pyperclip
import requests
import streamlit as st
from bs4 import BeautifulSoup

from common import write_page_config, request_chat_completion

write_page_config()
st.title("유튜브 쇼츠 대본 생성기")
supported_reference = [
    "https://entertain.naver.com/",
    "https://n.news.naver.com/"
]
if "script" not in st.session_state:
    st.session_state.script = ""


def parse_newsurl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    if url.startswith("https://entertain.naver.com/"):
        article = soup.find("div", id="articeBody").text
    elif url.startswith("https://n.news.naver.com/"):
        article = soup.find("article").text
    else:
        raise ValueError("not supported url!")
    return article


def generate_prompt(article):
    prompt = f"""
최신 뉴스 기사가 주어집니다.
뉴스 기사를 참고해서 유튜브 쇼츠 대본을 만들어주세요.
흥미롭고 자극적으로 작성해주세요.

---
뉴스 기사: {article}
---
    """.strip()
    return prompt


auto_complete = st.toggle("예제로 채우기")
example_url = "https://entertain.naver.com/read?oid=144&aid=0000917660"
with st.form("form"):
    reference_url = st.text_input(
        label="참고할 뉴스 URL",
        value=example_url if auto_complete else ""
    )
    submit = st.form_submit_button("쇼츠 대본 만들기")

placeholder = st.empty()
if submit:
    if not reference_url:
        st.error("참고할 뉴스 URL을 입력해주세요.")
        st.stop()
    try:
        article = parse_newsurl(reference_url)
    except ValueError:
        st.error(f"""아직 지원되지 않는 URL 출처입니다. {supported_reference}로 시작하는 URL만 넣어주세요.""")
        st.stop()

    prompt = generate_prompt(article)
    system_role = f"당신은 유튜브 쇼츠를 전문으로 유투버입니다."
    response = request_chat_completion(
        system_role=system_role,
        messages=[{"role": "user", "content": prompt}]
    )
    message = ""
    for chunk in response:
        delta = chunk.choices[0]["delta"]
        if "content" in delta:
            message += delta["content"]
            placeholder.markdown(message + "▌")
        else:
            break
    placeholder.markdown(message)
    st.session_state.script = message


if st.session_state.script:
    placeholder.markdown(st.session_state.script)
    copy_button = st.button("📎 대본 복사하기")
    if copy_button:
        pyperclip.copy(st.session_state.script)
        success = st.success("클립보드에 복사했습니다!", icon="✅")
