import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert 'message_date' to datetime format with 2-digit year
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')

    # Rename the column correctly
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []

    # Use the correct column name 'user_message' since it still exists in the DataFrame
    for message in df['user_message']:  # Correct column name
        entry = re.split(r'([\w\W]+?):\s', message)  # Use raw string for regex pattern
        if entry[1:]:  # User name found
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    # Add the new columns to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the old 'user_message' column after processing
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period =[]
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+"-"+str('00'))
        elif hour ==0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period


    return df

