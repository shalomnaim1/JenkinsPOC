#!/bin/bash
set -xe

pushd integration_tests
echo "Setting basic env.yml"
python env_maintainer.py --action setup --populate_sprout_only --sprout_url $SPROUT_URL --config_path conf/

echo "Decrypting credentials yaml"

python scripts/encrypt_conf.py -d --file credentials
echo "lease an appliance fro sproute and updating env.yml accordingly"
python env_maintainer.py --action setup \
                         --lease_appliance \
                         --stream $STREAM \
                         --wharf_ip $WHARF_IP \
                         --wharf_port $WHARF_PORT \
                         --sprout_url $SPROUT_URL
                         --config_path conf/
set +x
