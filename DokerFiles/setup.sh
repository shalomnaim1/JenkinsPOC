#!/bin/bash
set -x

echo "Decrypting credentials"
pushd integration_tests
python scripts/encrypt_conf.py -d --file credentials

echo "Rendering env.yaml"
popd
python /env_reander.py

set +x

