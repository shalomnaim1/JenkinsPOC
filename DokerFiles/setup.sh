#!/bin/bash
set -x

echo "Decrypting credentials"
cd integration_tests
python scripts/encrypt_conf.py -d --file credentials

echo "Rendering env.yaml"
cd ..
python /env_reander.py

set +x

