FROM python:3.7.8-stretch
COPY ./discord /opt/discord
USE /opt/discord
RUN pip3 install -r requirements/requirements.txt
cmd [ "python3", "bastion.py" ]
