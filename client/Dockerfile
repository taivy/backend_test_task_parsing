FROM python:3.9
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .
