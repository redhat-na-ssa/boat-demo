FROM quay.io/thoth-station/s2i-lab-elyra:latest

USER root
RUN ls -la /etc/pki/entitlement-host/
COPY requirements.txt /requirements.txt
COPY /etc/pki/entitlement-host/entitlement-key.pem /etc/pki/entitlement-host/
COPY /etc/pki/entitlement-host/entitlement.pem /etc/pki/entitlement-host/
COPY /etc/rhsm/rhsm.conf /etc/rhsm
COPY /etc/rhsm/ca/redhat-uep.pem /etc/rhsm/ca
RUN ls -la /etc/pki/entitlement; \
    dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm; \
    dnf install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm; \
    dnf install -y mesa-libGL ffmpeg-libs ffmpeg-devel; \
    pip install -r /requirements.txt
USER 1001
