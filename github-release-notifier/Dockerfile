FROM python:3.9-slim

ENV HOME=/app

WORKDIR $HOME
ADD requirements.txt $HOME/

RUN pip install --no-cache-dir -r requirements.txt

ADD github_release_notifier.py $HOME/

CMD [ "python3" , "/app/github_release_notifier.py" ]