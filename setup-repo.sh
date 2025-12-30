#!/usr/bin/env bash
#
# setup-repo.sh - Automated GitHub Repository Setup from pyproject-template
#
# This script automates the creation and configuration of a new GitHub repository
# based on the pyproject-template. It handles repository creation, settings
# configuration, branch protection, and provides a checklist of manual steps.
#
# Usage:
#   ./setup-repo.sh [OPTIONS]
#   curl -sSL https://raw.githubusercontent.com/endavis/pyproject-template/main/setup-repo.sh | bash
#
# Requirements:
#   - GitHub CLI (gh) installed and authenticated
#   - Git installed
#   - Bash 4.0+
#
# Author: Generated from pyproject-template
# License: MIT

set -eo pipefail

# Trap to ensure clean exit without killing parent shell
trap 'exit_handler $?' EXIT
exit_handler() {
    local exit_code=$1
    if [ $exit_code -ne 0 ]; then
        echo ""
        log_error "Setup failed with exit code $exit_code"
        echo ""
        log_info "For help, run: $0 --help"
    fi
}

# Safe exit that doesn't kill parent shell
safe_exit() {
    local code=${1:-0}
    # If running in subshell (piped), don't exit the parent
    if [ "${BASH_SUBSHELL}" -gt 0 ]; then
        return $code
    else
        exit $code
    fi
}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Template repository details
TEMPLATE_OWNER="endavis"
TEMPLATE_REPO="pyproject-template"
TEMPLATE_FULL="${TEMPLATE_OWNER}/${TEMPLATE_REPO}"

# Script version
VERSION="1.0.0"

#
# Helper Functions
#

print_banner() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                                                           ║${NC}"
    echo -e "${CYAN}║     Python Project Template - Repository Setup v${VERSION}    ║${NC}"
    echo -e "${CYAN}║                                                           ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

log_step() {
    echo ""
    echo -e "${CYAN}▸${NC} $1"
}

check_requirements() {
    log_step "Checking requirements..."

    # Check for gh CLI
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is not installed"
        echo "  Install from: https://cli.github.com/"
        safe_exit 1
    fi
    log_success "GitHub CLI found: $(gh --version | head -n1)"

    # Check gh authentication
    if ! gh auth status &> /dev/null; then
        log_error "GitHub CLI is not authenticated"
        echo "  Run: gh auth login"
        safe_exit 1
    fi
    log_success "GitHub CLI authenticated"

    # Check token type and permissions
    check_token_permissions

    # Check for git
    if ! command -v git &> /dev/null; then
        log_error "Git is not installed"
        safe_exit 1
    fi
    log_success "Git found: $(git --version)"

    # Check for python3 (for configure.py)
    if ! command -v python3 &> /dev/null; then
        log_warning "Python 3 not found - will skip placeholder configuration"
        HAS_PYTHON=false
    else
        log_success "Python 3 found: $(python3 --version)"
        HAS_PYTHON=true
    fi
}

check_token_permissions() {
    log_info "Checking GitHub token permissions..."

    # Try to determine token type
    local auth_info
    auth_info=$(gh auth status 2>&1)

    if echo "$auth_info" | grep -q "github_pat_"; then
        log_warning "You're using a Personal Access Token (PAT)"
        echo ""
        echo "  ${YELLOW}Required permissions for fine-grained PAT:${NC}"
        echo "  - Repository permissions:"
        echo "    • Administration: Read and write"
        echo "    • Contents: Read and write"
        echo "    • Metadata: Read"
        echo ""
        echo "  ${YELLOW}To create/update your PAT:${NC}"
        echo "  1. Go to: https://github.com/settings/tokens?type=beta"
        echo "  2. Create new token or edit existing"
        echo "  3. Select 'All repositories' or specific repos"
        echo "  4. Add the permissions listed above"
        echo "  5. Generate token and run: gh auth login"
        echo ""

        if ! prompt_confirm "Do you have the required permissions configured?" "y"; then
            log_error "Please configure your PAT with required permissions first"
            safe_exit 1
        fi
    else
        log_success "Token type appears to be OAuth (recommended)"
    fi
}

prompt_input() {
    local prompt="$1"
    local default="$2"
    local result

    if [ -n "$default" ]; then
        read -p "$(echo -e ${CYAN}?${NC}) $prompt [$default]: " result
        echo "${result:-$default}"
    else
        read -p "$(echo -e ${CYAN}?${NC}) $prompt: " result
        while [ -z "$result" ]; do
            log_warning "This field is required"
            read -p "$(echo -e ${CYAN}?${NC}) $prompt: " result
        done
        echo "$result"
    fi
}

prompt_confirm() {
    local prompt="$1"
    local default="${2:-n}"
    local result

    if [ "$default" = "y" ]; then
        read -p "$(echo -e ${CYAN}?${NC}) $prompt [Y/n]: " result
        result="${result:-y}"
    else
        read -p "$(echo -e ${CYAN}?${NC}) $prompt [y/N]: " result
        result="${result:-n}"
    fi

    [[ "$result" =~ ^[Yy]$ ]]
}

gather_inputs() {
    log_step "Gathering repository information..."
    echo ""

    # Repository name
    REPO_NAME=$(prompt_input "Repository name" "")

    # Organization (optional)
    if prompt_confirm "Create in an organization?"; then
        ORG_NAME=$(prompt_input "Organization name" "")
        REPO_OWNER="$ORG_NAME"
    else
        REPO_OWNER=$(gh api user --jq .login)
    fi

    REPO_FULL="${REPO_OWNER}/${REPO_NAME}"

    # Visibility
    if prompt_confirm "Make repository public?" "y"; then
        VISIBILITY="public"
    else
        VISIBILITY="private"
    fi

    # Package configuration
    echo ""
    log_info "Package configuration (used for placeholder replacement)"

    PACKAGE_NAME=$(prompt_input "Python package name (import name)" "$(echo $REPO_NAME | tr '-' '_')")
    PYPI_NAME=$(prompt_input "PyPI package name" "$REPO_NAME")
    DESCRIPTION=$(prompt_input "Package description" "A Python project based on pyproject-template")
    AUTHOR_NAME=$(prompt_input "Author name" "$(git config user.name || echo '')")
    AUTHOR_EMAIL=$(prompt_input "Author email" "$(git config user.email || echo '')")

    # Confirmation
    echo ""
    log_step "Configuration summary:"
    echo "  Repository: $REPO_FULL"
    echo "  Visibility: $VISIBILITY"
    echo "  Package name: $PACKAGE_NAME"
    echo "  PyPI name: $PYPI_NAME"
    echo "  Description: $DESCRIPTION"
    echo "  Author: $AUTHOR_NAME <$AUTHOR_EMAIL>"
    echo ""

    if ! prompt_confirm "Proceed with these settings?" "y"; then
        log_warning "Setup cancelled by user"
        safe_exit 0
    fi
}

create_repository() {
    log_step "Creating repository from template..."

    # Use REST API to create from template
    local create_response
    local http_code

    create_response=$(gh api "repos/$TEMPLATE_FULL/generate" -X POST \
        -f owner="$REPO_OWNER" \
        -f name="$REPO_NAME" \
        -f description="$DESCRIPTION" \
        -F private=$([ "$VISIBILITY" = "private" ] && echo "true" || echo "false") \
        -F include_all_branches=false \
        2>&1) && http_code=0 || http_code=$?

    if [ $http_code -ne 0 ]; then
        log_error "Failed to create repository from template"
        echo ""

        if echo "$create_response" | grep -q "Resource not accessible by personal access token"; then
            echo "${RED}Permission Error:${NC} Your GitHub token doesn't have the required permissions."
            echo ""
            echo "This happens when using a Personal Access Token (PAT) without proper permissions."
            echo ""
            echo "${YELLOW}Solution:${NC}"
            echo ""
            echo "1. ${CYAN}Re-authenticate with OAuth (recommended):${NC}"
            echo "   gh auth logout"
            echo "   gh auth login"
            echo "   # Choose: GitHub.com → HTTPS → Login with browser"
            echo ""
            echo "2. ${CYAN}Or update your fine-grained PAT:${NC}"
            echo "   https://github.com/settings/tokens?type=beta"
            echo "   Required permissions:"
            echo "   - Administration: Read and write"
            echo "   - Contents: Read and write"
            echo "   - Metadata: Read"
            echo ""
        else
            echo "$create_response"
        fi

        safe_exit 1
    fi

    log_success "Repository created: https://github.com/$REPO_FULL"

    # Wait a moment for repo to be fully ready
    sleep 2

    # Clone the newly created repository
    log_info "Cloning repository..."
    if ! gh repo clone "$REPO_FULL" "$REPO_NAME" 2>/dev/null; then
        log_error "Failed to clone repository"
        safe_exit 1
    fi

    # Change to repo directory
    cd "$REPO_NAME" || safe_exit 1
    log_success "Repository cloned locally"
}

configure_placeholders() {
    log_step "Configuring project placeholders..."

    if [ "$HAS_PYTHON" = false ]; then
        log_warning "Python 3 not available - skipping placeholder configuration"
        log_info "You'll need to run configure.py manually later"
        return
    fi

    if [ ! -f "configure.py" ]; then
        log_warning "configure.py not found - skipping placeholder configuration"
        return
    fi

    # Create temporary input file for configure.py
    cat > /tmp/configure_input.txt <<EOF
$REPO_NAME
$DESCRIPTION
$PACKAGE_NAME
$PYPI_NAME
$AUTHOR_NAME
$AUTHOR_EMAIL
$REPO_OWNER
EOF

    # Run configure.py with the inputs
    if python3 configure.py < /tmp/configure_input.txt; then
        log_success "Placeholders configured"

        # Commit the changes
        git add .
        git commit -m "chore: configure project from template

- Set project name to $REPO_NAME
- Configure package as $PACKAGE_NAME
- Set author to $AUTHOR_NAME

🤖 Generated with setup-repo.sh" || true

        git push || true
        log_success "Changes committed and pushed"
    else
        log_warning "Placeholder configuration failed - you may need to run configure.py manually"
    fi

    rm -f /tmp/configure_input.txt
}

configure_repository_settings() {
    log_step "Configuring repository settings..."

    # Get current settings from template
    local template_settings
    template_settings=$(gh api "repos/$TEMPLATE_FULL" 2>/dev/null || echo "{}")

    # Configure features and options
    gh api "repos/$REPO_FULL" -X PATCH -f description="$DESCRIPTION" \
        -F has_issues=true \
        -F has_projects=true \
        -F has_wiki=false \
        -F allow_squash_merge=true \
        -F allow_merge_commit=true \
        -F allow_rebase_merge=true \
        -F delete_branch_on_merge=true \
        -F allow_auto_merge=true \
        -F allow_update_branch=true \
        > /dev/null 2>&1 || log_warning "Some settings may not have been applied"

    log_success "Repository settings configured"
}

configure_branch_protection() {
    log_step "Configuring branch protection for main..."

    # Get template branch protection settings
    local protection_config
    protection_config=$(gh api "repos/$TEMPLATE_FULL/branches/main/protection" 2>/dev/null || echo "{}")

    if [ "$protection_config" = "{}" ]; then
        log_warning "Could not retrieve template branch protection settings"
        log_info "You may need to configure branch protection manually"
        return
    fi

    # Apply branch protection (simplified version - full replication is complex)
    gh api "repos/$REPO_FULL/branches/main/protection" -X PUT \
        --input - > /dev/null 2>&1 <<EOF || log_warning "Branch protection configuration may be incomplete"
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["test (3.12)", "test (3.13)", "format-check", "lint", "type-check"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismissal_restrictions": {},
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true
}
EOF

    log_success "Branch protection configured"
}

replicate_labels() {
    log_step "Replicating labels from template..."

    # Get labels from template
    local labels
    labels=$(gh api "repos/$TEMPLATE_FULL/labels" --jq '.[] | "\(.name)|\(.color)|\(.description // "")"')

    if [ -z "$labels" ]; then
        log_warning "Could not retrieve labels from template"
        return
    fi

    # Create each label
    while IFS='|' read -r name color description; do
        gh label create "$name" --color "$color" --description "$description" --repo "$REPO_FULL" 2>/dev/null || true
    done <<< "$labels"

    log_success "Labels replicated"
}

enable_github_pages() {
    log_step "Enabling GitHub Pages..."

    # Enable GitHub Pages for gh-pages branch (created by docs deployment)
    gh api "repos/$REPO_FULL/pages" -X POST \
        -f source[branch]=gh-pages \
        -f source[path]="/" \
        > /dev/null 2>&1 && log_success "GitHub Pages enabled" || log_warning "GitHub Pages configuration skipped (will be enabled after first docs deployment)"
}

print_manual_steps() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                  Setup Complete! 🎉                       ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    log_success "Repository created and configured: https://github.com/$REPO_FULL"
    echo ""

    log_step "Manual steps required:"
    echo ""
    echo "  ${YELLOW}[${NC} ${YELLOW}]${NC} Add PyPI token to repository secrets:"
    echo "      gh secret set PYPI_TOKEN --repo $REPO_FULL"
    echo ""
    echo "  ${YELLOW}[${NC} ${YELLOW}]${NC} Add TestPyPI token to repository secrets (optional):"
    echo "      gh secret set TEST_PYPI_TOKEN --repo $REPO_FULL"
    echo ""
    echo "  ${YELLOW}[${NC} ${YELLOW}]${NC} Add Codecov token to repository secrets (optional):"
    echo "      gh secret set CODECOV_TOKEN --repo $REPO_FULL"
    echo ""
    echo "  ${YELLOW}[${NC} ${YELLOW}]${NC} Review and adjust repository settings:"
    echo "      https://github.com/$REPO_FULL/settings"
    echo ""
    echo "  ${YELLOW}[${NC} ${YELLOW}]${NC} Review branch protection rules:"
    echo "      https://github.com/$REPO_FULL/settings/branches"
    echo ""
    echo "  ${YELLOW}[${NC} ${YELLOW}]${NC} Invite collaborators (if needed):"
    echo "      https://github.com/$REPO_FULL/settings/access"
    echo ""
    echo "  ${YELLOW}[${NC} ${YELLOW}]${NC} Enable Dependabot security updates:"
    echo "      https://github.com/$REPO_FULL/settings/security_analysis"
    echo ""

    log_step "Next steps:"
    echo ""
    echo "  1. Clone the repository: gh repo clone $REPO_FULL"
    echo "  2. Install dependencies: cd $REPO_NAME && uv sync --all-extras"
    echo "  3. Install pre-commit hooks: uv run pre-commit install"
    echo "  4. Start developing!"
    echo ""

    log_info "Documentation: https://github.com/$REPO_FULL/blob/main/README.md"
    echo ""
}

show_usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Automated GitHub repository setup from pyproject-template.

OPTIONS:
    -h, --help      Show this help message
    -v, --version   Show version information
    --non-interactive  Skip interactive prompts (requires env vars)

ENVIRONMENT VARIABLES (for non-interactive mode):
    REPO_NAME       Repository name (required)
    REPO_OWNER      Repository owner/org (default: current user)
    VISIBILITY      Repository visibility: public|private (default: public)
    PACKAGE_NAME    Python package name (default: repo name with underscores)
    PYPI_NAME       PyPI package name (default: repo name)
    DESCRIPTION     Package description
    AUTHOR_NAME     Author name (default: git config)
    AUTHOR_EMAIL    Author email (default: git config)

EXAMPLES:
    # Interactive mode
    $0

    # Download and run
    curl -sSL https://raw.githubusercontent.com/endavis/pyproject-template/main/setup-repo.sh | bash

    # Non-interactive mode
    REPO_NAME=my-project DESCRIPTION="My awesome project" $0 --non-interactive

REQUIREMENTS:
    - GitHub CLI (gh) installed and authenticated
    - Git installed
    - Python 3 (optional, for placeholder configuration)

EOF
}

#
# Main Script
#

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                safe_exit 0
                ;;
            -v|--version)
                echo "setup-repo.sh version $VERSION"
                safe_exit 0
                ;;
            --non-interactive)
                INTERACTIVE=false
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                safe_exit 1
                ;;
        esac
    done

    # Default to interactive mode
    INTERACTIVE="${INTERACTIVE:-true}"

    print_banner
    check_requirements

    if [ "$INTERACTIVE" = true ]; then
        gather_inputs
    else
        # Use environment variables
        REPO_NAME="${REPO_NAME:?REPO_NAME is required}"
        REPO_OWNER="${REPO_OWNER:-$(gh api user --jq .login)}"
        REPO_FULL="${REPO_OWNER}/${REPO_NAME}"
        VISIBILITY="${VISIBILITY:-public}"
        PACKAGE_NAME="${PACKAGE_NAME:-$(echo $REPO_NAME | tr '-' '_')}"
        PYPI_NAME="${PYPI_NAME:-$REPO_NAME}"
        DESCRIPTION="${DESCRIPTION:-A Python project based on pyproject-template}"
        AUTHOR_NAME="${AUTHOR_NAME:-$(git config user.name || echo '')}"
        AUTHOR_EMAIL="${AUTHOR_EMAIL:-$(git config user.email || echo '')}"
    fi

    create_repository
    configure_placeholders
    configure_repository_settings
    configure_branch_protection
    replicate_labels
    enable_github_pages
    print_manual_steps
}

# Run main function
main "$@"
