import streamlit as st

from scrape import scrape
from generate_calendar import generateCalendar


def main():

    with st.form("my_form", clear_on_submit=False):

        stu_id = st.number_input('学籍番号(先頭にsは不要です)',2000000, 3000000, 2000000, step=1)
        password = st.text_input('パスワード', type="password")
        submitted = st.form_submit_button("カレンダーを作成")

    # ボタンを押した時の処理
    if submitted:
        with st.spinner('カレンダー取得中'):

            # 時間割の取得
            jikanwari = scrape(stu_id, password)

            # カレンダー作成
            calendar = generateCalendar(jikanwari)

            # ファイルダウンロード
            st.download_button(label="カレンダーをダウンロード", data=calendar, file_name="myCalendar.ics")


if __name__ == '__main__':
    main()