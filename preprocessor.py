import pandas as pd

def preprocess(df,regions_df):
    # filtering for summer olympics
    df= df[df['Season'] == 'Summer']
    # Merge with regions_df
    df= df.merge(regions_df, on='NOC', how='left')
    # Dropping Duplicates
    df.drop_duplicates(inplace=True)
    # One hot encoding medal
    df= pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df