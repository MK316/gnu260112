import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Starter Platforms", layout="wide")

# =========================
# Tabs
# =========================
tab_intro, tab_trends = st.tabs(
    ["🧩 시작을 위한 핵심 플랫폼", "📈 Google Trends로 보는 흐름"]
)

# =========================================================
# TAB 1: Platform introduction (기존 페이지)
# =========================================================
with tab_intro:

    st.markdown("## 🔗 Streamlit 시작을 위한 기본 플랫폼")
    st.caption(
        "Streamlit 앱을 만들기 전에 꼭 한 번씩 경험해 보아야 할 핵심 플랫폼과 도구들입니다."
    )

    st.markdown("---")

    # ---- Simple & modern card style ----
    st.markdown(
        """
    <style>
    .platform-card {
        border: 1px solid #e6e6e6;
        border-radius: 14px;
        padding: 20px;
        background: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        height: 100%;
    }
    .platform-title {
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .platform-desc {
        font-size: 15px;
        color: #555;
        line-height: 1.6;
        margin-bottom: 14px;
    }
    .link-btn {
        display: inline-block;
        padding: 10px 16px;
        border-radius: 10px;
        font-weight: 700;
        text-decoration: none !important;
        color: #ffffff !important;
        background: #111111;
        transition: background-color 0.15s ease;
    }
    .link-btn:hover {
        background: #FFD700;
        color: #111111 !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    platforms = [
        {
            "name": "GitHub",
            "icon": "🗃️",
            "url": "https://github.com/",
            "desc": (
                "코드와 파일을 온라인에 저장하고 공유하는 플랫폼입니다.\n"
                "Streamlit 앱을 배포할 때 GitHub 저장소가 필요합니다.\n"
                "수업 자료와 프로젝트를 관리하는 데에도 유용합니다."
            ),
        },
        {
            "name": "Google Colab",
            "icon": "☁️",
            "url": "https://colab.google/",
            "desc": (
                "설치 없이 브라우저에서 바로 Python을 실행할 수 있는 환경입니다.\n"
                "Python 기초 문법을 연습하거나 간단한 실험을 하기에 적합합니다.\n"
                "초보자에게 부담이 적은 학습 도구입니다."
            ),
        },
        {
            "name": "Hugging Face",
            "icon": "🤗",
            "url": "https://huggingface.co/",
            "desc": (
                "AI 모델과 데이터셋, 데모 앱을 공유하는 플랫폼입니다.\n"
                "언어 모델과 관련된 다양한 예제를 직접 체험할 수 있습니다.\n"
                "Streamlit 기반 앱을 Spaces로 배포할 수도 있습니다."
            ),
        },
        {
            "name": "Python",
            "icon": "🐍",
            "url": "https://wikidocs.net/book/1",
            "desc": (
                "Streamlit 앱을 만드는 데 사용되는 프로그래밍 언어입니다.\n"
                "기본 문법과 조건문, 함수 정도만 알아도 충분히 시작할 수 있습니다.\n"
                "코딩 경험이 적은 학습자에게도 비교적 접근성이 높습니다."
            ),
        },
        {
            "name": "Streamlit",
            "icon": "🧩",
            "url": "https://streamlit.io/",
            "desc": (
                "Python 코드를 웹 애플리케이션으로 바꿔주는 프레임워크입니다.\n"
                "버튼, 탭, 슬라이더 등을 쉽게 추가할 수 있습니다.\n"
                "학습용 앱이나 수업 보조 도구를 만들기에 적합합니다."
            ),
        },
    ]

    cols = st.columns(2, gap="large")
    for i, p in enumerate(platforms):
        with cols[i % 2]:
            st.markdown(
                f"""
    <div class="platform-card">
      <div class="platform-title">{p["icon"]} {p["name"]}</div>
      <div class="platform-desc">{p["desc"].replace("\n", "<br>")}</div>
      <a class="link-btn" href="{p["url"]}" target="_blank" rel="noopener noreferrer">
        {p["name"]} 바로가기 ↗
      </a>
    </div>
    """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.caption("각 링크는 새 창에서 열리며, 자주 사용하는 플랫폼은 북마크해 두는 것을 권장합니다.")

# =========================================================
# TAB 2: Google Trends
# =========================================================
with tab_trends:

    st.markdown("## 📈 Google Trends로 보는 플랫폼 관심도 변화")
    st.caption(
        "디지털 도구와 AI 플랫폼이 언제부터 사회적으로 주목받기 시작했는지를 Google Trends 데이터를 통해 살펴봅니다."
    )

    st.markdown(
        """
- 이 그래프는 **특정 도구의 일시적 유행이 아닌, 장기적 변화 흐름**을 보여줍니다.
- 전공 수업에서 디지털·AI 도구를 도입해야 하는 **시대적 배경**을 설명하는 자료로 활용할 수 있습니다.
"""
    )

    trends_html = """
    <script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/4284_RC01/embed_loader.js"></script>
    <script type="text/javascript">
    trends.embed.renderExploreWidget(
      "TIMESERIES",
      {
        "comparisonItem":[
          {"keyword":"Github","geo":"","time":"2004-01-01 2026-01-12"},
          {"keyword":"Colab","geo":"","time":"2004-01-01 2026-01-12"},
          {"keyword":"Huggingface","geo":"","time":"2004-01-01 2026-01-12"},
          {"keyword":"Streamlit","geo":"","time":"2004-01-01 2026-01-12"}
        ],
        "category":0,
        "property":""
      },
      {
        "exploreQuery":"date=all&q=Github,Colab,Huggingface,Streamlit&hl=en",
        "guestPath":"https://trends.google.co.kr:443/trends/embed/"
      }
    );
    </script>
    """

    components.html(trends_html, height=750, scrolling=False)

    st.markdown(
        """
**활용 제안**
- 교수자: “왜 지금 이런 수업이 필요한가”를 설명하는 도입 자료
- 학생: 도구 학습이 개인 기술이 아니라 **사회적 요구**임을 이해
"""
    )
