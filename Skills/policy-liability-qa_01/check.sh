#!/bin/bash

# T81 Policy Checker Skill Wrapper
# Bridges OpenClaw skill to T81 Axion policy engine

set -euo pipefail

# Default values
POLICY_FILE=""
CONTEXT_FILE=""
CANONFS_ROOT="${T81_CANONFS_ROOT:-$HOME/.t81_canonfs}"
DRY_RUN=""
VERBOSE=""

# Parse arguments
OPERATION=""
RESOURCE=""
ARGS=("$@")
i=0
while [ $i -lt ${#ARGS[@]} ]; do
    case "${ARGS[$i]}" in
        --policy)
            ((i++))
            POLICY_FILE="${ARGS[$i]}"
            ;;
        --context)
            ((i++))
            CONTEXT_FILE="${ARGS[$i]}"
            ;;
        --canonfs-root)
            ((i++))
            CANONFS_ROOT="${ARGS[$i]}"
            ;;
        --dry-run)
            DRY_RUN="--dry-run"
            ;;
        --verbose|-v)
            VERBOSE="--verbose"
            ;;
        -*)
            echo "Error: Unknown option ${ARGS[$i]}" >&2
            exit 1
            ;;
        *)
            if [ -z "$OPERATION" ]; then
                OPERATION="${ARGS[$i]}"
            elif [ -z "$RESOURCE" ]; then
                RESOURCE="${ARGS[$i]}"
            else
                echo "Error: Too many arguments" >&2
                exit 1
            fi
            ;;
    esac
    ((i++))
done

# Validate input
if [ -z "$OPERATION" ] || [ -z "$RESOURCE" ]; then
    echo "Error: Both operation and resource must be specified" >&2
    echo "Usage: check <operation> <resource> [--policy <policy_file>] [--context <context_file>]" >&2
    exit 1
fi

# Check if T81 CLI is available
if ! command -v t81 &> /dev/null; then
    echo "Error: T81 CLI not found. Please install T81 Foundation." >&2
    exit 1
fi

# Validate policy file if specified
if [ -n "$POLICY_FILE" ] && [ ! -f "$POLICY_FILE" ]; then
    echo "Error: Policy file not found: $POLICY_FILE" >&2
    exit 1
fi

# Validate context file if specified
if [ -n "$CONTEXT_FILE" ] && [ ! -f "$CONTEXT_FILE" ]; then
    echo "Error: Context file not found: $CONTEXT_FILE" >&2
    exit 1
fi

# Create CanonFS root if it doesn't exist
mkdir -p "$CANONFS_ROOT"

# Determine command based on script name
case "$(basename "$0")" in
    check.sh)
        T81_CMD="t81 axion check"
        ;;
    validate-policy.sh)
        T81_CMD="t81 axion validate-policy"
        ;;
    test-rule.sh)
        T81_CMD="t81 axion test-rule"
        ;;
    list-policies.sh)
        T81_CMD="t81 axion list-policies"
        ;;
    simulate.sh)
        T81_CMD="t81 axion simulate"
        ;;
    *)
        echo "Error: Unknown policy script: $(basename "$0")" >&2
        exit 1
        ;;
esac

# Build T81 command
if [ "$(basename "$0")" != "list-policies.sh" ]; then
    if [ "$OPERATION" != "validate-policy" ] && [ "$OPERATION" != "test-rule" ]; then
        T81_CMD="$T81_CMD $OPERATION"
    fi
fi

if [ -n "$RESOURCE" ] && [ "$(basename "$0")" != "list-policies.sh" ]; then
    T81_CMD="$T81_CMD \"$RESOURCE\""
fi

if [ -n "$POLICY_FILE" ]; then
    T81_CMD="$T81_CMD --policy \"$POLICY_FILE\""
fi

if [ -n "$CONTEXT_FILE" ]; then
    T81_CMD="$T81_CMD --context \"$CONTEXT_FILE\""
fi

if [ -n "$CANONFS_ROOT" ]; then
    T81_CMD="$T81_CMD --canonfs-root \"$CANONFS_ROOT\""
fi

if [ -n "$DRY_RUN" ]; then
    T81_CMD="$T81_CMD $DRY_RUN"
fi

# Always output JSON for machine readability
T81_CMD="$T81_CMD --json"

if [ -n "$VERBOSE" ]; then
    echo "Executing: $T81_CMD" >&2
fi

# Execute T81 policy check
eval "$T81_CMD"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    if [ -n "$VERBOSE" ]; then
        echo "Policy check completed successfully" >&2
    fi
else
    echo "Error: Policy check failed with exit code $EXIT_CODE" >&2
    exit $EXIT_CODE
fi
