import streamlit as st


def load_css():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]{
        font-family: 'Inter', sans-serif;
    }

    /* ===========================
       Main Layout
    =========================== */

    .main .block-container{
        max-width:1200px;
        padding-top:1.8rem;
        padding-bottom:3rem;
    }

    .stApp{
        background:#FAFBFC;
    }

    /* ===========================
       Hide Branding
    =========================== */

    #MainMenu{visibility:hidden;}
    footer{visibility:hidden;}
    header{visibility:hidden;}

    /* ===========================
       Sidebar
    =========================== */

    section[data-testid="stSidebar"]{

        background:white;

        border-right:1px solid #ECECEC;

        box-shadow:4px 0px 25px rgba(0,0,0,0.04);

    }

    /* ===========================
       Chat Messages
    =========================== */

    .stChatMessage{

        border-radius:18px;

        padding:18px;

        margin-bottom:18px;

        border:1px solid #ECECEC;

        background:white;

        transition:all .25s ease;

        box-shadow:0 6px 20px rgba(0,0,0,.04);

    }

    .stChatMessage:hover{

        transform:translateY(-2px);

        box-shadow:0 12px 24px rgba(0,0,0,.08);

    }

    /* ===========================
       Buttons
    =========================== */

    .stButton>button{

        width:100%;

        border-radius:12px;

        border:none;

        font-weight:600;

        padding:.65rem;

        transition:.25s;

    }

    .stButton>button:hover{

        transform:translateY(-2px);

        box-shadow:0 8px 20px rgba(0,0,0,.12);

    }

    /* ===========================
       Metrics
    =========================== */

    div[data-testid="metric-container"]{

        background:white;

        border:1px solid #ECECEC;

        border-radius:16px;

        padding:16px;

        box-shadow:0 5px 18px rgba(0,0,0,.05);

    }

    /* ===========================
       Dataframe
    =========================== */

    div[data-testid="stDataFrame"]{

        border-radius:16px;

        overflow:hidden;

        border:1px solid #ECECEC;

        box-shadow:0 5px 18px rgba(0,0,0,.05);

    }

    /* ===========================
       Expanders
    =========================== */

    details{

        border-radius:14px;

        border:1px solid #ECECEC;

        background:white;

        margin-bottom:12px;

    }

    summary{

        font-weight:600;

        padding:6px;

    }

    /* ===========================
       Code
    =========================== */

    pre{

        border-radius:14px !important;

        border:1px solid #ECECEC;

    }

    /* ===========================
       File Uploader
    =========================== */

    div[data-testid="stFileUploader"]{

        border:2px dashed #CBD5E1;

        border-radius:18px;

        padding:16px;

        background:#FCFCFD;

    }

    /* ===========================
       Progress
    =========================== */

    div[data-testid="stProgress"]{

        margin-top:10px;

        margin-bottom:14px;

    }

    /* ===========================
       Scrollbar
    =========================== */

    ::-webkit-scrollbar{

        width:10px;

    }

    ::-webkit-scrollbar-track{

        background:#F5F5F5;

    }

    ::-webkit-scrollbar-thumb{

        background:#C5C5C5;

        border-radius:20px;

    }

    ::-webkit-scrollbar-thumb:hover{

        background:#9F9F9F;

    }

    </style>
    """, unsafe_allow_html=True)