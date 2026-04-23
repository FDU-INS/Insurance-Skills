#!/bin/bash

# Symlink to main policy script for policy simulation
exec "$(dirname "$0")/check.sh" "$@"
