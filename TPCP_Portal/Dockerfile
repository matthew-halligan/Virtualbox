FROM python:3.8.10

WORKDIR /app


COPY app.py /app
ADD templates /app/templates
COPY requirements.txt /app
COPY gtirb.sh /app

RUN pip3 install --trusted-host pypi.org \
              --trusted-host files.pythonhosted.org -r requirements.txt
              
RUN apt-get install curl && apt-get install ping

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
