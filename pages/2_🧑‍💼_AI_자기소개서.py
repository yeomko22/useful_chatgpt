import streamlit as st

def generate_prompt(company, position, apply_type, desired_talant, ):
    pass

st.title("🧑‍💼 기업별 맞춤형 자기소개서")
st.text("기업별 인재상과 질문에 맞춰서 자기소개서 초안을 작성해줍니다. 예시를 채운 다음 자소서 작성 버튼을 눌러보세요!")


def get_form(auto_complete=False):
    with st.form(f"form_{auto_complete}"):
        st.subheader("지원하는 회사 정보")
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
            apply_type = st.selectbox(label="지원 형태", options=["신입", "경력", "인턴"])
        example_desired_talent = """
꿈과 열정을 가지고 세계 최고에 도전하는 사람
고객을 최우선으로 생각하고 끊임없이 혁신하는 사람
팀웍을 이루며 자율적이고 창의적인 사람
꾸준히 실력을 배양하여 정정당당하게 경쟁하는 사람
    """.strip()
        desired_talant = st.text_area(
            label="지원 기업 인재상(선택)",
            placeholder="지원 기업의 인재상을 적어주세요.",
            value=example_desired_talent if auto_complete else ""
        )
        st.subheader("문항 정보")
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
            placeholder="답변에 소재로 사용할 본인의 경험을 간략하게 서술해주세요. \n ex) 팀장으로서 마케팅 공모전을 이끔",
            value=example_experience if auto_complete else ""
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            max_length = st.number_input(label="최대 길이", value=500, min_value=100, max_value=2000, step=100)
        submit = st.form_submit_button("✍️ 자소서 작성하기")


auto_complete = st.toggle(label="예시로 채우기", value=False)
get_form(auto_complete=auto_complete)
