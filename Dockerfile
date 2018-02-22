FROM python:3
ADD giffetteria.py /
CMD ["/usr/bin/pip", "install", "-r", "./requirements.txt"]
CMD ["python", "./giffetteria.py"]
