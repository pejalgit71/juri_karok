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
peserta_df = conn.read(nrows=8, usecols=list(range(5)), ttl="1m",  worksheet="peserta")
# menu_df = pd.read_csv("menu.csv")

if (choose == "Markah"):
    container1 = st.container(border=True)
    container2 = st.container(border=True)
    col1, col2, col3= container1.columns(3)
    col4, col5, col6= container2.columns(3)
    
    col1.subheader("Peserta Karaoke")
    col2.subheader("Jumlah Besar Markah")
    col3.subheader("Sisihan Markah ")
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

    edited_peserta = edited_peserta.sort_values(by='persembahan', ascending=False)
    edited_peserta = edited_peserta.reset_index(drop=True)
    edited_peserta.index = edited_peserta.index+1
   
    # pemenang1 = peserta_df[peserta_df["markah"] == peserta_df["markah"].nlargest(1)+][["nama", "markah"]] 
    # pemenang2 = peserta_df[peserta_df["markah"] == peserta_df["markah"].max(2).idxmin(), axis=0][["nama", "markah"]] 
    # pemenang1 = peserta_df["markah"].max()
    # pemenang2 = peserta_df["markah"]
    col3.write(peserta_df[["nama","markah"]])
   
    if col4.button("Klik untuk kira pemenang"):
        col4.subheader("No 1 adalah : " + str (peserta_df["nama"][1]))
        col4.subheader("No 2 adalah : " + str(peserta_df["nama"][2]))
        col4.subheader("No 3 adalah : " + str(peserta_df["nama"][3]))
        col4.balloons()
        col4.snow()
        
    if col5.button("Klik untuk kira Persembahan Terbaik"):
        col5.subheader("No 1 adalah : " + str(edited_peserta["nama"][1]))
        col5.balloons()

    peserta = col6.text_input('Tulis nama peserta')
    if col6.button('Cari'):
        have_it = peserta.lower() in list(map(str.lower,peserta_df["nama"]))
        col6.write('Jumpa!') if have_it else col6.write('Tak jumpa nama tuh')

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
