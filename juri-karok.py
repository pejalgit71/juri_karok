import streamlit as st
st.set_page_config(layout="wide")
import warnings
import pandas as pd
from datetime import datetime
import warnings
import os, fnmatch
from PIL import Image
import glob
warnings.filterwarnings("ignore")

st.sidebar.title("Juri Karaoke")
formside = st.sidebar.form("side_form")
choose = formside.radio("Pilih menu",["Markah","Admin"], index=None)
formside.form_submit_button("Submit")



from streamlit_gsheets import GSheetsConnection
conn = st.connection("gsheets", type=GSheetsConnection)
# menu_df = conn.read(spreadsheet=url,nrows=7,  worksheet="menu")
peserta_df = conn.read(nrows=7, usecols=list(range(5)), ttl="1m",  worksheet="peserta")
# menu_df = pd.read_csv("menu.csv")

if (choose == "Markah"):
    col1, col2, col3= st.columns(3)
    col1.subheader("Peserta Karaoke")
    col2.subheader("Markah")
    col3.subheader("Pemenang")
    peserta_df = pd.DataFrame(peserta_df)
    peserta_df = peserta_df.dropna(subset=["nama"])
    peserta_df = peserta_df.reset_index(drop=True)
    peserta_df.index = peserta_df.index+1
    
    # peserta_df['vokal'] = peserta_df.apply(lambda x: col2.number_input(f"Markah Vokal {x['nama']}", min_value=1, max_value=100, key=x['vokal']), axis=1)
    # peserta_df['kreativiti'] = peserta_df.apply(lambda y: col2.number_input(f"Markah Kreativiti{y['nama']}", min_value=1, max_value=100, key=y['kreativiti']), axis=1)
    # peserta_df['persembahan'] = peserta_df.apply(lambda z: col2.number_input(f"Markah Persembahan {z['nama']}", min_value=1, max_value=100, key=z['persembahan']), axis=1)
    
    # peserta_df['markah'] = peserta_df.apply(lambda x: col2.number_input(f"Markah Vokal {x['nama']}", min_value=1, max_value=100, key=x['nama']), axis=1)
    edited_peserta = col1.data_editor(
        peserta_df[["nama", "vokal", "kreativiti", "persembahan"]],
        column_config={
            "vokal": st.column_config.NumberColumn(min_value=0, max_value=50),
            "kreativiti": st.column_config.NumberColumn(min_value=0, max_value=30),
            "persembahan": st.column_config.NumberColumn(min_value=0, max_value=20)
            },disabled=["nama"],hide_index=True,
        )
    # edited_peserta = col1.data_editor(peserta_df[["nama", "vokal", "kreativiti", "persembahan"]], disabled=["nama"])
    peserta_df["markah"] = edited_peserta["vokal"]+edited_peserta["kreativiti"]+edited_peserta["persembahan"]
    col2.write(peserta_df[["nama", "markah"]])
    
    peserta_df = peserta_df.sort_values(by='markah', ascending=False)
    peserta_df = peserta_df.reset_index(drop=True)
    peserta_df.index = peserta_df.index+1
    # pemenang1 = peserta_df[peserta_df["markah"] == peserta_df["markah"].nlargest(1)+][["nama", "markah"]] 
    # pemenang2 = peserta_df[peserta_df["markah"] == peserta_df["markah"].max(2).idxmin(), axis=0][["nama", "markah"]] 
    # pemenang1 = peserta_df["markah"].max()
    # pemenang2 = peserta_df["markah"]
    col3.write(peserta_df[["nama","markah"]])
    st.subheader("No 1 adalah : " + str (peserta_df["nama"][1]))
    st.subheader("No 2 adalah : " + str(peserta_df["nama"][2]))
    st.subheader("No 3 adalah : " + str(peserta_df["nama"][3]))
    
if (choose == "Admin"):
    edited_peserta = pd.DataFrame()
    edited_peserta["nama"] = st.data_editor(
        peserta_df["nama"], num_rows="dynamic"
    )
    if st.button('Klik Sini Untuk Kemaskini'):
        peserta_df["nama"]=edited_peserta["nama"]
        # edited_peserta = edited_peserta[["nama", "vokal", "kreativiti", "persembahan"]]
        conn.update(worksheet="peserta", data=peserta_df)
        st.success("Nama telah dikemaskini")
                 
# .nlargest(2) + .idxmin()
