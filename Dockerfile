FROM public.ecr.aws/lambda/python:3.8

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./requirements.2.txt ./requirements.2.txt
RUN pip install -r ./requirements.2.txt

COPY . ./

CMD ["app.main.handler"]