FROM quay.io/thoth-station/s2i-lab-elyra:latest

USER root
COPY requirements.txt /requirements.txt
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm; \
    dnf install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm; \
    dnf install -y mesa-libGL ffmpeg-libs ffmpeg-devel; \
    pip install -r /requirements.txt
USER 1001
