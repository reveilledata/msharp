import pandas as pd
import numpy as np
import re

categories = pd.read_csv('assets/Aircraft_Categories.csv')
landings = pd.read_csv('assets/MSHARP_Landing_Codes.csv')

def AircraftCategory(value):
    try:
        cat = categories[categories['Model'] == value].iloc[0, 1]
        if cat is np.nan:
            return "catch"
        return cat
    except:
        return "catch"
    return "catch"

def MsharpConversion(msharp):
    o_df = None
    if '.csv' in msharp.name:
        o_df = pd.read_csv(msharp, skiprows=6)
    elif '.xlsx' in msharp.name:
        o_df = pd.read_excel(msharp, skiprows=5)

    # get only the data columns and subset with them.
    data = np.arange(o_df.columns.get_loc('Date Range Totals'), o_df.columns.get_loc('T&R'), 1)
    df = o_df.iloc[:, data]

    # Filter applicable top column headers (Hours, Landing, App, T&R, etc.) from the original dataframe
    filtered = filter(lambda name: 'Unnamed' not in name, df.columns)
    top_column_headers = list(filtered)

    # Create a dictionary of {"Column name": "Column Index"}
    header_dict = {}
    for header in top_column_headers:
        column_index = df.columns.get_loc(header)
        header_dict[header] = column_index

    df.iloc[0, 0] = 'Date'
    merged_columns = []
    topHeader = ''
    LANDING_CODE = ''

    for col in range(len(df.columns)):
        columnName = str(df.iloc[0, col])
        if '.' in str(columnName):
            columnName = str(int(float(columnName)))
        tH = list({i for i in header_dict if header_dict[i] == col})

        if len(tH) > 0:
            topHeader = tH[0]

        if 'Landings' in topHeader:
            if columnName != 'nan':
                LANDING_CODE = landings[landings['CODE'] == str(columnName)]['TIME'].iloc[0]
            merged_columns.append(f'{topHeader} {LANDING_CODE}:\n{columnName}')
        elif 'App' in topHeader:
            RE_INT = re.compile(r'\d')
            if RE_INT.match(columnName):
                merged_columns.append(f'{topHeader} Day:\n{columnName}')
            elif len(str(columnName)) == 1:
                merged_columns.append(f'{topHeader} Night:\n{columnName}')
            else:
                merged_columns.append(f'{columnName}')
        else:
            merged_columns.append(f'{columnName}')

    df.columns = merged_columns
    df = df[df.columns.drop(list(df.filter(regex='nan')))]

    lastRow = df[df.iloc[:, 0] == 'Career Totals'].index[0] - 1
    df = df.iloc[2:lastRow].reset_index(drop=True)

    df['Landings Day\nSum'] = df.filter(regex=("Landings Day:")).sum(axis=1)
    df['Landings Night\nSum'] = df.filter(regex=("Landings Night:")).sum(axis=1)

    df['App Day\nSum'] = df.filter(regex=("App Day:")).sum(axis=1)
    df['App Night\nSum'] = df.filter(regex=("App Night:")).sum(axis=1)

    # Add in the Category column based on the TMS/Aircraft
    df.insert(2, 'Category', 'catch')
    df['Category'] = df['Category'].astype(str)
    df['Category'] = df['TMS'].map(AircraftCategory)

    # Setting up types to prevent errors
    df['TPT'] = df['TPT'].astype(float)
    df['FPT'] = df['FPT'].astype(float)

    try:
        df['CPT'] = df['CPT'].astype(float)
    except Exception:
        pass


    df['ACT'] = df['ACT'].astype(float)
    df['SIM'] = df['SIM'].astype(float)
    df['NIGHT'] = df['NIGHT'].astype(float)

    return df