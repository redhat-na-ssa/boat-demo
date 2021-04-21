FROM quay.io/thoth-station/s2i-lab-elyra:latest

USER root
COPY requirements.txt /requirements.txt
RUN dnf install -y mesa-libGL; pip install -r /requirements.txt
USER 1001
