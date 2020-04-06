# import libraries
import sys
import pickle
import pandas as pd
import numpy as np


def load_data(filepath='data/', orient='records', lines=True):
    """
    load dataset
    :param filepath: (str)
    :param orient: (str) read_json orient
    :param lines: (bool) read_json by lines
    :return:(pandas.DataFrame) portfolio, profile, transcript
    """
    # read in the json files
    portfolio = pd.read_json(filepath+'portfolio.json', orient=orient, lines=lines)
    profile = pd.read_json(filepath+'profile.json', orient=orient, lines=lines)
    transcript = pd.read_json(filepath+'transcript.json', orient=orient, lines=lines)
    return portfolio, profile, transcript


def one_hot_channels(portfolio):
    """
    one hot encoded channels columns
    :param portfolio:(pandas.DataFrame)
    :return:
    """
    channel_lst = []
    for item in portfolio['channels']:
        channel_lst += item
    channel_lst = list(set(channel_lst))
    for channel in channel_lst:
        portfolio[channel] = portfolio.channels.apply(lambda x: 1 if channel in x else 0)
    # drop channels column
    portfolio = portfolio.drop('channels', axis=1)
    return portfolio


def divide_into_groups_dummies(df, column, interval):
    """
    divide values into several groups according to the interval，and transfer to one-hot style
    :param df:(dataframe)
    :param column:(str)
    :param interval:(int)
    :return:(dataframe)
    """
    df['temp'] = df.apply(lambda x: None if pd.isnull(x[column]) else np.floor(x[column]/interval).astype(int), axis=1)
    df = pd.get_dummies(df, columns=['temp'], prefix=column)
    return df


def get_events(df, event_value, new_name):
    """
    get one type of events and rename column "time"
    :param df:(pd.DataFrame)
    :param event_value:(str)event
    :param new_name:(str)the new column name
    :return:(pd.DataFrame)
    """
    temp = df[df['event']==event_value].copy()
    temp = temp.rename(columns={"time": new_name+"_time"})
    temp = temp.drop(['event'], axis=1)
    return temp


def get_time(from_df, to_df, time_in_from_df,
             time_in_to_df='offer_received_time', duration_col_name='duration'):
    """
    Match items in from_df to to_df according to person&offerId and calculate the time duration.
    If more than one item in to_df matches the item in to_df, only match the latest one.
    :param from_df: (pd,DataFrame)
    :param time_in_from_df: (str)column name in from_df
    :param to_df: (pd,DataFrame)
    :param time_in_to_df: (str)column name in to_df
    :param duration_col_name: (str)
    :return:
    """
    df = to_df.copy()
    df[duration_col_name] = None
    for _, row in from_df.iterrows():
        person = row['person']
        offerId = row['offerId']
        from_time = row[time_in_from_df]
        rec_time_lst = list(df[(df['person'] == person) & (df['offerId'] == offerId)][time_in_to_df])
        if rec_time_lst:
            time_btw_lst = [(from_time - time) for time in rec_time_lst if (from_time - time >= 0)]
            if time_btw_lst:
                time_btw = np.min(time_btw_lst)
                df.loc[lambda df:((df['person'] == person) & (df['offerId'] == offerId) & (
                    df[time_in_to_df] == (int(from_time - time_btw)))), duration_col_name] = time_btw
    return df


def time_validation(row, time, duration):
    """
    Check offer time validation, out of offer duration or None is invalid
    :param row: (pd.Series)
    :param time: (str)time column name
    :param duration: (dict)valid duration dict
    :return: (int)(0,1) 1 for valid, 0 for invalid
    """
    if pd.isnull(row[time]) or row[time]/24 > duration[row['offerId']]:
        return 0
    return 1


def clean_data(portfolio, profile, transcript):
    """
    clean the raw data
    :param df: (pandas.DataFrame) raw data
    :return: (pandas.DataFrame) cleaned data
    """
    print("clean portfolio...")
    # one hot encoded channels columns in portfolio
    portfolio = one_hot_channels(portfolio)
    # one hot encoded offer_type columns in portfolio
    portfolio = pd.get_dummies(portfolio, columns=['offer_type'])

    print("clean profile...")
    # replace the age 118 in profile to None
    profile.loc[lambda x: x['age'] == 118, 'age'] = None
    # Group the ages at intervals of 10，then one-hot encoding
    profile = divide_into_groups_dummies(profile, 'age', 10)
    # format became_member_on as type datetime
    profile['became_member_on'] = pd.to_datetime(profile.became_member_on.astype(str))
    # add became_member_yeaer column
    profile['became_member_year'] = profile['became_member_on'].apply(lambda x: x.year)
    # one-hot encoded became_member_yeaer
    profile = pd.get_dummies(profile, columns=['became_member_year'])
    # one-hot encoded gender
    profile = pd.get_dummies(profile, columns=['gender'])
    # Group the income at intervals of 10，then one-hot encoding
    profile = divide_into_groups_dummies(profile, 'income', 10000)

    # # extract transaction data
    # print("extract transaction data...")
    # transaction = transcript[transcript['event'] == 'transaction'].copy().reset_index(drop=True)
    # # add "amount" column
    # transaction['amount'] = transaction['value'].apply(lambda x: x['amount'])
    # transaction = transaction.drop(['value'], axis=1)

    print("clean transcript data...")
    # extract transcript data except transaction events
    # transcript = transcript[transcript['event'] != 'transaction']
    transcript = transcript.loc[lambda x: x['event'] != 'transaction', :]
    # add offerId column
    # attention: some keys in 'value' are‘offer_id’instead of offer id’
    transcript['offerId'] = transcript['value'].apply(
        lambda x: x.get('offer id') if x.get('offer id') else x.get('offer_id'))
    # drop 'value' column
    transcript = transcript.drop(['value'], axis=1)
    # combine the different events of the same customer and same offer into one row
    # extract different events
    offer_received = get_events(transcript, "offer received", "offer_received")
    offer_viewed = get_events(transcript, "offer viewed", "offer_viewed")
    offer_completed = get_events(transcript, "offer completed", "offer_completed")

    print("clean transcript data...please wait for about 20 minutes...")
    # add column time_btw_rec_view（duration between received and viewed）
    df = get_time(from_df=offer_viewed, to_df=offer_received,
                  time_in_from_df='offer_viewed_time',
                  duration_col_name='time_btw_rec_view')
    print("clean transcript data...please wait for about 20 minutes...")
    # add column 'time_btw_rec_cmpt'（duration between received and completed）
    df = get_time(from_df=offer_completed, to_df=df,
                  time_in_from_df='offer_completed_time',
                  duration_col_name='time_btw_rec_cmpt')
    # add 'offer_viewed' column，to mark whether the offer is viewed
    df['offer_viewed'] = df.apply(lambda x: 0 if pd.isnull(x['time_btw_rec_view']) else 1, axis=1)
    # add'offer_completed'column，to mark whether the offer is completed
    df['offer_completed'] = df.apply(lambda x: 0 if pd.isnull(x['time_btw_rec_cmpt']) else 1, axis=1)
    # Saves the expiration duration of different offers into the dict
    duration = dict()
    for offerId in portfolio['id']:
        duration[offerId] = int(portfolio[portfolio['id'] == offerId]['duration'])
    # validate of the duration from offer_completed to offer_received
    df['time_btw_rec_cmpt_valid'] = df.apply(time_validation, axis=1, args=['time_btw_rec_cmpt', duration])
    # validate of the duration from offer_viewed to offer_received
    df['time_btw_rec_view_valid'] = df.apply(time_validation, axis=1, args=['time_btw_rec_view', duration])
    # add 'viewed_before_completed' column，to mark whether the offer is viewed before completed
    df['viewed_before_completed'] = df.apply(
        lambda x: 0 if (pd.isnull(x['time_btw_rec_view']) or pd.isnull(x['time_btw_rec_cmpt'])
                        or x['time_btw_rec_view'] > x['time_btw_rec_cmpt']) else 1, axis=1)

    # merge portfolio into the clean data
    df_merged = pd.merge(df, portfolio, left_on='offerId', right_on='id', how='left')
    # merge profile into the clean data
    df_merged = pd.merge(df_merged, profile, left_on='person', right_on='id', how='left')
    # drop useless columns
    df_merged = df_merged.drop(['id_x', 'id_y'], axis=1)

    return df_merged


def save_data(df, filename='./data/merged.pickle'):
    """
    save data to database
    :param df: (pandas.DataFrame)
    :param filename: (str)
    :return: None
    """
    with open(filename, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)
    return


def main():
    if len(sys.argv) == 3:
        data_filepath, clean_data_filename = sys.argv[1:]

    else:
        print('Using dataset in the default filepaths (data\). '\
              'You can also provide the filepaths of the '\
              'datasets as the first argument , as '\
              'well as the filename to save the cleaned data '\
              'to as the second argument. \n\nExample: python process_data.py '\
              'data/  data/cleaned_data.pickle')

        data_filepath = './data/'
        clean_data_filename = './data/cleaned_data.pickle'

    print('Loading data in {}...\n'.format(data_filepath))
    try:
        portfolio, profile, transcript = load_data(data_filepath)
    except Exception as e:
        print("failed to loading the dataset!")

    print('Cleaning data...')
    df = clean_data(portfolio, profile, transcript)

    print('Saving data to {}...\n'.format(clean_data_filename))
    save_data(df, clean_data_filename)

    print('Cleaned data saved!')


if __name__ == '__main__':
    main()
