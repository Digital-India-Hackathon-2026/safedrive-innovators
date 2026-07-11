import streamlit as st
import os
import time

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="Safe Drive Innovators",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Safe Drive Innovators")
st.subheader("Alcohol Detection System Before Vehicle Start")

st.markdown("""
### Application Flow
1️⃣ Face Capture  
2️⃣ Breath Test  
3️⃣ Alcohol Detection Result  
4️⃣ Vehicle Decision
""")

# ----------------------------------
# Session State
# ----------------------------------
if "face_captured" not in st.session_state:
    st.session_state.face_captured = False

if "breath_completed" not in st.session_state:
    st.session_state.breath_completed = False

if "result_generated" not in st.session_state:
    st.session_state.result_generated = False

if "selected_sample" not in st.session_state:
    st.session_state.selected_sample = None


# ==================================
# STEP 1 : FACE CAPTURE
# ==================================
st.header("📷 Step 1: Driver Face Capture")

camera_image = st.camera_input("Capture Driver Face")

if camera_image is not None:
    st.session_state.face_captured = True
    st.success("✅ Driver Face Captured")
    st.info("👤 Driver identity stored temporarily.")

st.divider()


# ==================================
# STEP 2 : BREATH TEST
# ==================================
st.header("💨 Step 2: Breath Test")

if not st.session_state.face_captured:
    st.warning("⚠ Please capture the driver's face before proceeding.")
else:
    st.success("✅ Driver verified successfully.")

    sample = st.radio(
        "Select Demo Breath Sample",
        (
            "Safe Drive Sample",
            "Alcohol Detected Sample"
        )
    )

    # Assign audio file
    if sample == "Safe Drive Sample":
        audio_file = "audio/safe_drive.wav"
    else:
        audio_file = "audio/alcohol.wav"

    # Play selected audio
    if os.path.exists(audio_file):
        st.audio(audio_file)
    else:
        st.warning(f"Audio file not found: {audio_file}")

    # Blow Test Button
    if st.button("💨 Blow Test"):
        st.info("💨 Please blow into the sensor...")

        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.02)
            progress.progress(i + 1)

        st.success("✅ Breath sample captured successfully.")
        st.success("👤 Breath sample matched with captured driver.")

        st.session_state.breath_completed = True
        st.session_state.selected_sample = sample

st.divider()


# ==================================
# STEP 3 : ALCOHOL DETECTION
# ==================================
st.header("🍺 Step 3: Alcohol Detection")

if not st.session_state.face_captured:
    st.warning("⚠ Face capture required first.")

elif not st.session_state.breath_completed:
    st.warning("⚠ Complete the breath test first.")

else:
    if st.button("🔍 Detect Alcohol"):

        with st.spinner("Analyzing breath sample..."):
            time.sleep(2)

        st.session_state.result_generated = True

        if st.session_state.selected_sample == "Alcohol Detected Sample":
            st.error("🍺 Alcohol Detected")
        else:
            st.success("✅ No Alcohol Detected")

st.divider()


# ==================================
# STEP 4 : VEHICLE DECISION
# ==================================
st.header("🚘 Step 4: Vehicle Decision")

if not st.session_state.result_generated:
    st.info("Waiting for alcohol detection result...")

else:
    if st.session_state.selected_sample == "Alcohol Detected Sample":
        st.error("❌ Do NOT Start Vehicle")
        st.error("🔒 Vehicle Ignition Locked")
    else:
        st.success("✅ Safe to Drive")
        st.success("🔓 Vehicle Start Allowed")