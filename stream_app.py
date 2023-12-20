import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("upsc.csv")

# Added three new columns for adjusting marks scale
df["interview"] = (df.ptpct * 275).astype(int)
df["written"] = (df.wtpct * 1750).round().astype(int)
df["total"] = (df.ftpct * 2025).round().astype(int)


# Fixed colors for each 'Comm' category
comm_colors = {
    "OBC": "rgb(251,180,174)",  # Pastel1[0]
    "SC": "rgb(179,205, 227)",  # Pastel1[1]
    "ST": "rgb(222, 203, 228)",  # Pastel1[3]
    "GEN": "rgb(254, 217, 166)",  # Pastel1[4]
}

# Streamlit app
st.title("UPSC Result (2007-2017) : Data Analysis ")
st.markdown("")
st.markdown("")

st.header("Select Parameters for Customized Visualizations")

# Default values for range, year, and all data
default_comm = df["category"].unique()
default_written_range = (df["written"].min(), df["written"].max())
default_interview_range = (df["interview"].min(), df["interview"].max())
default_rank_range = (1, 1250)
default_year_range = (2007, 2017)

# Dropdown for filtering by 'category'
selected_comm = st.multiselect("Select Category", df["category"].unique(), default_comm)

# Slider for filtering by 'written'
w_total_range = st.slider(
    "Select range for written marks",
    int(upsc_2022_df["W_total"].min()),
    int(upsc_2022_df["W_total"].max()),
    (int(default_w_total_range[0]), int(default_w_total_range[1])),
    step=25,
)


# Slider for filtering by 'interview'
interview_range = st.slider(
    "Select range for interview marks",
    df["interview"].min(),
    df["interview"].max(),
    default_interview_range,
    step=25,
)

# Year slider
year_range = st.slider(
    "Select range for UPSC Exam Year",
    2007,
    2017,
    default_year_range,
    step=1,
)

# Slider for filtering by 'rank'
rank_range = st.slider(
    "Select range for UPSC All India Ranks to display",
    1,
    1250,
    default_rank_range,
    step=25,
)

# Filter the DataFrame based on user input
filtered_df = df[
    (df["category"].isin(selected_comm))
    & (df["written"] >= written_range[0])
    & (df["written"] <= written_range[1])
    & (df["interview"] >= interview_range[0])
    & (df["interview"] <= interview_range[1])
    & (df["year"] >= year_range[0])
    & (df["year"] <= year_range[1])
    & (df["rank"] >= rank_range[0])
    & (df["rank"] <= rank_range[1])
]

# Scatter plot with fixed color mapping
scatter_fig = px.scatter(
    filtered_df,
    x="written",
    y="interview",
    color="category",
    color_discrete_map=comm_colors,
    title="Interview vs Written Marks in UPSC by Categories",
)

# Add x and y-axis labels
scatter_fig.update_layout(xaxis_title="Written Marks", yaxis_title="Interview Marks")

# Comments for Scatter plot
st.header("Scatter Plot")
st.plotly_chart(scatter_fig)
st.markdown("")
st.markdown("")

###################################################################################################################

# Pie chart
comm_counts = filtered_df["category"].value_counts()
pie_fig = px.pie(
    comm_counts,
    names=comm_counts.index,
    values=comm_counts.values,
    hole=0.3,
    color=comm_counts.index,
    color_discrete_map=comm_colors,
    title="Interview vs Written Marks in UPSC by Categories",
    opacity=0.7,
)
pie_fig.update_traces(
    hoverinfo="label+percent", textinfo="percent+label", textfont_size=15
)

# Comments for Pie chart
st.write("# Pie Chart")
st.plotly_chart(pie_fig)

st.markdown("")
st.markdown("")


###################################################################################################################
# Box plot for 'interview'
box_fig = px.box(
    filtered_df,
    x="interview",
    y="category",
    color="category",
    labels={"interview": "Interview Marks", "category": "Categories"},
    category_orders={"category": selected_comm},
    color_discrete_map=comm_colors,
    title="Distribution of Categories Wise Interview Marks",
)

# Add a vertical line for the full data median
full_data_median = df["interview"].median()
box_fig.update_layout(
    shapes=[
        {
            "type": "line",
            "x0": full_data_median,
            "x1": full_data_median,
            "y0": -0.5,
            "y1": len(selected_comm) - 0.5,
            "xref": "x",
            "yref": "y",
            "line": dict(color="red", width=2),
        },
    ],
    annotations=[
        dict(
            x=1.15,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            align="left",
            font=dict(size=12),
        )
    ],
)

# Comments for Box plot
st.write("# Box Plot (Interview Marks)")
st.plotly_chart(box_fig)
st.markdown("")
st.markdown("")

###################################################################################################################
# Box plot for 'written' marks
box_fig_written = px.box(
    filtered_df,
    x="written",
    y="category",
    color="category",
    labels={"written": "Written Marks", "category": "Categories"},
    category_orders={"category": selected_comm},
    color_discrete_map=comm_colors,
    title="Distribution of Categories Wise Written Marks",
)

# Add a vertical line for the full data median
full_data_median_written = df["written"].median()
box_fig_written.update_layout(
    shapes=[
        {
            "type": "line",
            "x0": full_data_median_written,
            "x1": full_data_median_written,
            "y0": -0.5,
            "y1": len(selected_comm) - 0.5,
            "xref": "x",
            "yref": "y",
            "line": dict(color="red", width=2),
        },
    ],
    annotations=[
        dict(
            x=1.15,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            align="left",
            font=dict(size=12),
        )
    ],
)

# Comments for Box plot (Written Marks)
st.write("# Box Plot (Written Marks)")
st.plotly_chart(box_fig_written)
st.markdown("")
st.markdown("")


###################################################################################################################
# Add histograms for 'interview'
fig_interview = go.Figure()

for comm, color in comm_colors.items():
    hist_data_comm = filtered_df[filtered_df["category"] == comm]["interview"]
    fig_interview.add_trace(
        go.Histogram(
            x=hist_data_comm,
            histnorm="probability",
            name=comm,
            marker_color=f"{color}",
            opacity=0.7,
        )
    )

fig_interview.update_layout(
    barmode="overlay",
    title_text="Distribution of Interview Marks",
    xaxis_title="Interview Marks",
    yaxis_title="Probability",
)

# Comments for Histogram (Interview Marks)
st.write("# Histogram (Interview Marks)")
st.plotly_chart(fig_interview)


###################################################################################################################
# Written Marks

fig_written = go.Figure()

for comm, color in comm_colors.items():
    hist_data_comm = filtered_df[filtered_df["category"] == comm]["written"]
    fig_written.add_trace(
        go.Histogram(
            x=hist_data_comm,
            histnorm="probability",
            name=comm,
            marker_color=f"{color}",
            opacity=0.7,
        )
    )

fig_written.update_layout(
    barmode="overlay",
    title_text="Distribution of Written Marks",
    xaxis_title="Written Marks",
    yaxis_title="Probability",
)

# Comments for Histogram (Written Marks)
st.write("# Histogram (Written Marks)")
st.plotly_chart(fig_written)

# Add another blank row with an empty string
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
