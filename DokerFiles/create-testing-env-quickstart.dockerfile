FROM fedora
ENV GIT_SSL_NO_VERIFY false 
RUN dnf update -y \
    && dnf install -y git python \
    && git clone https://github.com/ManageIQ/integration_tests.git \
    && git clone https://gitlab.cee.redhat.com/cfme-qe/cfme-qe-yamls.git \
    && cd integration_tests \
    && python cfme/scripting/quickstart.py 
