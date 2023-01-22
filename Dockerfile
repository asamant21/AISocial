FROM python:3

ADD be_requirements.txt /
ADD main.py /
ADD app/ /app

RUN pip install -r be_requirements.txt
ENV SUPABASE_URL https://qcmbuvytqonaseejrbmw.supabase.co
ENV SUPABASE_KEY eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFjbWJ1dnl0cW9uYXNlZWpyYm13Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzQzMzU1MzIsImV4cCI6MTk4OTkxMTUzMn0.p8JkrDOGSsEzEdcxEHicHXchpxC_ZGZgMvH40JS1ERw
CMD [ "python", "main.py" ]
