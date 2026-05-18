#!/bin/bash

# Symlink to main policy script for policy listing
exec "$(dirname "$0")/check.sh" "$@"
