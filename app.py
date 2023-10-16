import streamlit as st
from st_pages import show_pages_from_config

from common import write_page_config, print_streaming_message

show_pages_from_config()
write_page_config()
st.title("🧠 chatGPT API로 AI 서비스 개발하기")
st.markdown("")
welcome_message = """
매일 내가 물어보는 것들을 답해주는 우리 친구 chatGPT!  
그런덴 chatGPT를 이용해서 나만의 서비스를 만들어 볼 수 있다고?

퍼펭스쿨이 야심차게 준비한 **chatGPT API로 AI 서비스 개발하기** 과정!

내가 원하는 대로 chatGPT가 텍스트를 생성하도록 제어하는 기술을 배워봅니다.  
그리고 다른 사람들도 이용할 수 있게 서비스로 만들어 봅니다.

저와 함께 chatGPT로 만들 수 있는 서비스의 무한한 가능성을 살펴보러 가시죠!
"""

if "first_visit" not in st.session_state:
    st.session_state.first_visit = False

if st.session_state.first_visit:
    print_streaming_message(welcome_message)
    st.session_state.first_visit = False
else:
    st.markdown(welcome_message)

st.markdown("""
<style>
[data-testid="stMarkdownContainer"] a {
    padding: 10px;
    border-radius: 10px;
    border: 1px solid;
    border-color: #e0e0e2;
    color: black;
    text-decoration: none; 
}
[data-testid="stMarkdownContainer"] a:hover {
    color: #FF4B4B;
    border-color: #FF4B4B;
}
</style>
""", unsafe_allow_html=True)

st.subheader("실습 프로젝트")
service_data_list = [
    {
        "title": "✍️ 마케팅 문구 생성기",
        "description": "브랜드와 키워드, 단어 수 등을 넣으면 마케팅 문구를 생성해주는 프로젝트입니다.",
        "url": "마케팅 문구 생성기",
        "image": "./images/ch1_thumbnail.png"
    },
    {
        "title": "🧑‍💼 자기소개서 도우미",
        "description": "내 경험을 토대로 자기소개서 문항을 작성해줍니다.",
        "url": "자기소개서 도우미",
        "image": "./images/ch2_thumbnail.png"
    },
    {
        "title": "▶️ 유튜브 쇼츠 대본 생성기",
        "description": "최신 뉴스 기사를 소재로 유튜브 쇼츠 대본을 만들어줍니다.",
        "url": "유튜브 쇼츠 대본 생성기",
        "image": "./images/ch3_thumbnail.png"
    },
]

tabs = st.tabs([x["title"] for x in service_data_list])
for i, tab in enumerate(tabs):
    with tab:
        service_data = service_data_list[i]
        st.text(service_data["description"])
        st.image(service_data["image"])
        url = service_data["url"]
        st.markdown(f'<a href="/{url}" target="_self">사용해보러 가기</a>', unsafe_allow_html=True)
