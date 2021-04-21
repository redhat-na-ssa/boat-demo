FROM quay.io/thoth-station/s2i-lab-elyra:latest

USER root
RUN ls -la ~
RUN mkdir /root/entitlements
COPY requirements.txt /requirements.txt
COPY /etc/pki/entitlement/* /root/entitlements/
RUN mkdir -p /run/secrets/etc-pki-entitlement-host; \
    ls -la /etc/pki/entitlement-host/; \
    cp -rav /root/entitlements/* /run/secrets/etc-pki-entitlement-host/; \
    ls -la /etc/pki/entitlement-host/; \
    dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm; \
    dnf install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm; \
    dnf install -y mesa-libGL ffmpeg-libs ffmpeg-devel; \
    pip install -r /requirements.txt
USER 1001
