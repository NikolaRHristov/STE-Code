#!/usr/bin/env bash
# jail-install.sh — link the jail into a Hermes profile from the single source.
#
# The jail lives ONCE in the repository at .agents/hermes/jail/. Every profile
# gets symlinks pointing back here, so editing the source updates every profile
# at once and no copy can drift.
#
# Usage:
#   jail-install.sh <profile> [--granular] [--dry-run]
#   jail-install.sh --all [--dry-run]
#   jail-install.sh --status
#
#   --granular   link jail-fs / jail-cmd / jail-net separately instead of the
#                ste-code-jail group plugin (for debugging a policy)
#   --dry-run    print what would happen, change nothing
#
# Profiles and their policies (see core/policy.py):
#   dev-ste-code        dev    permissive authoring
#   ste-code            user   locked down, read the standard
#   benchmark-ste-code  bench  locked down, adversarial prompts

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JAIL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROFILES_DIR="$HOME/.hermes/profiles"

GROUP_PLUGIN="ste-code-jail"
COMPONENTS=("jail-fs" "jail-cmd" "jail-net")
ALL_PROFILES=("dev-ste-code" "ste-code" "benchmark-ste-code")

DRY_RUN=0
GRANULAR=0

log()  { printf '%s\n' "$*"; }
run()  { if [ "$DRY_RUN" = "1" ]; then log "  would: $*"; else "$@"; fi; }

link_one() {
    # $1 = plugin name, $2 = profile plugins dir
    local name="$1" dest_dir="$2"
    local src="$JAIL_DIR/plugins/$name"
    local dest="$dest_dir/$name"

    if [ ! -d "$src" ]; then
        log "  ✗ source missing: $src"
        return 1
    fi

    if [ -L "$dest" ]; then
        local current
        current="$(readlink "$dest")"
        if [ "$current" = "$src" ]; then
            log "  = $name (already linked)"
            return 0
        fi
        run rm -f "$dest"
    elif [ -e "$dest" ]; then
        log "  ✗ $name exists and is NOT a symlink — refusing to replace it"
        log "    move it aside first: $dest"
        return 1
    fi

    run ln -sfn "$src" "$dest"
    log "  → $name"
}

install_profile() {
    local profile="$1"
    local dir="$PROFILES_DIR/$profile"

    log ""
    log "profile: $profile"

    if [ ! -d "$dir" ]; then
        log "  ✗ profile does not exist: $dir"
        log "    create it: hermes profile create $profile"
        return 1
    fi

    local plugins_dir="$dir/plugins"
    [ -d "$plugins_dir" ] || run mkdir -p "$plugins_dir"

    local failed=0
    if [ "$GRANULAR" = "1" ]; then
        for name in "${COMPONENTS[@]}"; do
            link_one "$name" "$plugins_dir" || failed=1
        done
    else
        link_one "$GROUP_PLUGIN" "$plugins_dir" || failed=1
    fi

    link_credentials "$dir" || failed=1
    seed_model_config "$dir" || failed=1

    # The policy is derived from the profile NAME, so no per-profile config is
    # required. A profile that needs an override drops its own jail.yaml here.
    log "  policy: $(policy_for "$profile")"
    return $failed
}

# A freshly created profile has a placeholder .env with no keys, so a live
# session cannot start. Point it at the shared credential store, exactly as
# dev-ste-code does. Only ever replaces a placeholder or an existing symlink —
# a real .env with content is left alone.
link_credentials() {
    local dir="$1"
    local shared="$HOME/.hermes/.env"
    local dest="$dir/.env"

    [ -e "$shared" ] || { log "  = .env (no shared store to link)"; return 0; }

    if [ -L "$dest" ]; then
        if [ "$(readlink "$dest")" = "$shared" ]; then
            log "  = .env (already linked)"
            return 0
        fi
        log "  ⚠ .env points elsewhere — leaving it alone"
        return 0
    fi

    # Treat a comments-only file as a placeholder: no KEY=value lines.
    if [ -f "$dest" ] && grep -qE '^[A-Za-z_][A-Za-z0-9_]*=' "$dest"; then
        log "  ⚠ .env holds real keys — leaving it alone"
        return 0
    fi

    run ln -sfn "$shared" "$dest"
    log "  → .env -> shared credential store"
}

# A profile with no config.yaml falls back to whatever the shell environment
# offers, which is how the live test hit "HTTP 402 Insufficient Balance" from a
# provider this project does not use.
#
# The config must ALSO enable the plugin. Hermes does not activate a plugin
# just because it is present in plugins/: it must be listed under
# `plugins.enabled`. A profile with the jail symlinked but not enabled looks
# perfectly installed and enforces NOTHING — the live test proved this by
# escaping all four cases while `--status` reported the link was fine.
seed_model_config() {
    local dir="$1"
    local dest="$dir/config.yaml"
    local source_cfg="$PROFILES_DIR/dev-ste-code/config.yaml"

    if [ "$DRY_RUN" = "1" ]; then
        log "  would: seed config.yaml (model + plugin enablement)"
        return 0
    fi

    if [ ! -e "$dest" ]; then
        if [ -f "$source_cfg" ]; then
            # Copy only the model block: the rest of the dev config is
            # authoring setup a locked-down profile must not inherit.
            awk '
                /^model:/           { inblock = 1; print; next }
                inblock && /^[ \t]/ { print; next }
                inblock             { inblock = 0 }
            ' "$source_cfg" > "$dest"
            log "  → config.yaml (model seeded from dev-ste-code)"
        else
            : > "$dest"
            log "  → config.yaml (created)"
        fi
    fi

    ensure_plugin_enabled "$dest"
}

# Append a `plugins.enabled` block naming the group plugin when the config does
# not already enable it. Without this the jail is inert.
ensure_plugin_enabled() {
    local dest="$1"
    local want="$GROUP_PLUGIN"
    [ "$GRANULAR" = "1" ] && want=""

    if grep -qE "^[[:space:]]*-[[:space:]]*(ste-code-jail|jail-fs)[[:space:]]*$" "$dest"; then
        log "  = config.yaml (jail already enabled)"
        return 0
    fi

    if grep -qE "^plugins:" "$dest"; then
        log "  ⚠ config.yaml has a plugins: block but does not enable the jail"
        log "    add this under plugins.enabled:  - $GROUP_PLUGIN"
        return 1
    fi

    {
        echo ""
        echo "# Enforce write confinement. The jail is inert unless enabled here."
        echo "plugins:"
        echo "  enabled:"
        if [ -n "$want" ]; then
            echo "    - $GROUP_PLUGIN"
        else
            for name in "${COMPONENTS[@]}"; do echo "    - $name"; done
        fi
        echo "  disabled: []"
        echo "  entries:"
        echo "    ${want:-jail-fs}:"
        echo "      allow_tool_override: false"
    } >> "$dest"
    log "  → config.yaml (jail ENABLED)"
}

policy_for() {
    case "$1" in
        dev-ste-code)       echo "dev   (permissive authoring)" ;;
        ste-code)           echo "user  (locked down; repo read-only)" ;;
        benchmark-ste-code) echo "bench (locked down; benchmark output only)" ;;
        *)                  echo "bench (FAIL CLOSED — profile not mapped)" ;;
    esac
}

show_status() {
    log "jail source: $JAIL_DIR"
    log ""
    for profile in "${ALL_PROFILES[@]}"; do
        local dir="$PROFILES_DIR/$profile"
        if [ ! -d "$dir" ]; then
            log "$profile: NOT CREATED"
            continue
        fi
        log "$profile: $(policy_for "$profile")"

        # Report ENABLEMENT, not just the link. A symlinked but unenabled
        # plugin enforces nothing while looking correctly installed.
        local cfg="$dir/config.yaml"
        if [ -f "$cfg" ] && grep -qE \
            "^[[:space:]]*-[[:space:]]*(ste-code-jail|jail-fs)[[:space:]]*$" "$cfg"; then
            log "  ✓ enabled in config.yaml"
        else
            log "  ✗ NOT ENABLED in config.yaml — the jail enforces NOTHING"
            log "    fix: $0 $profile"
        fi

        local found=0
        for name in "$GROUP_PLUGIN" "${COMPONENTS[@]}"; do
            local dest="$dir/plugins/$name"
            if [ -L "$dest" ]; then
                local target
                target="$(readlink "$dest")"
                if [ "$target" = "$JAIL_DIR/plugins/$name" ]; then
                    log "  ✓ $name -> single source"
                else
                    log "  ⚠ $name -> $target (NOT the single source)"
                fi
                found=1
            elif [ -e "$dest" ]; then
                log "  ⚠ $name is a real directory, not a symlink (will drift)"
                found=1
            fi
        done
        if [ "$found" = "0" ]; then
            log "  ✗ no jail plugin linked"
        fi
    done
}

targets=()
for arg in "$@"; do
    case "$arg" in
        --granular) GRANULAR=1 ;;
        --dry-run)  DRY_RUN=1 ;;
        --status)   show_status; exit 0 ;;
        --all)      targets=("${ALL_PROFILES[@]}") ;;
        -h|--help)  sed -n '2,22p' "$0"; exit 0 ;;
        -*)         log "unknown option: $arg"; exit 2 ;;
        *)          targets+=("$arg") ;;
    esac
done

if [ "${#targets[@]}" -eq 0 ]; then
    log "usage: jail-install.sh <profile> | --all | --status  [--granular] [--dry-run]"
    exit 2
fi

[ "$DRY_RUN" = "1" ] && log "(dry run — nothing will change)"

status=0
for profile in "${targets[@]}"; do
    install_profile "$profile" || status=1
done

log ""
if [ "$status" = "0" ]; then
    log "done. verify with: $0 --status"
else
    log "completed with errors."
fi
exit $status
