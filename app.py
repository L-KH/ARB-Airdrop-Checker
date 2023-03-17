from flask import Flask, render_template, request
import pandas as pd
import requests
from io import StringIO

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        addresses = request.form.get("addresses")
        addresses = set(address.lower().strip() for address in addresses.splitlines())

        # Download the CSV file from the given URL
        url = 'https://raw.githubusercontent.com/0xtoshi/arbichecker/main/eligible.csv'
        response = requests.get(url)
        response.raise_for_status()

        # Read the CSV file into a Pandas DataFrame
        csv_data = pd.read_csv(StringIO(response.text), low_memory=False)

        # Check if an address in the row is in the addresses set
        def check_row(row):
            return row["_recipients"].lower() in addresses

        # Find matching rows
        matching_rows = csv_data[csv_data.apply(check_row, axis=1)]

        return matching_rows.to_html(index=False)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
