#!/bin/bash

# Symlink to main policy script for rule testing
exec "$(dirname "$0")/check.sh" "$@"
