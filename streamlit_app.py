import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(
    page_title="House Price Predictor",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict"

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.hero-title {
    text-align: center;
    font-size: 52px;
    font-weight: 700;
    margin-bottom: 10px;
}

.hero-subtitle {
    text-align: center;
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 40px;
}

.section-title {
    font-size: 30px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 20px;
}

.feature-card {
    background-color: #f8f9fc;
    border-radius: 14px;
    padding: 18px;
    border: 1px solid #e5e7eb;
    margin-bottom: 16px;
}

.result-card {
    background-color: #f8fafc;
    border-radius: 16px;
    padding: 25px;
    border: 1px solid #e5e7eb;
}

.price-text {
    font-size: 42px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

FEATURE_INFO = {
    "MSSubClass": {
        "label": "Building Class",
        "description": "Represents house building type.",
        "range": "20 - 190",
        "example": 60
    },
    "LotFrontage": {
        "label": "Lot Frontage",
        "description": "Linear feet connected to street.",
        "range": "20 - 200",
        "example": 80
    },
    "LotArea": {
        "label": "Lot Area",
        "description": "Total land area of property.",
        "range": "1000 - 100000 sq ft",
        "example": 8500
    },
    "OverallQual": {
        "label": "Overall Quality",
        "description": "Material and finish quality.",
        "range": "1 - 10",
        "example": 7
    },
    "OverallCond": {
        "label": "Overall Condition",
        "description": "Overall house condition.",
        "range": "1 - 10",
        "example": 5
    },
    "YearBuilt": {
        "label": "Year Built",
        "description": "Year property was constructed.",
        "range": "1900 - 2025",
        "example": 2005
    },
}

all_features = [
    "MSSubClass", "LotFrontage", "LotArea",
    "OverallQual", "OverallCond", "YearBuilt",
    "YearRemodAdd", "MasVnrArea", "BsmtFinSF1",
    "BsmtFinSF2", "BsmtUnfSF", "TotalBsmtSF",
    "1stFlrSF", "2ndFlrSF", "LowQualFinSF",
    "GrLivArea", "BsmtFullBath", "BsmtHalfBath",
    "FullBath", "HalfBath", "BedroomAbvGr",
    "KitchenAbvGr", "TotRmsAbvGrd", "Fireplaces",
    "GarageYrBlt", "GarageCars", "GarageArea",
    "WoodDeckSF", "OpenPorchSF", "EnclosedPorch",
    "3SsnPorch", "ScreenPorch", "PoolArea",
    "MiscVal", "MoSold", "YrSold"
]

st.markdown(
    '<div class="hero-title">House Price Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Predict house prices using property characteristics and market estimation.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">'
    'Select Features for Predicting House Price'
    '</div>',
    unsafe_allow_html=True
)

search_term = st.text_input(
    "Search Property Features",
    placeholder="Example: Garage, Area, Year..."
)

filtered_features = [
    feature for feature in all_features
    if search_term.lower() in feature.lower()
]

selected_features = st.multiselect(
    "Choose Features",
    options=filtered_features if search_term else all_features,
    default=[
        "LotArea",
        "OverallQual",
        "YearBuilt"
    ]
)

input_data = {
    feature: 0
    for feature in all_features
}

for feature in selected_features:

    info = FEATURE_INFO.get(
        feature,
        {
            "label": feature,
            "description": "Property-related feature.",
            "range": "Varies",
            "example": 0
        }
    )

    st.markdown(
        '<div class="feature-card">',
        unsafe_allow_html=True
    )

    st.subheader(info["label"])

    st.write(info["description"])

    st.caption(
        f"Expected Range: {info['range']}"
    )

    st.caption(
        f"Example Value: {info['example']}"
    )

    input_data[feature] = st.number_input(
        f"Enter {info['label']}",
        value=int(info["example"]),
        step=1,
        format="%d"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

if st.button(
    "Predict House Price",
    use_container_width=True
):

    try:

        with st.spinner(
            "Analyzing property value..."
        ):

            response = requests.post(
                API_URL,
                json=input_data,
                timeout=20
            )

        if response.status_code == 200:

            predicted_price = response.json()[
                "predicted_price"
            ]

            st.markdown("---")

            st.markdown(
                '<div class="section-title">'
                'Prediction Result'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="result-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="price-text">'
                f'${predicted_price:,.2f}'
                f'</div>',
                unsafe_allow_html=True
            )

            if predicted_price < 150000:
                category = "Budget"
                reason = (
                    "Property falls in an affordable "
                    "market segment."
                )

            elif predicted_price < 300000:
                category = "Mid-Range"
                reason = (
                    "Balanced valuation based on "
                    "selected property features."
                )

            elif predicted_price < 600000:
                category = "Premium"
                reason = (
                    "Higher value due to stronger "
                    "property specifications."
                )

            else:
                category = "Luxury"
                reason = (
                    "Premium property with "
                    "high estimated market value."
                )

            st.success(
                f"Market Segment: {category}"
            )

            st.info(reason)

            market_ranges = {
                "Budget": 150000,
                "Mid-Range": 300000,
                "Premium": 600000,
                "Luxury": 900000
            }

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=list(
                        market_ranges.keys()
                    ),
                    y=list(
                        market_ranges.values()
                    ),
                    name="Market Range"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=[category],
                    y=[predicted_price],
                    mode="markers+text",
                    text=["Your Property"],
                    textposition="top center",
                    marker=dict(size=18),
                    name="Prediction"
                )
            )

            fig.update_layout(
                title="Market Position Analysis",
                xaxis_title="Market Category",
                yaxis_title="Price ($)",
                template="plotly_white",
                height=500
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        else:
            st.error(
                f"Backend Error: "
                f"{response.text}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to backend. "
            "Make sure FastAPI is running."
        )

    except Exception as error:
        st.error(
            f"Unexpected error: "
            f"{str(error)}"
        )