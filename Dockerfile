FROM python:3
ADD giffetteria.py /
RUN pip install requests
RUN pip install python-telegram-bot
RUN pip install beautifulsoup4
RUN pip install telegram
CMD ["python", "./giffetteria.py"]
