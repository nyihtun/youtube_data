from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import re
import streamlit as st

# data = []


def gather_data(url_input):
    return home_page(url_input) | about_page(url_input)


def home_page(url_input):
    try:
        url_opener = urlopen(
            Request(url_input, headers={'User-Agent': 'Chrome', 'Accept-Language': 'en-US,en;q=0.5'}))
        soup = bs(url_opener, features="html.parser")

        return dict(
            channel_id=channel_id(soup),
            sub_count=sub_count(soup)
        )
    except Exception as e:
        return e


def about_page(url_input):
    try:
        url_input_about = url_input + "/about"
        url_opener = urlopen(Request(url_input_about, headers={
                             'User-Agent': 'Chrome', 'Accept-Language': 'en-US,en;q=0.5'}))
        soup = bs(url_opener, features="html.parser")

        return dict(
            views=views(soup),
            description=description(soup),
            location=location(soup),
            joined_date=joined_date(soup)
        )
    except Exception as e:
        return e


def channel_id(soup):
    try:
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


def sub_count(soup):
    try:
        result_sub = soup.find(string=re.compile("subscriberCountText"))

        last_found = None
        for m in re.finditer('subscriberCountText', str(result_sub)):
            last_found = m.start()

        if last_found is None:
            return "Unknown subscriber count"

        aft_subscriber_count_text = result_sub[last_found:]
        simple_text = aft_subscriber_count_text[aft_subscriber_count_text.find(
            "simpleText")+13:]

        return simple_text.split(" ")[0].replace(",", ".")
    except Exception as e:
        return e


def views(soup):
    try:
        result = soup.find(string=re.compile("viewCountText"))

        last_found = None
        for m in re.finditer('viewCountText', str(result)):
            last_found = m.start()

        if last_found is None:
            return "Unknown viewer count"

        aft_view_count = result[last_found+30:]

        view_count_text = aft_view_count.split(" ")[0]

        # data.append(dict(view_count=view_count_text.replace(".", ",")))
        return view_count_text.replace(".", ",")
    except Exception as e:
        return e


def description(soup):
    try:
        result = soup.find(string=re.compile(
            '"channelAboutFullMetadataRenderer":{"description":{"'))

        if result is None:
            return "Description N/A"

        last_found = None
        for m in re.finditer('channelAboutFullMetadataRenderer', str(result)):
            last_found = m.start()

        if last_found is None:
            return "Description N/A"

        text_begins = result[last_found+64:]

        text_found = text_begins.split('"}')[0]

        return text_found
    except Exception as e:
        return e


def location(soup):
    try:
        result = soup.find(string=re.compile(
            '"country":{"simpleText"'))

        if result is None:
            return "Location N/A"

        last_found = None
        for m in re.finditer('"country":{"simpleText"', str(result)):
            last_found = m.start()

        if last_found is None:
            return "Location N/A"

        text_begins = result[last_found+25:]

        text_found = text_begins.split('"}')[0]

        return text_found
    except Exception as e:
        return e


def joined_date(soup):
    try:
        result = soup.find(string=re.compile(
            'joinedDateText'))

        if result is None:
            return "Joined date N/A"

        last_found = None
        for m in re.finditer('joinedDateText', str(result)):
            last_found = m.start()

        if last_found is None:
            return "Joined date N/A"

        text_begins = result[last_found+53:]

        text_found = text_begins.split('"}')[0]

        return text_found
    except Exception as e:
        return e


# url_input = "https://www.youtube.com/@dailysquare8511"
# url_input_about = url_input + "/about"
# url_opener = urlopen(Request(url_input_about, headers={
#                              'User-Agent': 'Chrome', 'Accept-Language': 'en-US,en;q=0.5'}))
# soup = bs(url_opener, features="html.parser")
# print(joined_date(soup))

# print(gather_data("https://www.youtube.com/@dailysquare8511"))  # with desc
# print(gather_data("https://www.youtube.com/@myanmargossip6519"))  # without desc

with st.form("my_form", clear_on_submit=True):
    url = st.text_input(
        'Youtube URL:', placeholder='https://www.youtube.com/@theone2871')

    submitted = st.form_submit_button("Submit")
    if submitted:
        if not url.strip():
            st.write("URL is missing")
        else:
            st.write(url)
            with st.spinner(text='Extracting data…'):
                data = gather_data(url)

                st.write(data["channel_id"])
                st.write(data["description"])
                st.write(data["sub_count"])
                st.write(data["joined_date"])
                st.write(data["views"])
                st.write(data["location"])
