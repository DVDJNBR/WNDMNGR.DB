// Edge Function to execute SQL files from Storage
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!
    const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!

    // Create Supabase client with service role key
    const supabase = createClient(supabaseUrl, supabaseServiceKey, {
      auth: {
        persistSession: false,
        autoRefreshToken: false,
      }
    })

    // Get SQL file path from request
    const { filePath } = await req.json()

    if (!filePath) {
      return new Response(
        JSON.stringify({ error: 'filePath is required' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    console.log(`[1] Downloading SQL file: ${filePath}`)

    // Download SQL file from Storage
    const { data: fileData, error: downloadError } = await supabase
      .storage
      .from('sql-scripts')
      .download(filePath)

    if (downloadError) {
      console.error('Download error:', downloadError)
      return new Response(
        JSON.stringify({ error: `Failed to download file: ${downloadError.message}` }),
        { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    const sqlContent = await fileData.text()
    console.log(`[2] Downloaded ${sqlContent.length} characters`)

    // Parse SQL into individual statements
    // Remove comments and split by semicolon
    const statements = sqlContent
      .split('\n')
      .filter(line => !line.trim().startsWith('--'))  // Remove SQL comments
      .join('\n')
      .split(';')
      .map(stmt => stmt.trim())
      .filter(stmt => stmt.length > 0)

    console.log(`[3] Parsed ${statements.length} SQL statements`)

    const results = []

    // Execute each statement
    for (let i = 0; i < statements.length; i++) {
      const stmt = statements[i]
      console.log(`[4.${i + 1}] Executing statement ${i + 1}/${statements.length}`)
      console.log(`    Preview: ${stmt.substring(0, 100)}...`)

      try {
        // Execute SQL using Supabase client
        // For DDL statements (CREATE TABLE, etc.), we use rpc to a custom function
        // Or we can use the postgres connection directly
        const { data, error } = await supabase.rpc('exec_sql', { sql: stmt })

        if (error) {
          // If exec_sql function doesn't exist, we'll need to execute differently
          // For now, log the error and continue
          console.error(`    Error executing statement ${i + 1}:`, error)
          results.push({
            statement: i + 1,
            preview: stmt.substring(0, 100),
            success: false,
            error: error.message
          })
        } else {
          console.log(`    ✓ Statement ${i + 1} executed successfully`)
          results.push({
            statement: i + 1,
            preview: stmt.substring(0, 100),
            success: true,
            data
          })
        }
      } catch (err) {
        console.error(`    Exception executing statement ${i + 1}:`, err)
        results.push({
          statement: i + 1,
          preview: stmt.substring(0, 100),
          success: false,
          error: err.message
        })
      }
    }

    const successCount = results.filter(r => r.success).length
    const failCount = results.filter(r => !r.success).length

    console.log(`[5] Execution complete: ${successCount} success, ${failCount} failed`)

    return new Response(
      JSON.stringify({
        success: failCount === 0,
        filePath,
        totalStatements: statements.length,
        successCount,
        failCount,
        results
      }),
      {
        status: failCount === 0 ? 200 : 207,  // 207 = Multi-Status
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    )

  } catch (error) {
    console.error('Unexpected error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
