#!/bin/bash

# Symlink to main policy script for policy validation
exec "$(dirname "$0")/check.sh" "$@"
