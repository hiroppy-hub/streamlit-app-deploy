import streamlit as st
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# .envからAPIキーを読み込む
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LangChainのChatOpenAIインスタンスを作成
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo",
    temperature=0.7,
)

# 専門家ごとのシステムメッセージ
EXPERT_SYSTEM_MESSAGES = {
    "歴史家": "あなたは優秀な歴史家です。分かりやすく、正確に解説してください。",
    "ITコンサルタント": "あなたは経験豊富なITコンサルタントです。専門的かつ分かりやすく説明してください。",
    "医師": "あなたは信頼できる医師です。専門知識を活かして丁寧に回答してください。",
}

def run_llm(user_input: str, expert: str) -> str:
    """入力テキストと専門家の種類をもとにOpenAI APIで回答を生成"""
    system_message = SystemMessage(EXPERT_SYSTEM_MESSAGES.get(expert, "あなたは優秀な専門家です。"))
    human_message = HumanMessage(user_input)
    response = llm([system_message, human_message])
    return response.content

# Streamlit UI
st.title("専門家AIチャットアプリ")
st.write(
    """
    このアプリは、選択した専門家になりきったAIがあなたの質問に回答します。
    専門家の種類を選び、質問を入力して「送信」ボタンを押してください。
    """
)

user_input = st.text_input("質問を入力してください")
expert = st.radio(
    "専門家を選択してください",
    list(EXPERT_SYSTEM_MESSAGES.keys()),
    index=0
)

if st.button("送信"):
    if user_input.strip():
        with st.spinner("AIが回答中..."):
            answer = run_llm(user_input, expert)
        st.markdown("#### 回答")
        st.write(answer)
    else:
        st.warning("質問を入力してください。")

st.divider()

st.title("サンプルアプリ②: 少し複雑なWebアプリ")

st.write("##### 動作モード1: 文字数カウント")
st.write("入力フォームにテキストを入力し、「実行」ボタンを押すことで文字数をカウントできます。")
st.write("##### 動作モード2: BMI値の計算")
st.write("身長と体重を入力することで、肥満度を表す体型指数のBMI値を算出できます。")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["文字数カウント", "BMI値の計算"]
)

st.divider()

if selected_item == "文字数カウント":
    input_message = st.text_input(label="文字数のカウント対象となるテキストを入力してください。")
    text_count = len(input_message)

else:
    height = st.text_input(label="身長（cm）を入力してください。")
    weight = st.text_input(label="体重（kg）を入力してください。")

if st.button("実行"):
    st.divider()

    if selected_item == "文字数カウント":
        if input_message:
            st.write(f"文字数: **{text_count}**")

        else:
            st.error("カウント対象となるテキストを入力してから「実行」ボタンを押してください。")

    else:
        if height and weight:
            try:
                bmi = round(int(weight) / ((int(height)/100) ** 2), 1)
                st.write(f"BMI値: {bmi}")

            except ValueError as e:
                st.error("身長と体重は数値で入力してください。")

        else:
            st.error("身長と体重をどちらも入力してください。")


