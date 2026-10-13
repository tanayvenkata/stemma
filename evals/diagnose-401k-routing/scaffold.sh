#!/usr/bin/env bash
# Copy this case's fixture (a slice of a real project) into the run's workspace.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -R "$here/fixture/." .
