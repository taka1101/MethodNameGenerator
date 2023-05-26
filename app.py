import openai
import streamlit as st

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なプログラミング講師です。"}
        ]

# ChatGPTとやり取りする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["prompt"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    # 入力欄を消去
    st.session_state["user_input"] = ""
    st.session_state["prompt"] = ""

# ユーザーインターフェイスの構築
st.title("メソッド名ジェネレーター")
st.write("プロンプトを入力せずに関数名や変数名を自動生成する")

# OpenAI API Keyの取得
user_api_key = st.text_input("OpenAI API Keyを入力してください。", key="user_api_key", type="password")
openai.api_key = user_api_key

# 開発言語選択
programming_language = ["C/C++", "Java", "Python", "Kotlin", "Swift"]
selected_language = st.selectbox("開発言語を選択してください", programming_language)

# 関数 or 変数
method = ["関数名", "変数名"]
selected_method = st.radio("作成する項目を選択してください。", method)

# メソッドの動作や役割入力
user_input = st.text_area("メソッドの動作や役割を入力してください。", key="user_input")

# ボタンの有効/無効状態を管理する変数を初期化する
button_enabled = False
# OpenAI API Keyが入力された場合にボタンを有効にする
if user_api_key:
    button_enabled = True
# ボタンを表示する
generate_button = st.button("Generate!", key="generate_button", disabled=not button_enabled, on_click=communicate)

# プロンプト生成
if selected_method == "関数名":
    st.session_state["prompt"] = selected_language + "で「" + user_input + "」という処理を行う関数名の候補をいくつか教えてください"
else:
    st.session_state["prompt"] = selected_language + "で「" + user_input + "」という役割の変数名の候補をいくつか教えてください"

"---"

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    # 直近のメッセージを上に
    for message in reversed(messages[1:]):
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
