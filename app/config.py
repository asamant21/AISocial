""""""
import os

from supabase import Client, create_client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

second_url = "https://apxmldjogrvjvfzaouyl.supabase.co"
second_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFweG1sZGpvZ3J2anZmemFvdXlsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY3OTc4NzEyMSwiZXhwIjoxOTk1MzYzMTIxfQ.897wIUqcjkpsOpd6NF-orMhmnyo7-Nj8zVq7VfG08yg"
second_client: Client = create_client(second_url, second_key)
