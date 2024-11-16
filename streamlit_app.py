import streamlit as st
import pandas as pd
import numpy as np
import joblib

scaler = joblib.load("scaler.pkl")
model = joblib.load("model.pkl")


def predict(inputs):
    defaults = {
        "General_Release date": 2024,
        "General_Battery capacity (mAh)": 4000,
        "General_Removable battery": "Unknown",
        "Display_Refresh Rate": 60,
        "Display_Screen size (inches)": 6.0,
        "Hardware_RAM": 6,
        "Hardware_Internal storage": 64,
        "Hardware_Expandable storage": "Unknown",
        "Connectivity_NFC": "Unknown",
        "camera_1_megapixel": 0,
        "camera_2_megapixel": 0,
        "camera_3_megapixel": 0,
        "camera_4_megapixel": 0,
        "camera_5_megapixel": 0,
        "num_cameras": 0,
        "front_camera_1_megapixel": 0,
        "front_camera_2_megapixel": 0,
        "num_front_cameras": 0,
        "Network_SIM_1": "Unknown",
        "Network_SIM_2": "Unknown",
    }

    for key, defaultValue in defaults.items():
        if key not in inputs or not inputs[key]:
            inputs[key] = defaultValue

    inputDf = pd.DataFrame(
        [inputs],
    )

    print(inputDf)

    trainColumns = [
        "General_Release date",
        "General_Battery capacity (mAh)",
        "Display_Refresh Rate",
        "Display_Screen size (inches)",
        "Hardware_RAM",
        "Hardware_Internal storage",
        "camera_1_megapixel",
        "camera_2_megapixel",
        "camera_3_megapixel",
        "camera_4_megapixel",
        "camera_5_megapixel",
        "num_cameras",
        "front_camera_1_megapixel",
        "front_camera_2_megapixel",
        "num_front_cameras",
        "General_Removable battery_Unknown",
        "General_Removable battery_Yes",
        "Hardware_Expandable storage_Unknown",
        "Hardware_Expandable storage_Yes",
        "Connectivity_NFC_Unknown",
        "Connectivity_NFC_Yes",
        "Network_SIM_1_4G",
        "Network_SIM_1_5G",
        "Network_SIM_1_Unknown",
        "Network_SIM_2_4G",
        "Network_SIM_2_5G",
        "Network_SIM_2_Unknown",
    ]

    inputEncoded = pd.get_dummies(inputDf, drop_first=True)
    inputAligned = inputEncoded.reindex(columns=trainColumns, fill_value=0)
    inputScaled = scaler.transform(inputAligned)
    predictedPrice = model.predict(inputScaled)
    return int(predictedPrice[0])


st.title("Mobile Phone Price Predictor")

launchYear = st.selectbox(
    "Launch Year",
    ["Select"] + list(range(2008, 2025)),
)
batteryCapacity = st.number_input(
    "Battery Capacity (mAh)", min_value=0, value=None, step=100
)
removableBattery = st.selectbox("Removable Battery", ["Select", "Yes", "No", "Unknown"])
refreshRate = st.number_input("Refresh Rate (Hz)", min_value=0, value=None, step=10)
screenSize = st.number_input(
    "Screen Size (inches)", min_value=0.0, value=None, step=0.1
)
ram = st.number_input("RAM (GB)", min_value=0, value=None, step=1)
internalStorage = st.number_input(
    "Internal Storage (GB)", min_value=0, value=None, step=1
)
expandableStorage = st.selectbox(
    "Expandable Storage", ["Select", "Yes", "No", "Unknown"]
)
nfc = st.selectbox("NFC", ["Select", "Yes", "No", "Unknown"])

backCam1, backCam2, backCam3, backCam4, backCam5 = [
    st.number_input(
        f"Back Camera {i+1} Resolution (MP)", min_value=0.0, value=None, step=0.1
    )
    for i in range(5)
]
totalBackCameras = st.number_input(
    "Total Back Cameras", min_value=0, value=None, step=1
)

frontCam1, frontCam2 = [
    st.number_input(
        f"Front Camera {i+1} Resolution (MP)", min_value=0.0, value=None, step=0.1
    )
    for i in range(2)
]
totalFrontCameras = st.number_input(
    "Total Front Cameras", min_value=0, value=None, step=1
)

primarySimNetwork = st.selectbox(
    "Primary SIM Network", ["Select", "3G", "4G", "5G", "Unknown"]
)
secondarySimNetwork = st.selectbox(
    "Secondary SIM Network", ["Select", "3G", "4G", "5G", "Unknown"]
)

if st.button("Predict Price"):
    inputs = {
        "General_Release date": launchYear,
        "General_Battery capacity (mAh)": batteryCapacity,
        "General_Removable battery": removableBattery,
        "Display_Refresh Rate": refreshRate,
        "Display_Screen size (inches)": screenSize,
        "Hardware_RAM": ram,
        "Hardware_Internal storage": internalStorage,
        "Hardware_Expandable storage": expandableStorage,
        "Connectivity_NFC": nfc,
        "camera_1_megapixel": backCam1,
        "camera_2_megapixel": backCam2,
        "camera_3_megapixel": backCam3,
        "camera_4_megapixel": backCam4,
        "camera_5_megapixel": backCam5,
        "num_cameras": totalBackCameras,
        "front_camera_1_megapixel": frontCam1,
        "front_camera_2_megapixel": frontCam2,
        "num_front_cameras": totalFrontCameras,
        "Network_SIM_1": primarySimNetwork,
        "Network_SIM_2": secondarySimNetwork,
    }
    price = predict(inputs)
    st.success(f"Predicted Price: ₹{price}")
