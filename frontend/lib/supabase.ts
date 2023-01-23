import { createClient } from '@supabase/supabase-js'

const PROJECT_URL = 'https://qcmbuvytqonaseejrbmw.supabase.co';
const CLIENT_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFjbWJ1dnl0cW9uYXNlZWpyYm13Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzQzMzU1MzIsImV4cCI6MTk4OTkxMTUzMn0.p8JkrDOGSsEzEdcxEHicHXchpxC_ZGZgMvH40JS1ERw'

// Create a single supabase client for interacting with your database
export const client = createClient(PROJECT_URL, CLIENT_ANON_KEY)
