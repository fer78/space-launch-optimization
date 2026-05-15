from flask import render_template, request

from webapp.services.data_service import (
    get_home_kpis,
    get_launch_sites,
    get_orbits,
    get_booster_versions
)

from webapp.services.plotly_service import (
    create_chart,
    create_launch_sites_map,
    create_gauge_chart
)

from webapp.services.prediction_service import (
    predict_launch_success,
    generate_recommendation
)


def init_app(app):
    """
    Register all application routes.
    """

    # ==========================================================
    # HOME
    # ==========================================================
    @app.route("/")
    def home():
        kpis = get_home_kpis()

        return render_template(
            "home.html",
            total_launches=kpis["total_launches"],
            success_rate=kpis["success_rate"],
            launch_sites=kpis["launch_sites"],
            best_model_accuracy=kpis["best_model_accuracy"]
        )

    # ==========================================================
    # ANALYTICS
    # ==========================================================
    @app.route("/analytics")
    def analytics():
        selected_chart = request.args.get(
            "chart",
            "success_by_site"
        )

        chart_options = [
            {
                "value": "success_by_site",
                "label": "Success Rate by Launch Site"
            },
            {
                "value": "payload_vs_success",
                "label": "Payload Mass vs Success"
            },
            {
                "value": "success_over_time",
                "label": "Success Trend Over Time"
            },
            {
                "value": "orbit_performance",
                "label": "Orbit Type Performance"
            },
            {
                "value": "feature_importance",
                "label": "Feature Importance"
            }
        ]

        fig = create_chart(selected_chart)
        chart_html = fig.to_html(full_html=False)

        return render_template(
            "analytics.html",
            chart_options=chart_options,
            selected_chart=selected_chart,
            chart_html=chart_html
        )

    # ==========================================================
    # MAP
    # ==========================================================
    @app.route("/map")
    def map_view():
        fig = create_launch_sites_map()
        map_html = fig.to_html(full_html=False)

        return render_template(
            "map.html",
            map_html=map_html
        )

    # ==========================================================
    # PREDICTOR
    # ==========================================================
    @app.route("/predictor", methods=["GET", "POST"])
    def predictor():
        launch_sites = get_launch_sites()
        orbits = get_orbits()
        booster_versions = get_booster_versions()

        prediction = None
        gauge_chart = None
        recommendation = None

        if request.method == "POST":
            launch_site = request.form["launch_site"]
            payload_mass = float(request.form["payload_mass"])
            orbit = request.form["orbit"]
            booster_version = request.form["booster_version"]

            probability = predict_launch_success(
                launch_site=launch_site,
                payload_mass=payload_mass,
                orbit=orbit,
                booster_version=booster_version
            )

            prediction = round(probability * 100, 2)

            gauge_fig = create_gauge_chart(prediction)
            gauge_chart = gauge_fig.to_html(full_html=False)

            recommendation = generate_recommendation(prediction)

        return render_template(
            "predictor.html",
            launch_sites=launch_sites,
            orbits=orbits,
            booster_versions=booster_versions,
            prediction=prediction,
            gauge_chart=gauge_chart,
            recommendation=recommendation
        )

    # ==========================================================
    # INSIGHTS
    # ==========================================================
    @app.route("/insights")
    def insights():
        return render_template("insights.html")

    # ==========================================================
    # ABOUT
    # ==========================================================
    @app.route("/about")
    def about():
        return render_template("about.html")
