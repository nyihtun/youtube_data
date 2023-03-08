from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import re
import streamlit as st

url_input = "https://www.youtube.com/@theone2871"

data = []


def channel_id(url_input):
    try:
        url_opener = urlopen(
            Request(url_input, headers={'User-Agent': 'Chrome'}))
        soup = bs(url_opener, features="html.parser")

        result = soup.find(href=re.compile("channel_id"))
        # for result in results:
        href = result.get('href')
        if not href == None:
            # data.append(dict(channel_id=href.split("=")[1]))
            return href.split("=")[1]
        else:
            # data.append(dict(channel_id="N/A"))
            return "N/A"
    except Exception as e:
        return e


def sub_count(url_input):
    try:
        url_opener = urlopen(
            Request(url_input, headers={'User-Agent': 'Chrome'}))
        soup = bs(url_opener, features="html.parser")

        result_sub = soup.find(string=re.compile("subscriberCountText"))

        aft_subscriber_count_text = result_sub[result_sub.find(
            "subscriberCountText"):]
        simple_text = aft_subscriber_count_text[aft_subscriber_count_text.find(
            "simpleText")+13:]

        # sub_count = simple_text.split(" ")[0].replace(",", ".")

        # data.append(dict(sub_count=sub_count))
        return simple_text.split(" ")[0].replace(",", ".")
    except Exception as e:
        return e


def views(url_input):
    try:
        url_input_about = url_input + "/about"
        url_opener = urlopen(
            Request(url_input_about, headers={'User-Agent': 'Chrome'}))
        soup = bs(url_opener, features="html.parser")

        results = soup.find(string=re.compile("viewCountText"))

        aft_view_count = results[results.find("viewCountText")+30:]

        view_count_text = aft_view_count.split(" ")[0]

        # data.append(dict(view_count=view_count_text.replace(".", ",")))
        return view_count_text.replace(".", ",")
    except Exception as e:
        return e


with st.form("my_form", clear_on_submit=True):
    url = st.text_input(
        'Youtube URL:', placeholder='https://www.youtube.com/@theone2871')

    submitted = st.form_submit_button("Submit")
    if submitted:
        if not url.strip():
            st.write("URL is missing")
        else:
            with st.spinner(text='Extracting data…'):
                st.write("Channel id:", channel_id(url))
                st.write("Subscriber count:", sub_count(url))
                st.write("Viewer count:", views(url))
