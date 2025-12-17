-- =============================================
-- Table: ingestion_versions
-- Description: Tracks data ingestion versions and metadata
-- =============================================

CREATE TABLE IF NOT EXISTS ingestion_versions (
    id SERIAL PRIMARY KEY,
    version_number INT NOT NULL,
    ingestion_date TIMESTAMP NOT NULL DEFAULT NOW(),
    ingestion_source VARCHAR(100) NOT NULL, -- 'github-actions', 'manual', etc.
    triggered_by VARCHAR(255), -- GitHub username, local user, etc.
    commit_sha VARCHAR(40), -- Git commit SHA if applicable
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress', -- 'in_progress', 'completed', 'failed'
    tables_affected INT, -- Number of tables loaded
    total_rows_inserted INT, -- Total rows across all tables
    execution_time_seconds INT, -- Duration of ingestion

    -- GOLD layer tracking
    gold_data_source_date DATE, -- Date from source file (e.g., 2025.12.09 from PDF)
    gold_generation_timestamp TIMESTAMP, -- When GOLD layer was generated
    gold_csv_count INT, -- Number of CSV files in GOLD layer

    -- Validation tests
    validation_passed BOOLEAN, -- Overall validation result
    test_silver_gold_reconciliation BOOLEAN, -- Silver to Gold row count match
    test_uuid_integrity BOOLEAN, -- All UUIDs are valid and unique
    test_foreign_keys BOOLEAN, -- All foreign key relationships valid
    test_required_fields BOOLEAN, -- All required fields populated
    validation_errors TEXT, -- JSON array of validation errors

    error_message TEXT, -- Error details if failed
    notes VARCHAR(500), -- Optional notes
    CONSTRAINT UQ_ingestion_version UNIQUE (version_number)
);

-- Index for quick lookups
CREATE INDEX IX_ingestion_versions_date ON ingestion_versions(ingestion_date DESC);
CREATE INDEX IX_ingestion_versions_status ON ingestion_versions(status);
CREATE INDEX IX_ingestion_versions_validation ON ingestion_versions(validation_passed);

-- Add helpful comment (PostgreSQL syntax)
COMMENT ON TABLE ingestion_versions IS 'Tracks all data ingestion versions with metadata, validation results, and audit trail for rollback purposes';