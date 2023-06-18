FROM python:3.9-slim-bullseye

ARG USERNAME=rtorrent
ARG USER_UID=1043
ARG USER_GID=100

# Create the user
RUN useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Install SSH client and LFTP
RUN apt-get update && apt-get install -y openssh-client lftp
RUN apt clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY torrentdl_service.py .
RUN chown -R $USER_UID:$USER_GID /app

USER $USERNAME

CMD ["python", "torrentdl_service.py"]
