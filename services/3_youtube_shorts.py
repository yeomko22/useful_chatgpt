import requests
import streamlit as st
from bs4 import BeautifulSoup
from common import request_chat_completion, write_streaming_response

prompt_template = """
최신 연예 뉴스 기사가 주어집니다.
뉴스 기사를 참고해서 유튜브 쇼츠 영상 대본을 만들어주세요.
각 단락마다 영상에 소개될 이미지나 영상 클립을 묘사해주세요.
각 단락별 대본은 3문장으로 짧게 작성해주세요. 
10대 소녀가 친구에게 말하는 듯한 말투로 작성해주세요.

아래 포맷으로 작성해주세요.
[제목] <제목 텍스트>\n\n
[클립] <영상에서 보여줄 이미지나 영상에 대한 묘사>\n
[대본] <나레이션 방식의 대본>\n
[클립] <영상에서 보여줄 이미지나 영상에 대한 묘사>\n
[대본] <나레이션 방식의 대본>\n
...
---
뉴스 기사: {article}
---
""".strip()


def parse_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    article = soup.find("div", id="articeBody").text
    return article.strip()


st.title("유튜브 쇼츠 대본 생성기")
st.text("네이버 연예 뉴스 URL을 넣어주면 유튜브 쇼츠용 대본을 생성합니다.")
auto_complete = st.toggle("예제로 채우기")
example_url = "https://entertain.naver.com/read?oid=144&aid=0000917660"
with st.form("form"):
    reference_url = st.text_input(
        label="참고할 뉴스 URL",
        value=example_url if auto_complete else ""
    )
    submit = st.form_submit_button("쇼츠 대본 만들기")
if submit:
    if not reference_url:
        st.error("참고할 뉴스 URL을 넣어주세요.")
    elif not reference_url.startswith("https://entertain.naver.com/"):
        st.error("지원되지 않는 URL입니다.")
    else:
        article = parse_article(reference_url)
        prompt = prompt_template.format(article=article)
        system_role = "당신은 쇼츠 전문 유투버입니다."
        response = request_chat_completion(prompt, stream=True, system_role=system_role)
        message = write_streaming_response(response)

        st.divider()
        st.subheader("복사용 대본")
        scripts = [x for x in message.split("\n") if x.startswith("[대본]")]
        for script in scripts:
            st.markdown(script.replace("[대본]", "").strip())
