import streamlit as st
import pandas as pd
import game_random_generator

# wide layout
st.set_page_config(layout="wide")

#################################
#
#
#           Functions
#
#
##################################


@st.cache_data
def fetch_data(level_name):
    df = pd.read_csv(level_name, sep=",", header=None)
    return df


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def path_to_image_html(path):
    return '<img class="tileset" src="' + path + '" width="30" >'


def level_renderer(df, game_objects, tileset):
    level_html = '<div class="container"><div class="gamegrid">'

    for i, row in enumerate(df):  # iterate through the rows of the numpy array
        for j, cell in enumerate(row):
            level_html += (
                f'<img title="{j}, {i}, {cell}" src="{tileset[cell]}"'
                f' style="grid-column-start: {j+1}; grid-row-start: {i+1};">'
            )
    level_html += f'{game_objects}</div></div>'

    return level_html



#################################
#
#
#           Constants
#
#
##################################


tileset = {
    "@": "https://oshi.at/ZMUu/avRY.gif",
    "W": "https://thumbs2.imgbox.com/10/db/7zaxbIP8_t.png",  # wall
    "FP": "https://thumbs2.imgbox.com/29/22/5rTLr6WH_t.png",  # floor_plain
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


#################################
#
#
#            The App
#
#
##################################

# css style

local_css("style.css")

# title
st.subheader("The Dungeon level editor")

# file upload for ones wanting to upload their own file
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file, header=None)
if uploaded_file is None:
    if "df" not in st.session_state:
        st.session_state.df = fetch_data("level1.csv")


# ------------------ SPLIT TO TABS--------------------------


tab1, tab2 = st.tabs(["Editor", "Tilset"])

# main editor

with tab1:

    col1, col2 = st.columns(2)

    with col2:
        level_data = st.experimental_data_editor(
            st.session_state.df, use_container_width=True, height=620
        )
        data_as_csv = level_data.to_csv(index=False, header=False).encode("utf-8")
        st.download_button("Download CSV", data_as_csv, "level_edited.csv")
        st.caption(
            "To edit the level, modify the table cells. All possible tile names are presented in the Tilset tab."
        )

    with col1:
        html = level_renderer(level_data.values, "",tileset)

        # display_html = st.empty()

        st.markdown(html, unsafe_allow_html=True)
        if st.button("Clear Level"):
            st.session_state.df = st.session_state.df.replace(
                regex="[a-zA-Z0-9]+", value="E"
            )

# tileset

if st.button("generate randomly"):
    st.session_state.df = game_random_generator.dungeon_df()
    st.experimental_rerun()

with tab2:

    df_tileset = pd.DataFrame.from_dict(tileset, orient="index", columns=["look"])

    st.markdown(
        df_tileset.to_html(escape=False, formatters=dict(look=path_to_image_html)),
        unsafe_allow_html=True,
    )
