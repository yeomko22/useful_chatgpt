import streamlit as st

from common import request_chat_completion, write_streaming_response

st.title("🧑‍💼 자기소개서 도우미")
st.markdown("자기소개서 질문과 지원자의 경험을 바탕으로 답변을 작성해줍니다. 예시를 채운 다음 자소서를 작성해보세요!")

example = {
    "company": "LG uplus",
    "position": "기업부문 B2B 국내영업",
    "max_length": 500,
    "question": "소속된 조직의 공동과업을 달성하는 과정에서 발생했던 어려움과 그 어려움을 극복하기 위해 기울인 노력에 대해 구체적인 사례를 바탕으로 기술해 주십시오.",
    "experience": "대학교 3학년 때 축구부 주장 역임.\n총장배 대회 우승이라는 공동의 목표로 함께 노력.\n주전 선수진 부상으로 어려움 겪었으나, 극복하고 8강 진출이라는 성과 달성"
}

prompt_template = """
기업 입사용 자기소개서를 작성해야합니다.
답변해야하는 질문과 이에 관련된 유저의 경험을 참고해서 자기소개서를 작성해주세요.
반드시 단락별로 소제목을 작성해주세요.
반드시 {max_length} 단어 이내로 작성해야 합니다.
---
지원 회사: {company}
지원 직무: {position}
질문: {question}
관련 경험: {experience}
---
""".strip()

auto_complete = st.toggle(label="예시로 채우기", value=False)
with st.form(f"form_{auto_complete}"):
    col1, col2, col3 = st.columns(3)
    with col1:
        company = st.text_input(
            label="지원 기업",
            placeholder="지원 기업",
            value=example["company"] if auto_complete else ""
        )
    with col2:
        position = st.text_input(
            label="지원 직무",
            placeholder="지원 직무",
            value=example["position"] if auto_complete else ""
        )
    with col3:
        max_length = st.number_input(label="최대 길이", value=500, min_value=100, max_value=2000, step=100)
    question = st.text_area(
        label="질문",
        value=example["question"] if auto_complete else "",
        placeholder="기업의 질문 문항을 채워주세요."
    )
    experience = st.text_area(
        label="질문과 관련 자신의 경험",
        placeholder="답변에 소재로 사용할 본인의 경험을 간략하게 서술해주세요.\nex) 팀장으로서 마케팅 공모전을 이끔",
        value=example["experience"] if auto_complete else ""
    )
    submit = st.form_submit_button("자소서 작성하기")

if submit:
    if not company:
        st.error("지원하는 회사를 작성해주세요.")
    elif not position:
        st.error("지원하는 직무를 작성해주세요.")
    elif not question:
        st.error("자소서 문항을 작성해주세요.")
    elif not experience:
        st.error("문항 작성에 활용할 본인의 경험을 작성해주세요.")
    else:
        prompt = prompt_template.format(
            company=company,
            position=position,
            max_length=max_length // 5,
            question=question,
            experience=experience
        )
        system_role = "당신은 전문 취업용 자기소개서 컨설턴트입니다."
        response = request_chat_completion(
            prompt=prompt,
            stream=True,
            system_role=system_role
        )
        message = write_streaming_response(response)
        st.markdown(f"**공백 포함 {len(message)}자**")
