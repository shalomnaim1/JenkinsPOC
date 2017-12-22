# JenkinsPOC

In this project, we dockerize integration test for Jenkins builds.
We create a DockerFile to build a docker image of integration test, this image will create a Fedora environment with all the dependencies that required to run tests.

# Image creation steps:
1. Clone base Image (Fedora image)
1. Export the relevant environment variables
1. Install all the dependencies
1. Placing configuration files
1. decrypt of the credential
1. Rendering the environment file (during the container initiation)

# Required environment variables
APPLINCE_IP: IP address of a CFME appliance
WHARF_IP: IP address of a selenium server, we decided to work with Whorf
WHARF_PORT: Port of a selenium container
CONF_PATH: Path of integration test config files
YAYCL_CRYPT_KEY: Key for credentials decryption

# Author spacial parameters
If a result file (XUnit or JUnit) is required you may have to share a host filesystem with the container.
This can be done using `-v` option while you starting the container, and setting pytest to save the results on this path.

# How to create and run an Image
To create a image just run the following command:
```{bash}
docker build -t <image_name>:<image tag> -f <doker_file_page> .
```

When the image file is ready, you can run the tests inside the container,

In the following example, I will show how to start running CMQE test using a container and save the results to local dir (/tmp/results) on the host.
The container will start in detach mode (run in the background)

```{bash}
docker run -d
           -v /tmp/results:/tmp --privileged
           -e APPLINCE_IP 1.2.3.4
           -e WHARF_IP 5.6.7.8
           -e WHARF_PORT 80
           -e CONF_PATH /integration_tests/conf
