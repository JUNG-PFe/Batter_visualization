import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import io
from PIL import Image, ImageDraw, ImageFont
import plotly.graph_objects as go
import re

# 데이터 컬러 설정
cols = {
    "직구": "#4C569B",
    "투심": "#B590C3",
    "커터": "#45B0D8",
    "슬라": "firebrick",
    "스위퍼": "#00FF00",
    "체인": "#FBE25E",
    "포크": "MediumSeaGreen",
    "커브": "orange",
    "너클": "black"
}

@st.cache_data
def load_data():
    # 데이터 URL
    data_url1 = "https://github.com/JUNG-PFe/Batter_visualization/raw/refs/heads/main/23_merged_data_%EC%88%98%EC%A0%95.xlsx"
    data_url2 = "https://github.com/JUNG-PFe/Batter_visualization/raw/refs/heads/main/24_merged_data_%EC%88%98%EC%A0%95.xlsx"
    
    # 데이터 로드
    df1 = pd.read_excel(data_url1)
    df2 = pd.read_excel(data_url2)
    
    # 날짜 형식 통일
    df1['Date'] = pd.to_datetime(df1['Date'])
    df2['Date'] = pd.to_datetime(df2['Date'])
    
    # 병합
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # 타격결과 매핑
    result_mapping = {
        "BB": "사구",
        "FL": "뜬공",
        "GR": "땅볼",
        "H1": "안타",
        "H2": "2루타",
        "H3": "3루타",
        "HR": "홈런",
        "DP": "병살타",
        "FO": "파울",
        "HI": "사구",
        "KK": "삼진",
        "SF": "희비",
        "LD": "직선타",
    }
    combined_df['타격결과'] = combined_df['타격결과'].map(result_mapping).fillna(combined_df['타격결과'])

    return combined_df

# 데이터 로드
df = load_data()

st.set_page_config(
    page_title="23-24 호크아이 데이터 선수간 비교",
    page_icon="⚾",
    layout="wide"
)

# -------------------------------
# 로그인 여부 확인
# -------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("로그인 후에 이 페이지를 이용할 수 있습니다.")
    st.stop()  # 로그인 상태가 아니면 여기서 실행 중지

st.title("호크아이 데이터 선수 간 비교분석")

# 탭 생성
tab1, tab2 = st.tabs(["선수 간 비교", "기간 간 비교"])

# -------------------
# Tab 1: 선수 간 비교
# -------------------
with tab1:
    st.subheader("선수 간 비교")

    # 선수 1과 선수 2 검색 및 선택 가로 배치
    col1, col2 = st.columns(2)

    with col1:
        # 선수 1 검색 및 선택
        search_query_1 = st.text_input("선수 1 검색", key="search_query_1").strip()
        if search_query_1:
            suggestions_1 = [name for name in sorted(df['타자'].unique()) if search_query_1.lower() in name.lower()]
        else:
            suggestions_1 = sorted(df['타자'].unique())

        if suggestions_1:
            pitcher1 = st.selectbox("선수 1 선택", suggestions_1, key="pitcher1")
        else:
            st.warning("선수 1 검색 결과가 없습니다.")
            pitcher1 = None

    with col2:
        # 선수 2 검색 및 선택
        search_query_2 = st.text_input("선수 2 검색", key="search_query_2").strip()
        if search_query_2:
            suggestions_2 = [name for name in sorted(df['타자'].unique()) if search_query_2.lower() in name.lower()]
        else:
            suggestions_2 = sorted(df['타자'].unique())

        if suggestions_2:
            pitcher2 = st.selectbox("선수 2 선택", suggestions_2, key="pitcher2")
        else:
            st.warning("선수 2 검색 결과가 없습니다.")
            pitcher2 = None

    # 구종 선택
    pitch_type = st.multiselect("구종 선택", df['구종'].unique(), key="pitch_type")
