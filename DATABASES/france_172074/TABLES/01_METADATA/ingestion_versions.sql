-- =============================================
-- Table: ingestion_versions
-- Description: Tracks data ingestion versions and metadata
-- =============================================

CREATE TABLE ingestion_versions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    version_number INT NOT NULL,
    ingestion_date DATETIME NOT NULL DEFAULT GETDATE(),
    ingestion_source VARCHAR(100) NOT NULL, -- 'github-actions', 'manual', etc.
    triggered_by VARCHAR(255), -- GitHub username, local user, etc.
    commit_sha VARCHAR(40), -- Git commit SHA if applicable
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress', -- 'in_progress', 'completed', 'failed'
    tables_affected INT, -- Number of tables loaded
    total_rows_inserted INT, -- Total rows across all tables
    execution_time_seconds INT, -- Duration of ingestion

    -- Validation tests
    validation_passed BIT, -- Overall validation result
    test_silver_gold_reconciliation BIT, -- Silver to Gold row count match
    test_uuid_integrity BIT, -- All UUIDs are valid and unique
    test_foreign_keys BIT, -- All foreign key relationships valid
    test_required_fields BIT, -- All required fields populated
    validation_errors NVARCHAR(MAX), -- JSON array of validation errors

    error_message NVARCHAR(MAX), -- Error details if failed
    notes NVARCHAR(500), -- Optional notes
    CONSTRAINT UQ_ingestion_version UNIQUE (version_number)
);

-- Index for quick lookups
CREATE INDEX IX_ingestion_versions_date ON ingestion_versions(ingestion_date DESC);
CREATE INDEX IX_ingestion_versions_status ON ingestion_versions(status);
CREATE INDEX IX_ingestion_versions_validation ON ingestion_versions(validation_passed);

-- Add helpful comment
EXEC sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Tracks all data ingestion versions with metadata, validation results, and audit trail for rollback purposes',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE', @level1name = N'ingestion_versions';
