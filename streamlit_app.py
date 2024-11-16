import streamlit as st
import pandas as pd
import numpy as np
import joblib

scaler = joblib.load("scaler.pkl")
model = joblib.load("model.pkl")


def predict(inputs):
    defaults = {
        "launchYear": 2024,
        "batteryCapacity": 4000,
        "removableBattery": "Unknown",
        "refreshRate": 60,
        "screenSize": 6.0,
        "ram": 6,
        "internalStorage": 64,
        "expandableStorage": "Unknown",
        "nfc": "Unknown",
        "backCam1": 0,
        "backCam2": 0,
        "backCam3": 0,
        "backCam4": 0,
        "backCam5": 0,
        "totalBackCameras": 0,
        "frontCam1": 0,
        "frontCam2": 0,
        "totalFrontCameras": 0,
        "primarySimNetwork": "Unknown",
        "secondarySimNetwork": "Unknown",
    }

    for key, defaultValue in defaults.items():
        if key not in inputs or not inputs[key]:
            inputs[key] = defaultValue

    inputDf = pd.DataFrame(
        [inputs],
        columns=[
            "General_Release date",
            "General_Battery capacity (mAh)",
            "General_Removable battery",
            "Display_Refresh Rate",
            "Display_Screen size (inches)",
            "Hardware_RAM",
            "Hardware_Internal storage",
            "Hardware_Expandable storage",
            "Connectivity_NFC",
            "camera_1_megapixel",
            "camera_2_megapixel",
            "camera_3_megapixel",
            "camera_4_megapixel",
            "camera_5_megapixel",
            "num_cameras",
            "front_camera_1_megapixel",
            "front_camera_2_megapixel",
            "num_front_cameras",
            "Network_SIM_1",
            "Network_SIM_2",
            "General_Price in India",
        ],
    )

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
        "launchYear": launchYear,
        "batteryCapacity": batteryCapacity,
        "removableBattery": removableBattery,
        "refreshRate": refreshRate,
        "screenSize": screenSize,
        "ram": ram,
        "internalStorage": internalStorage,
        "expandableStorage": expandableStorage,
        "nfc": nfc,
        "backCam1": backCam1,
        "backCam2": backCam2,
        "backCam3": backCam3,
        "backCam4": backCam4,
        "backCam5": backCam5,
        "totalBackCameras": totalBackCameras,
        "frontCam1": frontCam1,
        "frontCam2": frontCam2,
        "totalFrontCameras": totalFrontCameras,
        "primarySimNetwork": primarySimNetwork,
        "secondarySimNetwork": secondarySimNetwork,
    }
    price = predict(inputs)
    st.success(f"Predicted Price: ₹{price}")
