#!/bin/sh
echo "Checking variable \$SECRET_KEY"
if [ -z "$SECRET_KEY" ]; then
  echo "Container failed to start, please pass -e SECRET_KEY=your-key-for-django"
  exit 1
fi
exec "$@"