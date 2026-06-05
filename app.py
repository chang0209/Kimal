import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import cv2
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="만화 대사 전문 번역 앱", layout="wide", initial_sidebar_state="expanded")

st.title("📚 만화 대사 전문 번역 앱 (Prototype)")
st.caption("기획안 내용을 기반으로 제작된 기능 및 UI 검증용 프로토타입입니다.")
st.markdown("---")

# 2. 사이드바 - 이미지 업로드 및 설정
st.sidebar.header("📁 이미지 업로드 및 옵션")
uploaded_file = st.sidebar.file_uploader("만화 원서 이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

# 화질 제한 기준 설정 (기획서 반영)
MIN_RESOLUTION = 400
upscale_option = st.sidebar.checkbox("🚀 번역 완료 후 이미지 화질 업스케일링 적용", value=True)

# 3. 메인 로직
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    width, height = image.size
    st.sidebar.info(f"📊 이미지 정보: {width}x{height} (가로x세로)")

    if width < MIN_RESOLUTION or height < MIN_RESOLUTION:
        st.error("❌ **번역 불가 (실패 케이스)**")
        st.warning(f"이유: 화질이 특정 수준 이하입니다. (현재 해상도: {width}x{height} / 제한 기준: {MIN_RESOLUTION}px 이상)")
    elif width > height * 1.1:
        st.error("❌ **번역 불가 (실패 케이스)**")
        st.warning("이유: 두 페이지 이상 늘려놓은 형식의 이미지이거나 가로형 이미지입니다.")
    else:
        st.success("✅ **번역 가능 이미지 확인 (성공 케이스)**")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🖼️ 원본 이미지 및 말풍선 감지")
            img_np = np.array(image)
            box1 = [int(width*0.6), int(height*0.1), int(width*0.9), int(height*0.3)]
            box2 = [int(width*0.1), int(height*0.5), int(width*0.4), int(height*0.7)]
            cv2.rectangle(img_np, (box1[0], box1[1]), (box1[2], box1[3]), (0, 0, 255), 3)
            cv2.rectangle(img_np, (box2[0], box2[1]), (box2[2], box2[3]), (255, 0, 0), 3)
            st.image(img_np, caption="말풍선 자동 판별 완료", use_column_width=True)
            bubble_choice = st.selectbox("💬 번역하고 싶은 특정 말풍선을 선택하세요", ["전체 번역하기", "말풍선 1 (우측 상단)", "말풍선 2 (좌측 중앙)"])
        with col2:
            st.subheader("✨ 번역 및 보정 결과")
            if st.button("🔄 번역 시작하기"):
                with st.spinner("가독성을 개선하여 대사 번역 중..."):
                    time.sleep(1.5)
                res_img = image.copy()
                draw = ImageDraw.Draw(res_img)
                if bubble_choice in ["전체 번역하기", "말풍선 1 (우측 상단)"]:
                    draw.rectangle([box1[0], box1[1], box1[2], box1[3]], fill="white")
                    st.info("📝 **말풍선 1 번역 결과:**\n\n'이 세계의 끝에는 무엇이 기다리고 있을까...?'")
                if bubble_choice in ["전체 번역하기", "말풍선 2 (좌측 중앙)"]:
                    draw.rectangle([box2[0], box2[1], box2[2], box2[3]], fill="white")
                    st.info("📝 **말풍선 2 번역 결과:**\n\n'기존 번역기보다 훨씬 읽기 편하군!'")
                if upscale_option:
                    st.success("🚀 업스케일링 적용 완료!")
                st.image(res_img, use_column_width=True)
else:
    st.info("💡 이미지를 업로드하세요.")