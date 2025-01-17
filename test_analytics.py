@app.route("/plot_single_day/<date_column>/<value_column>", methods=["GET"])
def plot_single_day(date_column, value_column):
    try:
        # Ensure the date column exists
        if date_column not in df.columns or value_column not in df.columns:
            return jsonify({"error": f"Columns {date_column} or {value_column} not found"}), 400

        # Convert the date column to datetime
        df[date_column] = pd.to_datetime(df[date_column])

        # Prepare the plot
        plt.figure(figsize=(8, 5))
        plt.plot(df[date_column], df[value_column], marker="o", label=f"{value_column} on {date_column}")

        # If there's only one record, explicitly set x-axis limits to center on that date
        if len(df) == 1:
            single_date = df[date_column].iloc[0]
            plt.xlim(single_date - pd.Timedelta(days=1), single_date + pd.Timedelta(days=1))

        # Improve plot aesthetics
        plt.title(f"Single-Day Plot of {value_column}")
        plt.xlabel("Date")
        plt.ylabel(value_column)
        plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
        plt.grid(True)
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
