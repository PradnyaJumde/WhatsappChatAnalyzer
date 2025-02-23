import streamlit as st
import matplotlib.pyplot as plt
from streamlit import pyplot
import seaborn as sns
import preprocessor, helper

st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # Read file as bytes and decode
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)
    #st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to:", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        # Display statistics
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig)
#daily timeline

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)

        if not daily_timeline.empty:
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            plt.show()
            st.pyplot(fig)
        else:
            st.warning("No data available for the daily timeline.")

# Activity map
        st.title("Activity map")
        col1, col2 = st.columns(2)
        with col1:
             st.header("Most Busy Day")
             busy_day = helper.week_activity_map(selected_user, df)
             fig, ax = plt.subplots()
             ax.bar(busy_day.index, busy_day.values)
             plt.xticks(rotation='vertical')
             st.pyplot(fig)
        with col2:
             st.header("Most Busy Month")
             busy_month = helper.month_activity_map(selected_user, df)
             fig, ax = plt.subplots()
             ax.bar(busy_month.index, busy_month.values)
             plt.xticks(rotation='vertical')
             st.pyplot(fig)

        st.title("Weekely acctivity Map")
        user_heatmap=helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)




    # Finding the busiest users
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation="vertical")
            st.pyplot(fig)
            with col2:
               st.dataframe(new_df)
        # word cloud
        st.title("WordCloud")
    df_wc = helper.create_wordcloud(selected_user, df)

    if df_wc is not None:
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")  # Hide axes
        st.pyplot(fig)
    else:
        st.warning("Not enough words to generate a Word Cloud.")


    st.header("Most Common 20 words used")
    most_common_df = helper.most_common_words(selected_user, df)

    if not most_common_df.empty:
        fig, ax = plt.subplots()
        ax.bar(most_common_df['Word'], most_common_df['Count'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    else:
        st.write("No common words to display.")
#emoji analysis
    emoji_df = helper.emoji_analysis(selected_user,df)
    emoji_df=emoji_df.head(10)
    plt.rcParams["font.family"] = "Segoe UI Emoji"  # For Windows
    st.title("Emoji Analysis")
    col1,col2=st.columns(2)
    #st.dataframe(emoji_df)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df["Count"], labels=emoji_df["Emoji"], autopct="%1.1f%%", textprops={'fontsize': 14})  # Use column names
        st.pyplot(fig)



















