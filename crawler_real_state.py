import streamlit as st
import requests
import pandas as pd
import pickle
import os

# Streamlit page setup
st.set_page_config(page_title="Real Estate Listings Viewer", layout="wide")
st.title("Real Estate Listings from Pages 1 to 10")
st.markdown("This page fetches and displays real estate listings from pages 1 to 10 using the Naver Real Estate API.")

# Define the cookies and headers as provided
cookies = {
        'NNB': 'SCHAX5MQP2HWK',
    'ASID': '3a7b4bba00000190dfe8f22a00000062',
    '_fwb': '89pcEbHw2rEpEPDoyQ21Xj.1723596435870',
    '_fwb': '89pcEbHw2rEpEPDoyQ21Xj.1723596435870',
    'NID_AUT': '9t3J+GHxEl81jTuzN9/Q6ulbGUMTytUjMfZueAWQN55KWscvZjOQsA77GwspmG/A',
    'NID_JKL': 'hJnoyV7uGSAGkTNT6eItIQp9E6Tea/1RVVmXr3FZJNg=',
    'wcs_bt': '4f99b5681ce60:1724250328',
    'SHOW_FIN_BADGE': 'Y',
    'ab.storage.deviceId.59fcdfdf-df7d-4ae5-85c9-27c62228b306': 'g%3Ace529e01-98bd-6d85-4425-522532ba0ddc%7Ce%3Aundefined%7Cc%3A1732801406659%7Cl%3A1733024469056',
    'ab.storage.userId.59fcdfdf-df7d-4ae5-85c9-27c62228b306': 'g%3AW3g7%7Ce%3Aundefined%7Cc%3A1732801406650%7Cl%3A1733024469057',
    'ab.storage.sessionId.59fcdfdf-df7d-4ae5-85c9-27c62228b306': 'g%3A25d5b8f1-6471-2f21-ee00-635f095d2906%7Ce%3A1733027576251%7Cc%3A1733024469055%7Cl%3A1733025776251',
    'NAC': 'vma0BcwFsv0m',
    'nhn.realestate.article.rlet_type_cd': 'A01',
    'nhn.realestate.article.trade_type_cd': '""',
    'nhn.realestate.article.ipaddress_city': '1100000000',
    'landHomeFlashUseYn': 'Y',
    'realestate.beta.lastclick.cortar': '1147000000',
    'NACT': '1',
    'NID_SES': 'AAABtX9BdYRnziQL6tmRu1pJV8BVENL8amDR+KqmtdVjoDZ/0iTXI940Ji5Q5MbUAA8ek/JBm1e9fXNsShZbwYXrMhOL/BAiFPEJkH5yZhvXZsgru+kWziUjtV8qVpn5VeAIGiGQqvS/u24mQs5jYjZU2SWXwOLTXEylprF7dlrBONDHEbOedVZxGLnI+FOOG/lhLaQDOiquyQWRAtprGg+bgyWeNYegG0DeAMrk8mhij89j2u1EP3t333yUTJV+tj/jYJIqvoq10KcL75UrFOmSfxgOTrpQmgTcv8+JYalnAleiyZxas8b8+G15b924KfUwrEYdVgIphuf/0JHn3BNs+6j4ROajZcj9pgvxG2ta2280lc/teYTcC1IOvgV/5+iYCe3BRWGWIyomH4prE8xcYrBWSY4a5tUQ8OAEepkkVCvLk/2bnW9q+9kIV0Wockr/tgs7gLbVfgDq14GwipLAHvAg0MQiWggx2yul42w/gQr8IheWuYm9U2s0LaHjVWHanzTUJlaSCnC0J5DFe8zYwg9iyvgkTchInaTmNratTclm7J3yt4hBuKezUmEAateJTA4ByFsYOzp4RSuQrTtfA1k=',
    'SRT30': '1735731903',
    'BUC': '-A8X-RqR2Nqb1Tck349W8g2bSIyVsYViAkP-mxug0MI=',
    'REALESTATE': 'Wed%20Jan%2001%202025%2020%3A54%3A27%20GMT%2B0900%20(Korean%20Standard%20Time)',
}
headers = {
    'accept': '*/*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3MzU3MzI0NjcsImV4cCI6MTczNTc0MzI2N30.KJYB7C0GAJHu3fTXAGrY6DvMxLHDEgZilM7Mj0q5o3s',
    # 'cookie': 'NNB=SCHAX5MQP2HWK; ASID=3a7b4bba00000190dfe8f22a00000062; _fwb=89pcEbHw2rEpEPDoyQ21Xj.1723596435870; _fwb=89pcEbHw2rEpEPDoyQ21Xj.1723596435870; NID_AUT=9t3J+GHxEl81jTuzN9/Q6ulbGUMTytUjMfZueAWQN55KWscvZjOQsA77GwspmG/A; NID_JKL=hJnoyV7uGSAGkTNT6eItIQp9E6Tea/1RVVmXr3FZJNg=; wcs_bt=4f99b5681ce60:1724250328; SHOW_FIN_BADGE=Y; ab.storage.deviceId.59fcdfdf-df7d-4ae5-85c9-27c62228b306=g%3Ace529e01-98bd-6d85-4425-522532ba0ddc%7Ce%3Aundefined%7Cc%3A1732801406659%7Cl%3A1733024469056; ab.storage.userId.59fcdfdf-df7d-4ae5-85c9-27c62228b306=g%3AW3g7%7Ce%3Aundefined%7Cc%3A1732801406650%7Cl%3A1733024469057; ab.storage.sessionId.59fcdfdf-df7d-4ae5-85c9-27c62228b306=g%3A25d5b8f1-6471-2f21-ee00-635f095d2906%7Ce%3A1733027576251%7Cc%3A1733024469055%7Cl%3A1733025776251; NAC=vma0BcwFsv0m; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=""; nhn.realestate.article.ipaddress_city=1100000000; landHomeFlashUseYn=Y; realestate.beta.lastclick.cortar=1147000000; NACT=1; NID_SES=AAABtX9BdYRnziQL6tmRu1pJV8BVENL8amDR+KqmtdVjoDZ/0iTXI940Ji5Q5MbUAA8ek/JBm1e9fXNsShZbwYXrMhOL/BAiFPEJkH5yZhvXZsgru+kWziUjtV8qVpn5VeAIGiGQqvS/u24mQs5jYjZU2SWXwOLTXEylprF7dlrBONDHEbOedVZxGLnI+FOOG/lhLaQDOiquyQWRAtprGg+bgyWeNYegG0DeAMrk8mhij89j2u1EP3t333yUTJV+tj/jYJIqvoq10KcL75UrFOmSfxgOTrpQmgTcv8+JYalnAleiyZxas8b8+G15b924KfUwrEYdVgIphuf/0JHn3BNs+6j4ROajZcj9pgvxG2ta2280lc/teYTcC1IOvgV/5+iYCe3BRWGWIyomH4prE8xcYrBWSY4a5tUQ8OAEepkkVCvLk/2bnW9q+9kIV0Wockr/tgs7gLbVfgDq14GwipLAHvAg0MQiWggx2yul42w/gQr8IheWuYm9U2s0LaHjVWHanzTUJlaSCnC0J5DFe8zYwg9iyvgkTchInaTmNratTclm7J3yt4hBuKezUmEAateJTA4ByFsYOzp4RSuQrTtfA1k=; SRT30=1735731903; BUC=-A8X-RqR2Nqb1Tck349W8g2bSIyVsYViAkP-mxug0MI=; REALESTATE=Wed%20Jan%2001%202025%2020%3A54%3A27%20GMT%2B0900%20(Korean%20Standard%20Time)',
    'priority': 'u=1, i',
    'referer': 'https://new.land.naver.com/complexes/652?ms=37.5379028,126.8807896,16&a=PRE:JGC&e=RETAIL',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

pickle_file = "real_estate_data.pkl"

# Function to get data from the API for pages 1 to 10
@st.cache_data
def fetch_all_data():
    all_articles = []
    for page in range(1, 11):
        try:
            # Make the request for the specific page
            url = f'https://new.land.naver.com/api/articles/complex/652?realEstateType=PRE%3AJGC&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=652&buildingNos=&areaNos=&type=list&order=rank'
            response = requests.get(url, cookies=cookies, headers=headers)

            # Verify response is valid JSON
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articleList", [])
                all_articles.extend(articles)
            else:
                st.warning(f"Failed to retrieve data for page {page}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except ValueError:
            st.error(f"Non-JSON response for page {page}.")
    return all_articles

# Function to load existing pickle data
def load_existing_data(pickle_file):
    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as f:
            existing_data = pickle.load(f)
        return pd.DataFrame(existing_data)
    return pd.DataFrame()  # Return empty DataFrame if no file exists

# Function to save updated data to pickle
def save_data_to_pickle(data, pickle_file):
    with open(pickle_file, "wb") as f:
        pickle.dump(data, f)

# Fetch data for all pages
new_data = fetch_all_data()

# Transform data into a DataFrame if data is available
if new_data:
    new_df = pd.DataFrame(new_data)

    # Load existing data from pickle
    existing_df = load_existing_data(pickle_file)

    # Combine new data with existing data and remove duplicates
    combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset="articleNo", keep="last")

    # Save updated data to pickle
    save_data_to_pickle(combined_df.to_dict(orient="records"), pickle_file)

    # Display the updated data
    st.write("### Real Estate Listings - Updated Data")
    st.dataframe(combined_df)

    # Add a button to save the data as a CSV file
    csv_data = combined_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Updated CSV",
        data=csv_data,
        file_name="updated_real_estate_listings.csv",
        mime="text/csv",
    )
else:
    st.write("No new data available.")