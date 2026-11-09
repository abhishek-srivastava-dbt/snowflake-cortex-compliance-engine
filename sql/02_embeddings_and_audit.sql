-- =====================================================================
-- Day 2 & 3: Vector Storage, Arctic Embeddings & Llama-3.1 Policy Audit
-- =====================================================================
USE ROLE COMPLIANCE_AI_ADMIN;
USE WAREHOUSE CORTEX_WH;

-- 1. Raw Chunks Storage (Bronze/Silver Layer)
CREATE TABLE IF NOT EXISTS COMPLIANCE_INTEL_DB.RAW_DOCS.CONTRACT_CHUNKS (
    CHUNK_ID VARCHAR(36) DEFAULT UUID_STRING(),
    DOCUMENT_NAME VARCHAR(100),
    CATEGORY VARCHAR(50),
    CHUNK_INDEX INT,
    CHUNK_TEXT TEXT,
    CHUNK_EMBEDDING VECTOR(FLOAT, 768),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 2. In-Warehouse Vectorization via Arctic Embed
UPDATE COMPLIANCE_INTEL_DB.RAW_DOCS.CONTRACT_CHUNKS
SET CHUNK_EMBEDDING = SNOWFLAKE.CORTEX.AI_EMBED('snowflake-arctic-embed-m', CHUNK_TEXT)
WHERE CHUNK_EMBEDDING IS NULL;

-- 3. Gold Layer Structured Findings Ledger
CREATE TABLE IF NOT EXISTS COMPLIANCE_INTEL_DB.AUDIT_GOLD.COMPLIANCE_FINDINGS (
    FINDING_ID VARCHAR(36) DEFAULT UUID_STRING(),
    DOCUMENT_NAME VARCHAR(100),
    POLICY_RULE TEXT,
    SEVERITY VARCHAR(20),
    ANALYSIS_SUMMARY TEXT,
    IS_VIOLATION BOOLEAN,
    AUDITED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 4. Automated LLM Regulatory Audit Pipeline
INSERT INTO COMPLIANCE_INTEL_DB.AUDIT_GOLD.COMPLIANCE_FINDINGS 
    (DOCUMENT_NAME, POLICY_RULE, SEVERITY, ANALYSIS_SUMMARY, IS_VIOLATION)
SELECT 
    DOCUMENT_NAME,
    'Mandatory incident escalation requires critical Sev-1 incident acknowledgement within 10 minutes or less, and breach notification to controllers within 48 hours.' AS POLICY_RULE,
    'HIGH' AS SEVERITY,
    SNOWFLAKE.CORTEX.AI_COMPLETE(
        'llama3.1-70b', 
        CONCAT(
            'You are an enterprise compliance auditor. Evaluate this clause against the policy.\n',
            'Policy: Mandatory incident escalation requires critical Sev-1 incident acknowledgement within 10 minutes or less, and breach notification to controllers within 48 hours.\n',
            'Clause: ', CHUNK_TEXT, '\n',
            'State if there is a violation and why in 2 sentences.'
        )
    ) AS ANALYSIS_SUMMARY,
    TRUE AS IS_VIOLATION
FROM COMPLIANCE_INTEL_DB.RAW_DOCS.CONTRACT_CHUNKS
WHERE CATEGORY IN ('SLA', 'GDPR');