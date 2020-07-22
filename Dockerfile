FROM python:3.7.8-stretch
COPY ./discord /opt/discord
WORKDIR /opt/discord
RUN pip3 install -r requirements/requirements.txt
CMD [ "python3", "bastion.py" ]
