FROM fedora

ENV PYCURL_SSL_LIBRARY "openssl"
ENV GIT_SSL_NO_VERIFY false 

ADD resources/requirements-additional.txt /
ADD resources/render_env.py / 
ADD resources/setup.sh /
ADD resources/env.yaml.template /

RUN dnf update -y \
    && dnf install -y git docutils python vim \
    && curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" \
    && python get-pip.py \
    && pip install -Ur requirements-additional.txt \
    && git clone https://github.com/ManageIQ/integration_tests.git \
    && git clone https://gitlab.cee.redhat.com/cfme-qe/cfme-qe-yamls.git \
    && cd integration_tests \
    && dnf install -y $(python -c "import cfme.scripting.quickstart as q;print q.REDHAT_PACKAGES") \
    && pip install -Ur requirements.txt \
    && pip uninstall -y numpy \
    && easy_install numpy \
    && rm -f conf/* \
    && cp ../cfme-qe-yamls/complete/cfme_data.yaml conf/ \
    && cp ../cfme-qe-yamls/complete/credentials.eyaml conf/

ADD resources/lease_appliance.py /integration_tests

