FROM public.ecr.aws/lambda/python:3.9

# ติดตั้ง boto3 เผื่อไว้ (แม้ AWS จะมีให้ แต่ทำแบบนี้จะคุม Version ได้ชัวร์กว่า)
RUN pip install boto3

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.lambda_handler" ]