import requests
import pandas as pd
import streamlit as st

API_KEY = st.secrets["MONDAY_API_KEY"]
def fetch_board(board_id):

    query = f"""
    {{
      boards(ids: {board_id}) {{
        items_page {{
          items {{
            name
            column_values {{
              text
              column {{
                title
              }}
            }}
          }}
        }}
      }}
    }}
    """

    url = "https://api.monday.com/v2"

    response = requests.post(
        url,
        json={"query": query},
        headers={"Authorization": API_KEY}
    )

    data = response.json()

    items = data["data"]["boards"][0]["items_page"]["items"]

    rows = []

    for item in items:

        row = {"Item Name": item["name"]}

        for col in item["column_values"]:
            row[col["column"]["title"]] = col["text"]

        rows.append(row)

    df = pd.DataFrame(rows)

    return df


