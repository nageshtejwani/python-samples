import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Title for the app
st.title("Interactive Data Plotting with Matplotlib and DataFrame")

# Sidebar for user options
st.sidebar.header("Input Options")

# Option to upload a CSV file
upload_option = st.sidebar.radio(
    "Select Input Type", ["Manual Input", "Upload CSV"]
)

if upload_option == "Manual Input":
    # Manual input for X and Y values
    x_values = st.sidebar.text_input(
        "X Values (comma-separated)", "1,2,3,4,5"
    )
    y_values = st.sidebar.text_input(
        "Y Values (comma-separated)", "2,4,6,8,10"
    )

    # Parse the inputs into a DataFrame
    try:
        x = list(map(float, x_values.split(",")))
        y = list(map(float, y_values.split(",")))

        if len(x) != len(y):
            st.error("The number of X and Y values must match.")
            df = None
        else:
            df = pd.DataFrame({"X": x, "Y": y})
    except ValueError:
        st.error("Please enter valid numeric values for X and Y.")
        df = None

elif upload_option == "Upload CSV":
    # File uploader for CSV
    uploaded_file = st.sidebar.file_uploader("Upload a CSV File", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded DataFrame:")
        st.dataframe(df)
    else:
        st.info("Please upload a CSV file.")
        df = None

# If a valid DataFrame is available
if df is not None:
    # Display the DataFrame
    st.write("## Data Preview")
    st.dataframe(df)

    # Dropdown to select columns for plotting
    x_column = st.selectbox("Select X-axis Column", df.columns)
    y_column = st.selectbox("Select Y-axis Column", df.columns)

    # Dropdown to select plot type
    plot_type = st.selectbox(
        "Select Plot Type", ["Line Plot", "Scatter Plot", "Bar Plot"]
    )

    # Button to generate the plot
    if st.button("Generate Plot"):
        try:
            # Create the plot
            fig, ax = plt.subplots()
            if plot_type == "Line Plot":
                ax.plot(df[x_column], df[y_column], marker="o", label="Line Plot")
            elif plot_type == "Scatter Plot":
                ax.scatter(df[x_column], df[y_column], color="red", label="Scatter Plot")
            elif plot_type == "Bar Plot":
                ax.bar(df[x_column], df[y_column], color="green", label="Bar Plot")

            # Customize the plot
            ax.set_title("Generated Plot")
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.legend()

            # Display the plot
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error generating plot: {e}")

