FROM python:3.9-slim

WORKDIR /root

COPY ./webapp /root

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /root/requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]