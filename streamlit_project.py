import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt


with st.echo(code_location='below'):
    @st.cache
    def get_data(location):
        return (
            pd.read_csv(location)
        )


    """
        ## Топ 2000 Аниме (по данным MyAnimeList)
    """
    df_anime = get_data('mal_top2000_anime.csv').drop(['Unnamed: 0'], axis=1)


    def str_to_list(column):
        for i in range(len(df_anime[column])):
            a = df_anime[column][i]
            a = a[2:len(a) - 2].split("', '")
            df_anime[column][i] = a


    str_to_list('Genres')
    str_to_list('Studio')
    str_to_list('Theme(s)')

    show_anime_dataset = st.checkbox('Show full Anime dataset')
    if show_anime_dataset:
        df_anime

    col1, col2, col3 = st.columns(3)
    with col1:
        genres_1 = df_anime["Genres"]
        genres = ['Any']
        for el in genres_1:
            for genre in el:
                if not (genre in genres):
                    genres.append(genre)

        genre_select = st.selectbox(
            'Аниме какого жанра вы бы хотели рассмотреть?',
            genres)
    with col2:
        themes_1 = df_anime["Theme(s)"]
        themes = ['Any']
        for el in themes_1:
            for theme in el:
                if not (theme in themes):
                    themes.append(theme)

        theme_select = st.selectbox(
            'Аниме с какой темой вы бы хотели рассмотреть?',
            themes)
    with col3:
        studios_1 = df_anime["Studio"]
        studios = ['Any']
        for el in studios_1:
            for studio in el:
                if not (studio in studios):
                    studios.append(studio)

        studio_select = st.selectbox(
            'Аниме какой студии вы бы хотели рассмотреть?',
            studios)

    df_anime_selection = df_anime
    if genre_select != 'Any':
        df_anime_selection = df_anime_selection[:][[genre_select in x for x in df_anime_selection['Genres']]]
    if studio_select != 'Any':
        df_anime_selection = df_anime_selection[:][[studio_select in x for x in df_anime_selection['Studio']]]
    if theme_select != 'Any':
        df_anime_selection = df_anime_selection[:][[theme_select in x for x in df_anime_selection['Theme(s)']]]
    df_anime_selection

    lib = st.radio(
        "Выберите библиотеку для построения графика:",
        ('matplotlib.pyplot', 'seaborn', 'altair'))

    if lib == 'matplotlib.pyplot':
        def adjust_lightness(color, amount=0.5):
            import matplotlib.colors as mc
            import colorsys
            try:
                c = mc.cnames[color]
            except:
                c = color
            c = colorsys.rgb_to_hls(*mc.to_rgb(c))
            return colorsys.hls_to_rgb(c[0], c[1] * amount, c[2])


        fig, ax = plt.subplots()
        TYPE_COLORS = ["#f66d44", "#feae65", "#e6f69d", "#aadea7", "#64c2a6", "#2d87bb"]
        CATEGORY_CODES = pd.Categorical(df_anime_selection["Type"]).codes
        COLORS = np.array(TYPE_COLORS)[CATEGORY_CODES]
        EDGECOLORS = [adjust_lightness(color, 0.6) for color in COLORS]
        # ANIME = df_anime_selection['Name']
        # if len(ANIME) <= 10:
        #    ANIME_HIGHLIGHT = ANIME
        # else:
        #    ANIME_HIGHLIGHT = ANIME[:11]
        # TEXTS = []
        # for idx, anime in enumerate(ANIME):
        #    if anime in ANIME_HIGHLIGHT:
        #        x, y = df_anime_selection['Score Rank'][idx], df_anime_selection['Popularity Rank'][idx]
        #        TEXTS.append(ax.text(x, y, anime, fontsize=12))
        # TEXTS
        # adjust_text(
        #    TEXTS,
        #    expand_points=(3, 3),
        #    arrowprops=dict(arrowstyle="-", lw=1),
        #    ax=ax
        # )

        ax.scatter(
            df_anime_selection['Score Rank'], df_anime_selection['Popularity Rank'], color=COLORS,
            edgecolors=EDGECOLORS,
            s=80, alpha=0.5, zorder=10
        )
        ax.set_xlabel("Score Rank")
        ax.set_ylabel("Popularity Rank")
        st.pyplot(fig)

    if lib == 'seaborn':
        fig, ax = plt.subplots()
        sns.scatterplot(data=df_anime_selection, x="Score Rank", y="Popularity Rank", hue="Type")
        st.pyplot(fig)

        fig = sns.pairplot(data=df_anime_selection)
        st.pyplot(fig)

    if lib == 'altair':
        chart = (
            alt.Chart(df_anime_selection)
                .mark_circle()
                .encode(x="Score Rank", y="Popularity Rank", color='Type')
        )

        st.altair_chart(
            (
                chart
            ).interactive(), use_container_width=True
        )

    """
        ## Индекс Джини по странам 1981-2018 гг.
    """
    df_ig = get_data('data.csv').rename(columns={'Year_' + str(i): i for i in range(1981, 2019)})
    df_ig

    c1, c2 = st.columns(2)
    with c1:
        option = st.selectbox(
            'Какие страны вы хотите рассмотреть?',
            df_ig['Country_Name'],
        )
    with c2:
        start_year, end_year = st.select_slider(
            'Выберите диапазон времени:',
            options=range(1981, 2019),
            value=(1981, 2018))
    df_ig_selection = df_ig[:][[x == option for x in df_ig['Country_Name']]].set_index('Country_Name').drop(['Country_Code', 'Region_Name', 'Income_Group', 'Special_Notes'], axis=1)
    df_ig_selection


    """
    ## Standard of living indicators
    """

    df = pd.read_csv('standard-of-living-indicators.csv').drop(['Unnamed: 0'], axis=1)
    df
    option = st.selectbox(
        'Which region would you like to see?',
        df['Region'].unique()
    )
    df_selection = df[lambda x: x["Region"] == option]
    df_selection
    chart_SPI = (
        alt.Chart(df_selection)
            .mark_circle()
            .encode(x='GDP per capita $', y="SPI", color=alt.value('red'))
    )
    chart_HCI = (
        alt.Chart(df_selection)
            .mark_circle()
            .encode(x='GDP per capita $', y="HCI", color=alt.value('green'))
    )
    chart_HPI = (
        alt.Chart(df_selection)
            .mark_circle()
            .encode(x='GDP per capita $', y="HPI", color=alt.value('blue'))
    )
    chart_GINI = (
        alt.Chart(df_selection)
            .mark_circle()
            .encode(x='GDP per capita $', y="GINI", color=alt.value('yellow'))
    )
    chart_HDI = (
        alt.Chart(df_selection)
            .mark_circle()
            .encode(x='GDP per capita $', y="HDI", color=alt.value('pink'))
    )

    st.altair_chart(
        (
                chart_SPI
                + chart_HDI
                + chart_GINI
                + chart_HPI
                + chart_HCI
        ).interactive(), use_container_width=True
    )







