import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load data
df = pd.read_csv("upsc.csv")

# Added three new columns for adjusting marks scale
df["interview"] = (df.ptpct * 275).apply(int)
df["written"] = (df.wtpct * 1750).apply(round).apply(int)
df["total"] = (df.ftpct * 2025).apply(round).apply(int)

# Fixed colors for each 'Comm' category
comm_colors = {
    "OBC": "rgb(251,180,174)",  # Pastel1[0]
    "SC": "rgb(204,235, 197)",  # Pastel1[1]
    "ST": "rgb(222, 203, 228)",  # Pastel1[3]
    "GEN": "rgb(254, 217, 166)",  # Pastel1[4]
}

# Streamlit app
st.title("UPSC Result (2007-2017) : Data Analysis ")
st.markdown("")
st.markdown("")

# Sidebar for sliders
st.sidebar.header("Select Parameters to customize your analysis")

# Default values for range, year, and all data
default_comm = df["category"].unique()
default_written_range = (df["written"].min(), df["written"].max())
default_interview_range = (df["interview"].min(), df["interview"].max())
default_rank_range = (1, 1250)
default_year_range = (2007, 2017)

# Dropdown for filtering by 'category'
selected_comm = st.sidebar.multiselect(
    "Select Category (s)", df["category"].unique(), default_comm
)

# Slider for filtering by 'written'
written_range = st.sidebar.slider(
    "Select range for written marks",
    int(df["written"].min()),
    int(df["written"].max()),
    default_written_range,
    step=25,
)

# Slider for filtering by 'interview'
interview_range = st.sidebar.slider(
    "Select range for interview marks",
    int(df["interview"].min()),
    int(df["interview"].max()),
    default_interview_range,
    step=25,
)

# Year slider
year_range = st.sidebar.slider(
    "Select range for UPSC Exam Year",
    2007,
    2017,
    default_year_range,
    step=1,
)

# Slider for filtering by 'rank'
rank_range = st.sidebar.slider(
    "Select range for UPSC All India Ranks to display",
    1,
    1250,
    default_rank_range,
    step=25,
)

# ...

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
    title="",
    # opacity=0.5,
)
pie_fig.update_traces(
    hoverinfo="label+percent", textinfo="percent+label", textfont_size=15
)

# Comments for Pie chart

st.markdown("")
st.markdown("")
st.header("Categories wise candidates distribution")
st.plotly_chart(pie_fig)

st.markdown("")
st.markdown("")


########################################################################################
# Scatter plot with fixed color mapping
scatter_fig = px.scatter(
    filtered_df,
    x="written",
    y="interview",
    color="category",
    color_discrete_map=comm_colors,
    title="",
)

# Add x and y-axis labels
scatter_fig.update_layout(xaxis_title="Written Marks", yaxis_title="Interview Marks")

# Show plot
st.header("Interview vs Written Marks by Categories")
st.plotly_chart(scatter_fig)
st.markdown("")
st.markdown("")

########################################################################################
# Scatter plots for mean/median interview vs written marks for different categories

# Calculate mean and median for each category
category_stats = filtered_df.groupby("category").agg(
    {"interview": ["mean", "median"], "written": ["mean", "median"]}
)
category_stats.reset_index(inplace=True)
category_stats.columns = [
    "category",
    "mean_interview",
    "median_interview",
    "mean_written",
    "median_written",
]

# Scatter plot for mean interview vs written marks
mean_scatter_fig = px.scatter(
    category_stats,
    x="mean_written",
    y="mean_interview",
    color="category",
    color_discrete_map=comm_colors,
    title="Mean Interview vs Written Marks by Categories",
    text="category",  # Display category names on the plot
)

# Update x-axis range
mean_scatter_fig.update_xaxes(range=[500, 1200])

# Add x and y-axis labels
mean_scatter_fig.update_layout(
    xaxis_title="Mean Written Marks", yaxis_title="Mean Interview Marks"
)

# Place text below points
mean_scatter_fig.update_traces(textposition="bottom center")

# Show plot
st.header("Mean Interview vs Mean Written Marks by Categories")
st.plotly_chart(mean_scatter_fig)
st.markdown("")
st.markdown("")

# Scatter plot for median interview vs written marks
median_scatter_fig = px.scatter(
    category_stats,
    x="median_written",
    y="median_interview",
    color="category",
    color_discrete_map=comm_colors,
    title="Median Interview vs Written Marks by Categories",
    text="category",  # Display category names on the plot
)

# Update x-axis range
median_scatter_fig.update_xaxes(range=[500, 1200])

# Add x and y-axis labels
median_scatter_fig.update_layout(
    xaxis_title="Median Written Marks", yaxis_title="Median Interview Marks"
)

# Place text below points
median_scatter_fig.update_traces(textposition="bottom center")

# Show plot
st.header("Median Interview vs Median Written Marks by Categories")
st.plotly_chart(median_scatter_fig)
st.markdown("")
st.markdown("")


#########################################################################################################

# Calculate top and bottom 10 percentile thresholds
top_10_percentile_written = df["written"].quantile(0.9)
bottom_10_percentile_written = df["written"].quantile(0.1)
top_10_percentile_interview = df["interview"].quantile(0.9)
bottom_10_percentile_interview = df["interview"].quantile(0.1)

# Filter top and bottom 10 percentile scores
top_10_percentile_df = df[
    (df["written"] >= top_10_percentile_written)
    & (df["interview"] >= top_10_percentile_interview)
]
bottom_10_percentile_df = df[
    (df["written"] <= bottom_10_percentile_written)
    & (df["interview"] <= bottom_10_percentile_interview)
]

# Scatter plot for top 10 percentile written vs interview marks
top_10_percentile_scatter_fig = px.scatter(
    top_10_percentile_df,
    x="written",
    y="interview",
    color="category",
    color_discrete_map=comm_colors,
    title="Top 10 Percentile: Written vs Interview Marks by Categories",
)

# Update x-axis range
top_10_percentile_scatter_fig.update_xaxes(range=[500, 1200])

# Add x and y-axis labels
top_10_percentile_scatter_fig.update_layout(
    xaxis_title="Written Marks", yaxis_title="Interview Marks"
)

# Show plot
st.header("Top 10 Percentile: Written vs Interview Marks by Categories")
st.plotly_chart(top_10_percentile_scatter_fig)
st.markdown("")
st.markdown("")

# Scatter plot for bottom 10 percentile written vs interview marks
bottom_10_percentile_scatter_fig = px.scatter(
    bottom_10_percentile_df,
    x="written",
    y="interview",
    color="category",
    color_discrete_map=comm_colors,
    title="Bottom 10 Percentile: Written vs Interview Marks by Categories",
)

# Update x-axis range
bottom_10_percentile_scatter_fig.update_xaxes(range=[500, 1200])

# Add x and y-axis labels
bottom_10_percentile_scatter_fig.update_layout(
    xaxis_title="Written Marks", yaxis_title="Interview Marks"
)

# Show plot
st.header("Bottom 10 Percentile: Written vs Interview Marks by Categories")
st.plotly_chart(bottom_10_percentile_scatter_fig)
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
    title="",
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
st.header("Distribution of Categories Wise Interview Marks)")
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
    title="",
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
st.header("Distribution of Categories Wise Written Marks")
st.plotly_chart(box_fig_written)
st.markdown("")
st.markdown("")


###################################################################################################################
###Histograms
# Show the plot for written marks
st.header("Histogram of Written Marks by Category")
histogram_written = px.histogram(
    filtered_df,
    x="written",
    color="category",
    barmode="overlay",
    title="Histogram of Written Marks by Category",
    labels={"written": "Written Marks", "category": "Category"},
    histnorm="percent",  # Normalize y-axis to percentages
    color_discrete_map=comm_colors,
)
st.plotly_chart(histogram_written)

# Show the plot for interview marks
st.header("Histogram of Interview Marks by Category")
histogram_interview = px.histogram(
    filtered_df,
    x="interview",
    color="category",
    barmode="overlay",
    title="Histogram of Interview Marks by Category",
    labels={"interview": "Interview Marks", "category": "Category"},
    histnorm="percent",  # Normalize y-axis to percentages
    color_discrete_map=comm_colors,
)
st.plotly_chart(histogram_interview)
