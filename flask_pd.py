from flask import Flask, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Sample DataFrame
df = pd.DataFrame({
    "X": [1, 2, 3, 4, 5],
    "Y": [2, 4, 6, 8, 10],
    "Z": [1, 3, 5, 7, 9]
})


@app.route("/")
def home():
    return "Flask DataFrame Example API is running!"


# Endpoint to get the DataFrame as JSON
@app.route("/dataframe", methods=["GET"])
def get_dataframe():
    return jsonify({
        "columns": df.columns.tolist(),
        "data": df.to_dict(orient="records")
    })


# Endpoint to generate a plot
@app.route("/plot/<x_column>/<y_column>", methods=["GET"])
def generate_plot(x_column, y_column):
    try:
        # Check if the specified columns exist in the DataFrame
        if x_column not in df.columns or y_column not in df.columns:
            return jsonify({"error": f"Columns {x_column} or {y_column} not found"}), 400

        # Generate the plot using Matplotlib
        plt.figure()
        plt.plot(df[x_column], df[y_column], marker="o", label=f"{x_column} vs {y_column}")
        plt.title(f"Plot of {y_column} vs {x_column}")
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
