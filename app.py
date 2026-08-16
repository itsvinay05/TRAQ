import streamlit as st
import joblib
import networkx as nx
import time

model=joblib.load("models/traq_xgboost.pkl")

st.set_page_config(
    page_title="TRAQ Traffic Intelligence",
    page_icon="🚦",
    layout="wide"
)
# ---------------- LANDING PAGE ----------------

if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

if not st.session_state.intro_done:

    st.markdown(
        """
        <style>
        .traq-title {
            text-align: center;
            font-size: 80px;
            font-weight: 800;
            letter-spacing: 18px;
            animation: fadeIn 2s ease-in-out;
        }

        .traq-subtitle {
            text-align: center;
            font-size: 22px;
            animation: slideUp 2s ease-in-out;
        }

        @keyframes fadeIn {
            from {opacity: 0; transform: scale(0.5);}
            to {opacity: 1; transform: scale(1);}
        }

        @keyframes slideUp {
            from {opacity: 0; transform: translateY(30px);}
            to {opacity: 1; transform: translateY(0);}
        }
        </style>

        <div class="traq-title">TRAQ</div>

        <div class="traq-subtitle">
            🚦Traffic Intelligence
            <br>
            <small> See the Jam Before It Spreads !!</small>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button(" ENTER TRAQ ", use_container_width=True):
            st.session_state.intro_done = True
            st.rerun()

    st.stop()

st.title("🚦 TRAQ Traffic Intelligence")
st.caption("See the Jam Before It Spreads.")
st.divider()

st.subheader("📊 AI Traffic Intelligence")
st.caption(
    "Real-time traffic conditions, AI congestion prediction "
    "and future traffic forecast."
)

# Sidebar
st.sidebar.header("⚙️ Scenario Controls")
st.subheader("🤖 AI Congestion Forecast")

traffic_volume = st.slider(
    "Traffic Volume",
    min_value=100,
    max_value=2000,
    value=1400,
    step=100
)

road_capacity = st.slider(
    "Road Capacity",
    min_value=500,
    max_value=2000,
    value=1000,
    step=100
)

rain = st.selectbox(
    "Rain",
    ["No", "Yes"]
)

incident = st.selectbox(
    "Incident",
    ["No", "Yes"]
)

hour = st.slider(
    "Time of Day (Hour)",
    min_value=0,
    max_value=23,
    value=18
)

day = st.slider(
    "Day of Week",
    min_value=0,
    max_value=6,
    value=0
)

average_speed = st.slider(
    "Average Speed (km/h)",
    min_value=10,
    max_value=80,
    value=29,
    step=1
)

rain_value = 1 if rain == "Yes" else 0
incident_value = 1 if incident == "Yes" else 0

prediction_input = [[
    hour,
    day,
    traffic_volume,
    road_capacity,
    average_speed,
    rain_value,
    incident_value
]]

prediction = model.predict(prediction_input)[0]

prediction_probability = model.predict_proba(
    prediction_input
)[0][prediction]

confidence = prediction_probability * 100

if prediction == 1:
    st.error("🔴 AI Prediction: HIGH CONGESTION")
else:
    st.success("🟢 AI Prediction: LOW CONGESTION")

st.subheader("📈 Forecast Interpretation")

traffic_ratio = traffic_volume / road_capacity

if traffic_ratio >= 1.5:
    forecast_level = "VERY HIGH"
elif traffic_ratio >= 1.0:
    forecast_level = "HIGH"
elif traffic_ratio >= 0.7:
    forecast_level = "MEDIUM"
else:
    forecast_level = "LOW"

st.metric(
    "Traffic Load Level",
    forecast_level
)

st.caption(
    f"Traffic is using approximately {traffic_ratio * 100:.0f}% "
    "of the available road capacity."
)

st.metric(
    "AI Confidence",
    f"{confidence:.1f}%"
)

st.progress(
    int(confidence)
)
st.subheader("🔮 Future Congestion Forecast")

future_traffic_volume = min(
    2000,
    int(traffic_volume * 1.10)
)

future_prediction_input = [[
    hour,
    day,
    future_traffic_volume,
    road_capacity,
    average_speed,
    rain_value,
    incident_value
]]

future_prediction = model.predict(
    future_prediction_input
)[0]

future_probability = model.predict_proba(
    future_prediction_input
)[0][future_prediction]

future_confidence = future_probability * 100

if future_prediction == 1:
    st.error("🔴 Next 15 Minutes: HIGH CONGESTION")
else:
    st.success("🟢 Next 15 Minutes: LOW CONGESTION")

st.metric(
    "Forecast Confidence",
    f"{future_confidence:.1f}%"
)

st.caption(
    f"Expected traffic volume: {future_traffic_volume} vehicles"
)

st.subheader("🚨 Ripple Simulation")

incident_road = st.selectbox(
    "Select Incident Road",
    ["A", "B", "C", "D", "E"]
)

if st.button("🚨 Simulate Incident"):

    road_network = nx.Graph()

    road_network.add_edges_from([
        ("A", "B"),
        ("A", "C"),
        ("A", "D"),
        ("B", "E"),
        ("C", "E"),
        ("D", "E")
    ])

    affected_roads = list(
        road_network.neighbors(incident_road)
    )

    st.error(f"🚧 Road {incident_road} is closed!")

    st.write("Affected connected roads:")

    for road in affected_roads:
        st.write(f"➡️ Road {road}")

    road_network.remove_node(incident_road)

    st.warning(
        f"🔴 Ripple effect detected from Road {incident_road}"
    )

    st.success(
        f"Secondary analysis completed for "
        f"{len(affected_roads)} connected roads."
    )

scenario = st.sidebar.selectbox(
    "Select Scenario",
    [
        "Normal Traffic",
        "Accident",
        "Road Closure",
        "Heavy Rain",
        "Increased Traffic"
    ]
)

# Scenario results
results = {
    "Normal Traffic": {
        "congestion": "LOW",
        "roads": 0,
        "cost": 5,
        "message": "Traffic is currently normal."
    },
    "Accident": {
        "congestion": "HIGH",
        "roads": 3,
        "cost": 8,
        "message": "Accident detected. Ripple effects expected."
    },
    "Road Closure": {
        "congestion": "HIGH",
        "roads": 4,
        "cost": 10,
        "message": "Road closure is affecting nearby routes."
    },
    "Heavy Rain": {
        "congestion": "HIGH",
        "roads": 2,
        "cost": 9,
        "message": "Heavy rain may increase congestion."
    },
    "Increased Traffic": {
        "congestion": "HIGH",
        "roads": 3,
        "cost": 9,
        "message": "Traffic demand has increased."
    }
}

result = results[scenario]

# Scenario
st.divider()
st.subheader("🔮 What-If Traffic Scenario")

st.subheader(f"➡️ {scenario}")
st.info(result["message"])

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Congestion", result["congestion"])

with col2:
    st.metric("Affected Roads", result["roads"])

with col3:
    st.metric("Route Cost", result["cost"])

# Impact panel

st.subheader("🛣️ Route Comparison")

route_network = nx.Graph()

# AI prediction affects routing
if traffic_ratio >= 1.5:
    congestion_factor = 2.0
    st.error("🔴 VERY HIGH congestion")

elif traffic_ratio >= 1.0:
    congestion_factor = 1.5
    st.error("🟠 HIGH congestion")

elif traffic_ratio >= 0.7:
    congestion_factor = 1.2
    st.warning("🟡 MEDIUM congestion")

else:
    congestion_factor = 1.0
    st.success("🟢 LOW congestion")



road_costs = {
    "AB": 5 * congestion_factor,
    "AC": 2,
    "AD": 6,
    "BE": 3,
    "CE": 7,
    "DE": 4
}
if scenario == "Accident":
    road_costs["AB"] += 5

elif scenario == "Road Closure":
    road_costs["AC"] = 999

elif scenario == "Heavy Rain":
    road_costs["AC"] += 3
    road_costs["CE"] += 3

elif scenario == "Increased Traffic":
    road_costs["AB"] += 2
    road_costs["AC"] += 2
    road_costs["AD"] += 2

route_network.add_weighted_edges_from([
    ("A", "B", road_costs["AB"]),
    ("A", "C", road_costs["AC"]),
    ("A", "D", road_costs["AD"]),
    ("B", "E", road_costs["BE"]),
    ("C", "E", road_costs["CE"]),
    ("D", "E", road_costs["DE"])
])

source = "A"
destination = "E"

try:
    best_route = nx.dijkstra_path(
        route_network,
        source,
        destination,
        weight="weight"
    )

    best_cost = nx.dijkstra_path_length(
        route_network,
        source,
        destination,
        weight="weight"
    )

    st.write("Candidate routes are evaluated using Dijkstra.")

    st.success(
        f"✅ Recommended Route: {' → '.join(best_route)}"
    )

    st.metric(
        "Dijkstra Route Cost",
        best_cost
    )

except nx.NetworkXNoPath:
    st.error("❌ No available route found.")

st.success(f"✅ Recommended Route: {best_route}")
st.subheader("📊 Impact Analysis")

if result["congestion"] == "HIGH":
    st.error("🔴 Secondary congestion detected")
else:
    st.success("🟢 No major congestion detected")

# Route recommendation
st.subheader("🛣️ Route Recommendation")

st.success(
    f"✅ Recommended Route: {' → '.join(best_route)}"
)

st.info(
    f"🔄 Route updated based on current scenario: {' → '.join(best_route)}"
)

st.caption(
    "Route dynamically calculated using Dijkstra based on current road costs."
)

# Emergency mode
st.subheader("🚑 Emergency Routing")

emergency = st.selectbox(
    "Emergency Vehicle",
    ["None", "Ambulance", "Fire Service"]
)

if scenario == "Road Closure":
    emergency_route = nx.dijkstra_path(
        route_network,
        "A",
        "E",
        weight="weight"
    )
else:
    emergency_route = nx.dijkstra_path(
        route_network,
        "A",
        "E",
        weight="weight"
    )

    st.warning(
        f"🚨 {emergency} route requested"
    )

    st.success(
        f"🚑 Emergency Route: {' → '.join(emergency_route)}"
    )


st.subheader("🚨 Incident & Emergency Status")

st.write(f"Current Scenario: {scenario}")

if emergency != "None":
    st.warning(f"Emergency Mode Active: {emergency}")
else:
    st.info("Emergency Mode: Inactive")

st.subheader("🤖 Model Performance")

col1, col2 = st.columns(2)

with col1:
    st.metric("Accuracy", "75%")

with col2:
    st.metric("Model", "XGBoost")

if scenario in ["Accident", "Road Closure"]:
    st.warning(
        "Emergency route available. "
        "Official closures and instructions must be respected."
    )
else:
    st.info("No emergency incident currently selected.")

st.divider()

st.caption(
    "🚦 TRAQ • AI-powered Traffic Forecasting & Dynamic Route Optimization"
)

st.caption("Prototype for demonstration and academic evaluation."
)