-- In the 2025_02 Bundle, which is expected to be enabled by default the week of May 4, 2025 in release 9.12 (dates subject to change), Snowflake announced BCR-1924, which introduced user-based access control (UBAC). UBAC simplifies user collaboration in Snowflake securable objects such as Streamlit applications.

-- UBAC allows object owners to grant privileges directly to users, streamlining the sharing process and eliminating the need to create or modify roles for every sharing scenario. This is particularly beneficial for sharing limited-audience and under-development assets with specific colleagues.  

-- What is changing?
-- With UBAC, principals with the permission to grant privileges, will be able to grant privileges directly to users. For example: 

GRANT USAGE ON STREAMLIT streamlit_db.streamlit_schema.streamlit_app TO USER bob;

-- We understand that this new access control model may affect your governance practices. If you need to disable UBAC in your account after Bundle 2025_02 becomes enabled by default, set the account parameter DISABLE_USER_PRIVILEGE_GRANTS = TRUE 

ALTER ACCOUNT <name> SET DISABLE_USER_PRIVILEGE_GRANTS = TRUE


-- more information, read the User-based access control private preview documentation. This preview topic provides use-case scenarios, FAQs that answer common questions, and further guidance, including;  when to use RBAC vs. UBAC, how to monitor UBAC usage, and best practices for integrating UBAC into your existing governance processes. 

-- https://docs.snowflake.com/LIMITEDACCESS/ubac-overview?mkt_tok=MjUyLVJGTy0yMjcAAAGaK45ETlV_gHrlsIkYR0GA4APYne_Y8BVNdSl6Xkzensk-gCrKOZHzslQaJR5DehiEwo0UNeDz8NKJA_xgoLQBec26i-LkKb8xgUIkyjPBJ8iO2FAizA

GRANT USAGE ON STREAMLIT streamlit_db.streamlit_schema.streamlit_app TO USER USER_DESIGNER;


CREATE OR REPLACE DATABASE STREAMLIT_DB;
CREATE OR REPLACE SCHEMA STREAMLIT_SCHEMA;

CREATE OR REPLACE TABLE CALL_TRANSCRIPTS (
  CALL_ID STRING,
  AGENT_NAME STRING,
  CUSTOMER_NAME STRING,
  CALL_DATE DATE,
  TRANSCRIPT TEXT
);

SELECT * FROM CALL_TRANSCRIPTS LIMIT 30;
