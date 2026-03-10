import requests
import pandas as pd
import os

API_KEY = os.getenv("eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYzMTAxMzQ2MywiYWFpIjoxMSwidWlkIjoxMDA4MTI4NzIsImlhZCI6IjIwMjYtMDMtMTBUMDY6MjM6MjYuNjEyWiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM0MTUzMzY4LCJyZ24iOiJhcHNlMiJ9.8UkdXSKeYf9vEqPz99XR10clvQAFECn2kNt6uIb32Ao")


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

