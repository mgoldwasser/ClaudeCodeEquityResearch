# shellcheck shell=bash
# Shared --as-of contract helper for bash data-retrieval tools.
# See tools/AS_OF.md for the specification.
#
# Source this file from each tool:
#     # shellcheck source=_as_of.sh
#     source "$(dirname "$0")/_as_of.sh"
#
# Exports:
#   AS_OF         - resolved date in YYYY-MM-DD, or empty string in live mode
#   AS_OF_EPOCH   - UTC epoch of end-of-day(AS_OF), or empty string
#   as_of_resolve "$cli_value"               - parse flag+env, populate globals
#   as_of_is_historical                      - returns 0 if historical, 1 if live
#   as_of_assert_live_only "tool" "cmd" \
#                          "reason" "alt"    - hard-fail if historical
#   as_of_strip_flag "$@"                    - echo args with --as-of X removed

AS_OF=""
AS_OF_EPOCH=""
_AS_OF_ENV_VAR="EQUITY_SWARM_AS_OF"
_AS_OF_MIN="1990-01-01"
_AS_OF_EXIT_PARSE=1
_AS_OF_EXIT_CURRENT_ONLY=2

_as_of_validate() {
    local s="$1" source="$2"
    if [[ ! "$s" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo "ERROR: invalid --as-of value '${s}' from ${source}. Expected format YYYY-MM-DD." >&2
        exit "${_AS_OF_EXIT_PARSE}"
    fi
    # Reject pre-1990 lexicographically (works for YYYY-MM-DD)
    if [[ "$s" < "${_AS_OF_MIN}" ]]; then
        echo "ERROR: --as-of ${s} is before minimum supported date ${_AS_OF_MIN}." >&2
        exit "${_AS_OF_EXIT_PARSE}"
    fi
    # Probe parseability via date(1) — GNU and BSD differ but both accept YYYY-MM-DD
    if ! date -j -f "%Y-%m-%d" "$s" "+%s" >/dev/null 2>&1 \
       && ! date -d "$s" "+%s" >/dev/null 2>&1; then
        echo "ERROR: --as-of ${s} could not be parsed by date(1)." >&2
        exit "${_AS_OF_EXIT_PARSE}"
    fi
}

_as_of_to_epoch() {
    # End-of-day UTC epoch for the given YYYY-MM-DD.
    local s="$1"
    # BSD date (macOS): -u forces UTC interpretation of the input.
    if date -u -j -f "%Y-%m-%dT%H:%M:%S" "${s}T23:59:59" "+%s" 2>/dev/null; then
        return 0
    fi
    # GNU date (Linux): -u forces UTC; -d parses the string.
    date -u -d "${s} 23:59:59 UTC" "+%s"
}

_as_of_today() {
    date -u "+%Y-%m-%d"
}

# Portable uppercase helper — works on bash 3.2 (macOS default) where ${var^^} is unavailable.
as_of_upper() {
    printf '%s' "$1" | tr '[:lower:]' '[:upper:]'
}

as_of_resolve() {
    local cli_value="${1:-}"
    local raw source today
    if [[ -n "$cli_value" ]]; then
        raw="$cli_value"
        source="--as-of flag"
    elif [[ -n "${!_AS_OF_ENV_VAR:-}" ]]; then
        raw="${!_AS_OF_ENV_VAR}"
        source="\$${_AS_OF_ENV_VAR}"
    else
        AS_OF=""
        AS_OF_EPOCH=""
        return 0
    fi

    _as_of_validate "$raw" "$source"
    today="$(_as_of_today)"
    if [[ "$raw" > "$today" || "$raw" == "$today" ]]; then
        AS_OF=""
        AS_OF_EPOCH=""
        return 0
    fi

    AS_OF="$raw"
    AS_OF_EPOCH="$(_as_of_to_epoch "$raw")"
    echo "[as-of] historical mode: ${AS_OF}" >&2
}

as_of_is_historical() {
    [[ -n "$AS_OF" ]]
}

as_of_assert_live_only() {
    local tool="$1" cmd="$2" reason="$3" alt="${4:-}"
    if ! as_of_is_historical; then
        return 0
    fi
    echo "ERROR: ${tool} ${cmd} --as-of ${AS_OF} is not supported." >&2
    echo "  Reason: ${reason}" >&2
    if [[ -n "$alt" ]]; then
        echo "  Alternative: ${alt}" >&2
    fi
    exit "${_AS_OF_EXIT_CURRENT_ONLY}"
}

# Parse --as-of out of an argv. Populates AS_OF_CLI and REST_ARGS (array).
# Works on bash 3.2+ (no mapfile / process substitution dependency).
# Usage:
#     as_of_extract_flag "$@"
#     as_of_resolve "${AS_OF_CLI}"
#     set -- "${REST_ARGS[@]}"
AS_OF_CLI=""
REST_ARGS=()
as_of_extract_flag() {
    AS_OF_CLI=""
    REST_ARGS=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --as-of)
                AS_OF_CLI="${2:-}"
                shift 2 || shift
                ;;
            --as-of=*)
                AS_OF_CLI="${1#--as-of=}"
                shift
                ;;
            *)
                REST_ARGS+=("$1")
                shift
                ;;
        esac
    done
}
