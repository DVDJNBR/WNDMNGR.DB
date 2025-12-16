-- PostgreSQL function to execute dynamic SQL
-- This must be created ONCE in Supabase SQL Editor before using the Edge Function

CREATE OR REPLACE FUNCTION exec_sql(sql text)
RETURNS json AS $$
DECLARE
  result json;
BEGIN
  -- Execute the SQL statement
  EXECUTE sql;

  -- Return success indicator
  RETURN json_build_object('success', true, 'message', 'SQL executed successfully');

EXCEPTION
  WHEN OTHERS THEN
    -- Return error details
    RETURN json_build_object(
      'success', false,
      'error', SQLERRM,
      'detail', SQLSTATE
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permission to authenticated users
GRANT EXECUTE ON FUNCTION exec_sql(text) TO authenticated;
GRANT EXECUTE ON FUNCTION exec_sql(text) TO service_role;
