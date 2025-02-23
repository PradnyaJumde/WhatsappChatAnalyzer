from collections import Counter
import emoji
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from urlextract import URLExtract
#class is imported
extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #fetch the number of messages
    num_messages = df.shape[0]

    #fetch the number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    #fetch number of media messages
    num_media_messages = df[df['message'].notna() & (df['message'].str.strip().str.lower() == '<media omitted>')].shape[
        0]
    #fetching number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))


    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user, df):
    # If "Overall" is selected, don't filter the dataframe

    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())  # Convert stopwords into a set

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

        # Remove group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'].str.strip() != '<Media omitted>']

    def rename_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    if df.empty:
        return None  # Return None if no words exist

    # Generate the word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'].apply(rename_stop_words)
    temp['message'] = temp['message'].apply(lambda x: re.sub(r'\(file attached\)', '', x, flags=re.IGNORECASE))
    temp['message'] = temp['message'].apply(lambda x: re.sub(r'This message was deleted', '', x, flags=re.IGNORECASE))
    temp['message'] = temp['message'].apply(lambda x: re.sub(r'<Media omitted>', '', x, flags=re.IGNORECASE))
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

    # most common words
from collections import Counter
import pandas as pd
import re

from collections import Counter
import pandas as pd
import re

def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())  # Convert stopwords into a set

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove group notifications
    temp = df[df['user'] != 'group_notification']

    # Remove "(file attached)" and "message deleted" from messages while keeping other text
    temp['message'] = temp['message'].apply(lambda x: re.sub(r'\(file attached\)', '', x, flags=re.IGNORECASE))
    temp['message'] = temp['message'].apply(lambda x: re.sub(r'This message was deleted', '', x, flags=re.IGNORECASE))
    temp['message'] = temp['message'].apply(lambda x: re.sub(r'<Media omitted>', '', x, flags=re.IGNORECASE))

    # Process words
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and word.strip():  # Ignore empty words after cleaning
                words.append(word)

    # Get the 20 most common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])
    return most_common_df

#emoji analysis
import emoji
import pandas as pd
from collections import Counter

def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])  # Use emoji.is_emoji() to detect emojis

    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common(), columns=['Emoji', 'Count'])  # Create DataFrame

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    if df.empty:
        print("Filtered DataFrame is empty!")
        return pd.DataFrame()  # Return an empty DataFrame instead of None

    timeline = df.groupby(['year', 'month_num', 'month']).count().reset_index()

    if timeline.empty:
        print("Timeline DataFrame is empty!")
        return pd.DataFrame()

    timeline['time'] = timeline.apply(lambda row: f"{row['month']}-{row['year']}", axis=1)

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    if df.empty:
        return pd.DataFrame(columns=['only_date', 'message'])  # Ensure structure remains valid

    daily_timeline1 = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline1

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap=df.pivot_table(index='day_name', columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap






