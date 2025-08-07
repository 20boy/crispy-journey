FROM python:3.13
LABEL authors="KOYE"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]


#ENTRYPOINT ["top", "-b"]