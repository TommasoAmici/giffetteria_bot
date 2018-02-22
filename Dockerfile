FROM python:3
ADD giffetteria.py /
RUN pip3 install requests
RUN pip3 install python-telegram-bot
RUN pip3 install beautifulsoup4
RUN pip3 install telegram
CMD ["python3", "./giffetteria.py"]
