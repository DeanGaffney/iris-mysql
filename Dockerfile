FROM python:2.7-alpine

WORKDIR /usr/src/app

COPY conf.json ./

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./iris-mysql.py"]