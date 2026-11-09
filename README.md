\# 🛡️ Enterprise Compliance Intelligence Engine (Snowflake Cortex AI)



An end-to-end, zero-egress regulatory compliance intelligence platform built natively inside Snowflake. This engine leverages Snowflake Cortex Vector Search (`snowflake-arctic-embed-m`) and serverless LLM reasoning (`llama3.1-70b`) to automate SLA and regulatory audit enforcement across enterprise vendor contracts.



\## 📌 Architecture Highlights

\- \*\*Zero Data Egress:\*\* All vector embeddings (`AI\_EMBED`), cosine similarity ranking, and LLM evaluations (`AI\_COMPLETE`) execute strictly within Snowflake's trust perimeter—eliminating external third-party API exposure.

\- \*\*FinOps \& Resource Governance:\*\* Configured a dedicated Snowflake Resource Monitor (`CORTEX\_DEV\_MONITOR`) with a monthly 5-credit quota and automated hard suspension triggers at 100% to guarantee cost predictability.

\- \*\*Medallion Schema Design:\*\* Isolates raw ingested clauses (`RAW\_DOCS`) from immutable compliance violation logs (`AUDIT\_GOLD`) under least-privilege RBAC (`COMPLIANCE\_AI\_ADMIN`).

\- \*\*Autonomous CLI Orchestration:\*\* Automated database provisioning and vector search execution via the Snowflake Cortex Code CLI (CoCo) agent framework.

\- \*\*Native User Interface:\*\* Streamlit in Snowflake front-end providing risk officers with executive metrics, semantic retrieval, and on-demand LLM audit tools.



\## 🛠️ Tech Stack

\- \*\*Data Platform:\*\* Snowflake (Medallion Architecture)

\- \*\*AI Functions:\*\* `AI\_EMBED`, `VECTOR\_COSINE\_SIMILARITY`, `AI\_COMPLETE`

\- \*\*Models:\*\* `snowflake-arctic-embed-m` (768-dim), `llama3.1-70b`

\- \*\*UI \& Analytics:\*\* Streamlit in Snowflake, Snowpark Python

\- \*\*Orchestration Tooling:\*\* Snowflake Cortex Code CLI



\## 📂 Repository Structure

```text

snowflake-cortex-compliance-engine/

├── README.md                      # Architecture overview and documentation

├── sql/

│   ├── 01\_governance\_and\_schema.sql  # RBAC, schemas, and resource monitors

│   └── 02\_embeddings\_and\_audit.sql   # Vector storage and LLM audit engine

├── streamlit/

│   └── streamlit\_app.py           # Native Streamlit dashboard application

└── assets/                        # Screenshots and architecture diagrams

