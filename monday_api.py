import requests
import pandas as pd
import os

API_KEY = os.getenv("eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYzMTAxMzQ2MywiYWFpIjoxMSwidWlkIjoxMDA4MTI4NzIsImlhZCI6IjIwMjYtMDMtMTBUMDY6MjM6MjYuNjEyWiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM0MTUzMzY4LCJyZ24iOiJhcHNlMiJ9.8UkdXSKeYf9vEqPz99XR10clvQAFECn2kNt6uIb32Ao")



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

    try:

        response = requests.post(
            url,
            json={"query": query},
            headers={"Authorization": API_KEY},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException:

        raise Exception("Failed to connect to Monday API")


    try:

        items = data["data"]["boards"][0]["items_page"]["items"]

    except:

        raise Exception("Invalid board data received from Monday API")


    rows = []

    for item in items:

        row = {"Item Name": item["name"]}

        for col in item["column_values"]:
            row[col["column"]["title"]] = col["text"]

        rows.append(row)

    df = pd.DataFrame(rows)

    return df