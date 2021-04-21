FROM quay.io/thoth-station/s2i-lab-elyra:latest

USER root
RUN mkdir -p /run/secrets/etc-pki-entitlement-host
RUN ls -la /etc/pki/entitlement-host/
COPY requirements.txt /requirements.txt
COPY /etc/pki/entitlement/* /etc/pki/entitlement-host/
# COPY /etc/rhsm/* /etc/rhsm-host
RUN ls -la /etc/pki/entitlement-host/
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm; \
    dnf install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm; \
    dnf install -y mesa-libGL ffmpeg-libs ffmpeg-devel; \
    pip install -r /requirements.txt
USER 1001
