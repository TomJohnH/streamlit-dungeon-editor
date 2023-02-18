# https://streamlit-feature-demos-data-editor-foundationdemo-bhdzga.streamlit.app/

import streamlit as st
import pandas as pd

from pydataset import data


@st.cache_data
def fetch_data(level_name):
    df = pd.read_csv(level_name, sep=",", header=None)
    return df


# edited_df = st.experimental_data_editor(df)
df = fetch_data("level1.csv")

st.subheader("The Dungeon level editor")
level_data = st.experimental_data_editor(df)
data_as_csv = level_data.to_csv(index=False, header=False).encode("utf-8")
st.download_button("Download CSV", data_as_csv, "level_edited.csv")

# ----------------------------------------------------


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")

tileset = {
    "@": "https://oshi.at/ZMUu/avRY.gif",
    "W": "https://thumbs2.imgbox.com/10/db/7zaxbIP8_t.png",  # wall
    "FP": "https://thumbs2.imgbox.com/29/22/5rTLr6WH_t.png",  # floor_plain
    # "FP": "https://oshi.at/PQkn/ExtR.png",  # floor 1 tilset 2
    "CAT": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/cat.gif",  # cat
    "M": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/monster.gif",  # monster, skeleton
    "FS": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/floor_stain_1.png",
    "E": "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==",
    "FE3": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/floor_edge_3.png",  # floor_edge_3
    "WON": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_outer_n.png",  # Wall_outer_n
    "WOE": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_outer_e.png",  # Wall_outer_e
    "WONE": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_outer_ne.png",  # Wall_outer_ne
    "WOW": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_outer_w.png",  # Wall_outer_w
    "WONW": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_outer_nw.png",  # wall_outer_nw
    "WFR": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_front_right.png",  # wall front right
    "WTR": "https://oshi.at/QpWg/Mfxv.png",  # wall top right
    # "DK": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/wall_missing_brick_2.png",  # darkness
    "WMB": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/wall_missing_brick_2.png",  # wall missing brick 1
    "BOX": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/box.png",  # box
    "DR": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/darkness_right.png",  # darkenss right
    "DB": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/darkness_bottom.png",  # darkness bottom
    "T": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/torch.gif",  # torch
    "FMN1": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/floor_mud_n_1.png",  # floor_mud_n_1
    "FMN2": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/floor_mud_n_2.png",  # floor_mud_n_2
    "FMNE": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/floor_mud_ne.png",  # floor_mud_ne
    "CGOF": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/chest_golden_open_full.png",  # chest_golden_open_full
    "CGOO": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/chest_open_empty.png",  # chest_open_empty
    "FL": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Floor_ladder.png",  # Floor_ladder
}


def level_renderer(df, game_objects):
    i = 0
    j = 0
    level_html = '<div class="container"><div class="gamegrid">'
    for x in df:  # array from data frame: df.values
        # st.write(x)
        j = 0
        for y in x:

            # if y == "FP" and random.uniform(0, 1) > 0.7:
            #     tilset_tile = tileset["DK"]
            # else:
            #     tilset_tile = tileset[y]

            level_html = (
                level_html
                + '<img src="'
                + tileset[y]  # tilset_tile
                + '" style="grid-column-start: '
                + str(j + 1)
                + "; grid-row-start: "
                + str(i + 1)
                + ';">'
            )
            j = j + 1
        i = i + 1
    level_html = level_html + game_objects + "</div></div>"
    return level_html


html = level_renderer(level_data.values, "")

# display_html = st.empty()

display_html = st.markdown(html, unsafe_allow_html=True)
