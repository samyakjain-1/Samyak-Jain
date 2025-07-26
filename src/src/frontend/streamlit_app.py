import streamlit as st
import requests
import json

# Backend API URL
API_URL = "http://localhost:8080/process"

st.set_page_config(page_title="MarketAI", layout="wide")

st.title("🤖 MarketAI: Agentic Financial Analysis")
st.markdown("Enter a financial hypothesis below and let the AI agents analyze it for you.")

# User input
hypothesis_input = st.text_input(
    "Enter your hypothesis:",
    "e.g., Apple will reach $250 by the end of 2025"
)

if st.button("Analyze Hypothesis"):
    if hypothesis_input:
        with st.spinner("The AI agents are analyzing your hypothesis... This may take a moment."):
            try:
                payload = {"hypothesis": hypothesis_input}
                response = requests.post(API_URL, json=payload, timeout=300)

                if response.status_code == 200:
                    st.success("Analysis complete!")
                    result = response.json()

                    # Display the results
                    st.subheader("Analysis Report")
                    st.metric("Confidence Score", f"{result.get('confidence_score', 0.0) * 100:.1f}%", help="A score from 0.15 to 0.85 representing the AI's confidence.")
                    
                    st.write("**Recommendation:**")
                    st.info(result.get("recommendation", "No recommendation provided."))

                    st.write("**Executive Summary:**")
                    st.write(result.get("summary", "No summary provided."))

                    # Display Confirmations and Contradictions
                    st.subheader("Evidence Breakdown")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("✅ **Confirmations (Supporting Evidence)**")
                        for item in result.get("confirmations", []):
                            with st.expander(f"**{item.get('quote')}**"):
                                st.markdown(f"**Reason:** {item.get('reason')}")
                                st.markdown(f"**Source:** {item.get('source')}")
                                st.markdown(f"**Strength:** {item.get('strength')}")

                    with col2:
                        st.write("❌ **Contradictions (Risks & Headwinds)**")
                        for item in result.get("contradictions", []):
                            with st.expander(f"**{item.get('quote')}**"):
                                st.markdown(f"**Reason:** {item.get('reason')}")
                                st.markdown(f"**Source:** {item.get('source')}")
                                st.markdown(f"**Strength:** {item.get('strength')}")

                    # Since the API returns the report, not the alerts, we can't display them here yet.
                    # This would require a new API endpoint to fetch alerts for a given report ID.
                    # For now, we will just show the main report.
                    
                    st.write("**Raw Report Data:**")
                    st.json(result)

                else:
                    st.error(f"Error from API: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend API: {e}")
    else:
        st.warning("Please enter a hypothesis to analyze.")
