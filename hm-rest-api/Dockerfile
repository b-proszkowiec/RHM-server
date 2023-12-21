FROM python:3.7-alpine

WORKDIR /app

COPY src .
RUN pip install --root-user-action=ignore -r requirements.txt

CMD ["python", "rhm_controller.py"]