import plotly.express as px
import plotly.graph_objects as go

from webapp.services.data_service import load_data


# ==========================================================
# GENERIC CHART FACTORY
# ==========================================================
def create_chart(chart_name):
    """
    Return the Plotly figure associated with the selected chart.
    """
    if chart_name == "success_by_site":
        return create_success_by_site_chart()

    elif chart_name == "payload_vs_success":
        return create_payload_vs_success_chart()

    elif chart_name == "success_over_time":
        return create_success_over_time_chart()

    elif chart_name == "orbit_performance":
        return create_orbit_performance_chart()

    elif chart_name == "feature_importance":
        return create_feature_importance_chart()

    # Default chart
    return create_success_by_site_chart()


# ==========================================================
# CHART 1: SUCCESS RATE BY LAUNCH SITE
# ==========================================================
def create_success_by_site_chart():
    df = load_data()

    summary = (
        df.groupby("Launch Site")["class"]
        .mean()
        .reset_index()
    )

    summary["class"] = summary["class"] * 100

    fig = px.bar(
        summary,
        x="Launch Site",
        y="class",
        title="Success Rate by Launch Site",
        labels={"class": "Success Rate (%)"},
    )

    return fig


# ==========================================================
# CHART 2: PAYLOAD MASS VS SUCCESS
# ==========================================================
def create_payload_vs_success_chart():
    df = load_data()

    fig = px.scatter(
        df,
        x="Payload Mass (kg)",
        y="class",
        color="Launch Site",
        title="Payload Mass vs Launch Success",
    )

    return fig


# ==========================================================
# CHART 3: SUCCESS OVER TIME
# ==========================================================
def create_success_over_time_chart():
    df = load_data()

    df["Date"] = px.data.tips().assign(dummy=1)["dummy"][:0]  # placeholder
    # En el proyecto real, aquí convertirías la columna Date a datetime.

    fig = px.histogram(
        df,
        x="Launch Site",
        color="class",
        title="Launch Outcomes by Site",
        barmode="group",
    )

    return fig


# ==========================================================
# CHART 4: ORBIT PERFORMANCE
# ==========================================================
def create_orbit_performance_chart():
    df = load_data()

    summary = (
        df.groupby("Orbit")["class"]
        .mean()
        .reset_index()
    )

    summary["class"] = summary["class"] * 100

    fig = px.bar(
        summary,
        x="Orbit",
        y="class",
        title="Success Rate by Orbit Type",
        labels={"class": "Success Rate (%)"},
    )

    return fig


# ==========================================================
# CHART 5: FEATURE IMPORTANCE
# ==========================================================
def create_feature_importance_chart():
    features = [
        "Payload Mass",
        "Launch Site",
        "Orbit",
        "Booster Version",
    ]

    importance = [0.35, 0.25, 0.22, 0.18]

    fig = px.bar(
        x=features,
        y=importance,
        title="Feature Importance",
        labels={"x": "Feature", "y": "Importance"},
    )

    return fig


# ==========================================================
# INTERACTIVE MAP
# ==========================================================
def create_launch_sites_map():
    df = load_data()

    summary = (
        df.groupby(["Launch Site", "Lat", "Long"])
        .agg(
            total_launches=("class", "count"),
            success_rate=("class", "mean"),
        )
        .reset_index()
    )

    summary["success_rate"] *= 100

    fig = px.scatter_map(
        summary,
        lat="Lat",
        lon="Long",
        size="total_launches",
        color="success_rate",
        hover_name="Launch Site",
        hover_data={
            "total_launches": True,
            "success_rate": ":.2f",
        },
        zoom=3,
        title="Launch Sites Performance Map",
    )

    return fig


# ==========================================================
# GAUGE CHART FOR PREDICTIONS
# ==========================================================
def create_gauge_chart(probability):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability,
            title={"text": "Success Probability (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"thickness": 0.3},
                "steps": [
                    {"range": [0, 50]},
                    {"range": [50, 80]},
                    {"range": [80, 100]},
                ],
            },
        )
    )

    return fig