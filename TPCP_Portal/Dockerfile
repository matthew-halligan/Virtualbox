FROM python:3.8.10

WORKDIR /app


COPY app.py /app
COPY api_methods.py /app
COPY client.py /app
COPY global_items.py /app
COPY requirements.txt /app

ADD templates /app/templates
ADD static /app/static


RUN pip3 install --trusted-host pypi.org \
              --trusted-host files.pythonhosted.org -r requirements.txt
              

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
