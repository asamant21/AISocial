FROM python:3.9

ADD requirements.txt /
ADD main.py /
ADD app/ /app

RUN pip install -r requirements.txt
ENV OPENAI_API_KEY key
ENV SUPABASE_URL url
ENV SUPABASE_KEY another_key
CMD [ "python", "main.py" ]