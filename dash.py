import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import io
import base64

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Matplotlib Plot in Dash"),
    html.Div([
        html.Label("X Values (comma-separated):"),
        dcc.Input(id="x_values", value="1,2,3,4,5", type="text"),
        html.Br(),
        html.Label("Y Values (comma-separated):"),
        dcc.Input(id="y_values", value="2,4,6,8,10", type="text"),
        html.Br(),
        html.Button("Generate Plot", id="submit-button", n_clicks=0)
    ]),
    html.Div([
        html.Img(id="plot-image")
    ])
])

# Callback to update the plot
@app.callback(
    Output("plot-image", "src"),
    Input("submit-button", "n_clicks"),
    [Input("x_values", "value"), Input("y_values", "value")]
)
def update_plot(n_clicks, x_values, y_values):
    if n_clicks > 0:
        x = list(map(float, x_values.split(",")))
        y = list(map(float, y_values.split(",")))

        # Generate the Matplotlib plot
        plt.figure()
        plt.plot(x, y, marker="o")
        plt.title("Sample Plot")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")

        # Save the plot to a BytesIO buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        # Encode the image as base64
        encoded_image = base64.b64encode(buf.getvalue()).decode("utf-8")
        return "data:image/png;base64,{}".format(encoded_image)

    return None

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
