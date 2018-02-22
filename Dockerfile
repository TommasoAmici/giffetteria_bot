FROM python:3
ADD giffetteria.py /
RUN pip install -r requirements.txt
CMD ["python", "./giffetteria.py"]
