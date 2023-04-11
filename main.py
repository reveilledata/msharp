# Core Pkgs
import streamlit as st
# EDA Pkgs
import pandas as pd
from datetime import datetime, timedelta
# Custom imports
from msharp_pipeline import MsharpConversion


def main():

    st.title("ManyTime Logbooks")

    # """Semi Automated ML App with Streamlit """
    data = st.file_uploader("Upload your MSHARP Data", type=["csv"])
    if data is not None:
        df = MsharpConversion(data)
        df = df[df['TMS'].notna()]
        caught = df[df['Category'] == "catch"]

        if len(caught):
            st.write(f":red[Please provide Categories for these aircraft]")
            aircraft = caught['TMS'].unique()
            st.write(', '.join(aircraft))

        for cat in df['Category'].unique():
            st.header(f"{cat}")

            tmp = df[df['Category'] == cat]
            allAircraft = tmp['TMS'].unique()
            st.write(', '.join(allAircraft))

            # dictionary with list object in values
            item = []
            m6 = []
            m12 = []
            mAll = []

            # 6 months, 12 months, all
            tmp['Date'] = pd.to_datetime(tmp['Date'])
            print(tmp['TPT'].sum())

            end = datetime.today()
            start = datetime.today() - timedelta(days=180)
            mask = (tmp['Date'] > start) & (tmp['Date'] <= end)
            months6 = tmp.loc[mask]

            start = datetime.today() - timedelta(days=365)
            mask = (tmp['Date'] > start) & (tmp['Date'] <= end)
            months12 = tmp.loc[mask]

            item.append('Total')

            m6.append(round(months6['TPT'].sum(), 1))
            m12.append(round(months12['TPT'].sum(), 1))
            mAll.append(round(tmp['TPT'].sum(), 1))

            item.append('PIC')
            m6.append(round(months6['FPT'].sum(), 1))
            m12.append(round(months12['FPT'].sum(), 1))
            mAll.append(round(tmp['FPT'].sum(), 1))

            try:
                m6.append(round(months6['CPT'].sum(), 1))
                m12.append(round(months12['CPT'].sum(), 1))
                mAll.append(round(tmp['CPT'].sum(), 1))
                # this must go last
                item.append('SIC')

            except Exception:
                pass

            item.append('ACT')
            m6.append(round(months6['ACT'].sum(), 1))
            m12.append(round(months12['ACT'].sum(), 1))
            mAll.append(round(tmp['ACT'].sum(), 1))

            item.append('HOOD')
            m6.append(round(months6['SIM'].sum(), 1))
            m12.append(round(months12['SIM'].sum(), 1))
            mAll.append(round(tmp['SIM'].sum(), 1))

            item.append('NIGHT')
            m6.append(round(months6['NIGHT'].sum(), 1))
            m12.append(round(months12['NIGHT'].sum(), 1))
            mAll.append(round(tmp['NIGHT'].sum(), 1))

            item.append('APP DAY')
            m6.append(round(months6['App Day\nSum'].sum(), 1))
            m12.append(round(months12['App Day\nSum'].sum(), 1))
            mAll.append(round(tmp['App Day\nSum'].sum(), 1))

            item.append('APP NIGHT')
            m6.append(round(months6['App Night\nSum'].sum(), 1))
            m12.append(round(months12['App Night\nSum'].sum(), 1))
            mAll.append(round(tmp['App Night\nSum'].sum(), 1))

            item.append('LANDING DAY')
            m6.append(round(months6['Landings Day\nSum'].sum(), 1))
            m12.append(round(months12['Landings Day\nSum'].sum(), 1))
            mAll.append(round(tmp['Landings Day\nSum'].sum(), 1))

            item.append('LANDING NIGHT')
            m6.append(round(months6['Landings Night\nSum'].sum(), 1))
            m12.append(round(months12['Landings Night\nSum'].sum(), 1))
            mAll.append(round(tmp['Landings Night\nSum'].sum(), 1))

            # creating a Dataframe object
            details = {
                ' ': item,
                '6 MONTHS': m6,
                '12 MONTHS': m12,
                'ALL': mAll
            }

            details_df = pd.DataFrame(details).set_index(' ')
            st.dataframe(details_df, use_container_width=True)


if __name__ == '__main__':
    main()
