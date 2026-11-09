import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd

# Page setup
st.set_page_config(layout="wide", page_title="Compliance Intelligence Engine")
session = get_active_session()

st.title("🛡️ Enterprise Compliance Intelligence Engine")
st.caption("Zero-egress LLM contract auditing & vector similarity search powered by Snowflake Cortex AI")

tab1, tab2, tab3 = st.tabs(["📊 Executive Audit Dashboard", "🔍 Semantic Clause Search", "⚡ On-Demand Policy Audit"])

# TAB 1: EXECUTIVE AUDIT DASHBOARD
with tab1:
    st.subheader("Audited Policy Violations (Gold Layer)")
    
    findings_df = session.sql("""
        SELECT 
            DOCUMENT_NAME,
            SEVERITY,
            IS_VIOLATION,
            ANALYSIS_SUMMARY,
            AUDITED_AT
        FROM COMPLIANCE_INTEL_DB.AUDIT_GOLD.COMPLIANCE_FINDINGS
        ORDER BY AUDITED_AT DESC
    """).to_pandas()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Findings", len(findings_df))
    col2.metric("Violations Flagged", int(findings_df["IS_VIOLATION"].sum()) if not findings_df.empty else 0)
    col3.metric("High Severity", len(findings_df[findings_df["SEVERITY"] == "HIGH"]) if not findings_df.empty else 0)
    
    st.dataframe(findings_df, width="stretch")

# TAB 2: SEMANTIC CLAUSE SEARCH
with tab2:
    st.subheader("Query Contract Repository via Vector Cosine Similarity")
    query_text = st.text_input(
        "Search compliance question / topic:",
        "What is the required deadline to report a personal data breach?"
    )
    top_k = st.slider("Top results to retrieve:", min_value=1, max_value=5, value=2)
    
    if st.button("Run Semantic Search", type="primary"):
        search_query = f"""
            SELECT 
                DOCUMENT_NAME,
                CATEGORY,
                ROUND(VECTOR_COSINE_SIMILARITY(
                    CHUNK_EMBEDDING, 
                    AI_EMBED('snowflake-arctic-embed-m', '{query_text}')
                ), 4) AS SIMILARITY_SCORE,
                CHUNK_TEXT
            FROM COMPLIANCE_INTEL_DB.RAW_DOCS.CONTRACT_CHUNKS
            ORDER BY SIMILARITY_SCORE DESC
            LIMIT {top_k}
        """
        results_df = session.sql(search_query).to_pandas()
        for idx, row in results_df.iterrows():
            with st.expander(f"[{row['CATEGORY']}] {row['DOCUMENT_NAME']} — Similarity: {row['SIMILARITY_SCORE']}"):
                st.write(row['CHUNK_TEXT'])

# TAB 3: ON-DEMAND POLICY AUDIT
with tab3:
    st.subheader("Ad-Hoc Regulatory Audit via Cortex LLM")
    policy_input = st.text_area(
        "Policy Rule to Audit Against:",
        "Critical Severity 1 incidents must be acknowledged within 10 minutes or less."
    )
    
    if st.button("Execute LLM Audit", type="secondary"):
        with st.spinner("Analyzing contract chunks via llama3.1-70b..."):
            audit_sql = f"""
                SELECT 
                    DOCUMENT_NAME,
                    CATEGORY,
                    AI_COMPLETE(
                        'llama3.1-70b',
                        CONCAT(
                            'You are an enterprise compliance auditor. Evaluate this clause against the policy.\\n',
                            'Policy: {policy_input}\\n',
                            'Clause: ', CHUNK_TEXT, '\\n',
                            'Respond in 2 sentences stating if there is a violation and why.'
                        )
                    ) AS AUDIT_VERDICT
                FROM COMPLIANCE_INTEL_DB.RAW_DOCS.CONTRACT_CHUNKS
                WHERE CATEGORY = 'SLA'
                LIMIT 1
            """
            audit_res = session.sql(audit_sql).to_pandas()
            for _, r in audit_res.iterrows():
                st.markdown(f"**Document:** {r['DOCUMENT_NAME']}")
                st.info(r['AUDIT_VERDICT'])