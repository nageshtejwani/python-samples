from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests


@app.route("/")
def home():
    return "Flask DataFrame Example API is running!"


# Endpoint to upload and process a CSV file
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    # Check if a file is uploaded
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # Read the uploaded CSV file
    file = request.files["file"]
    try:
        # Create a DataFrame from the uploaded CSV file
        df = pd.read_csv(file)

        # Example processing: Add a new column
        df["Sum"] = df.sum(axis=1)

        # Return the DataFrame as JSON
        return jsonify({
            "columns": df.columns.tolist(),
            "data": df.to_dict(orient="records"),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to generate a plot
@app.route("/generate_plot", methods=["POST"])
def generate_plot():
    try:
        # Receive JSON data
        data = request.json
        x_column = data.get("x_column")
        y_column = data.get("y_column")
        df_data = data.get("data")

        # Check if required data is provided
        if not x_column or not y_column or not df_data:
            return jsonify({"error": "Missing required data"}), 400

        # Create a DataFrame from the provided data
        df = pd.DataFrame(df_data)

        # Generate the plot using Matplotlib
        plt.figure()
        plt.plot(df[x_column], df[y_column], marker="o", label="Line Plot")
        plt.title("Generated Plot")
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.legend()

        # Save the plot to a BytesIO buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        # Return the plot as a response
        return send_file(buf, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
