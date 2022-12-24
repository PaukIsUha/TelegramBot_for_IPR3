FROM python:3.10-slim

WORKDIR /home/igor/HSE/Python/HW4/app

COPY ./app .

RUN pip install -r requirements.txt

EXPOSE 8888 

CMD ["python", "AsyncBot.py"] 
