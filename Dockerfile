FROM makinacorpus/geodjango:focal-3.9

WORKDIR /app

COPY requirements.pip /app/

RUN pip3 install -r requirements.pip

COPY mozio /app/mozio
COPY manage.py /app/
COPY wait-for-it.sh .
COPY start.sh .

CMD python3.9 manage.py migrate && python3.9 manage.py runserver
