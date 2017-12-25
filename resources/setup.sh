#!/bin/bash
set -x

python /render_env.py

echo "Decrypting credentials"
pushd integration_tests
python scripts/encrypt_conf.py -d --file credentials
python lease_appliance.py

echo "Rendering env.yaml"
popd
python /render_env.py

set +x

