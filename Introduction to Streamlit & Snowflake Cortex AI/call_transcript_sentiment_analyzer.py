# streamlit_app.py

# Import python packages
import streamlit as st

# We can also use Snowpark for our analyses!
from snowflake.snowpark.context import get_active_session
session = get_active_session()

# --- Streamlit UI ---
st.title("Call Center Transcript Analyzer using Snowflake Cortex")


# --- Load data ---
trans = f"SELECT * FROM CALL_TRANSCRIPTS"
call_df = session.sql(trans).to_pandas()

# --- Agent filter ---
agents = call_df['AGENT_NAME'].unique()
selected_agent = st.selectbox("Select Agent", agents)
filtered_df = call_df[call_df['AGENT_NAME'] == selected_agent]

# --- Display data ---
st.subheader(f"Call Transcripts for Agent: {selected_agent}")
st.dataframe(filtered_df[['CALL_DATE', 'CUSTOMER_NAME', 'TRANSCRIPT']])

# --- Select call ---
selected_call = st.selectbox("Select a call to analyze", filtered_df['CALL_ID'])
selected_transcript = filtered_df[filtered_df['CALL_ID'] == selected_call]['TRANSCRIPT'].values[0]

# --- Run AI analysis with Snowflake Cortex ---
if st.button("Analyze with Cortex"):
    with st.spinner("Calling Cortex..."):

        # Sentiment Analysis
        query = f"""
        SELECT 
        SNOWFLAKE.CORTEX.SENTIMENT($${selected_transcript}$$) AS SENTIMENT
        """
        senti_result = session.sql(query).collect()
        sentiment = senti_result[0]['SENTIMENT']

        # Summarization
        summary_query = f"""
        SELECT 
        SNOWFLAKE.CORTEX.SUMMARIZE($${selected_transcript}$$) AS SUMMARY
        """
        summary_result = session.sql(summary_query).collect()
        summary = summary_result[0]['SUMMARY']

        # Define your categories
        categories = ["Billing", "Technical Support", "Account Access", "Product Feedback"]

        # Convert the list into a SQL array
        category_list = ",".join([f"'{cat}'" for cat in categories])
        sql_array = f"ARRAY_CONSTRUCT({category_list})"

        # Classification query
        classification_query = f"""
            SELECT 
                SNOWFLAKE.CORTEX.CLASSIFY_TEXT($${selected_transcript}$$, {sql_array}) AS CATEGORY
        """
        classification_result = session.sql(classification_query).collect()
        category = classification_result[0]['CATEGORY']

        # Display Results
        st.subheader("Cortex AI Output")
        st.write("**Sentiment:**", sentiment)
        st.write("**Summary:**",summary)
        st.write("**Classify Text:**",category)
        
        st.success('This is a success message!', icon="✅")
