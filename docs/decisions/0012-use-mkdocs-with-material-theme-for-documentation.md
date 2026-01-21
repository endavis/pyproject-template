# ADR-0012: Use mkdocs with Material theme for documentation

## Status

Accepted

## Date

2025-01-21

## Context

Project documentation can be managed in several ways:

- **README only**: Simple but limited, doesn't scale
- **Wiki**: Separate from code, can drift out of sync
- **Sphinx**: Python standard, reStructuredText, powerful but complex
- **MkDocs**: Markdown-based, simple, modern themes
- **Docusaurus**: React-based, more complex setup
- **GitHub Pages with Jekyll**: Ruby-based, GitHub-native

The project needed documentation that:

- Lives alongside code (docs-as-code)
- Uses Markdown (familiar to most developers)
- Has a modern, responsive design
- Supports search
- Is easy to maintain
- Can be hosted on GitHub Pages

## Decision

Use **MkDocs** with the **Material for MkDocs** theme:

- **MkDocs**: Static site generator for Markdown documentation
- **Material theme**: Modern, responsive design with many features

Configuration in `mkdocs.yml`:
- Navigation structure defined explicitly
- Material theme with light/dark mode toggle
- Search enabled
- Code highlighting with copy buttons
- Admonitions for callouts

Documentation tasks via doit:
- `doit docs_build`: Build documentation site
- `doit docs_serve`: Serve locally for preview
- `doit docs_deploy`: Deploy to GitHub Pages

Structure:
- `docs/`: Documentation source files
- `docs/TABLE_OF_CONTENTS.md`: Auto-generated TOC
- `mkdocs.yml`: Site configuration

## Consequences

### Positive

- Markdown is easy to write and review
- Material theme looks professional out of the box
- Excellent search functionality
- Dark/light mode support
- Documentation stays in sync with code
- Free hosting on GitHub Pages

### Negative

- Another dependency to maintain
- Theme updates may require config changes
- Limited customization compared to Sphinx

### Neutral

- Requires building before deployment
- Navigation must be manually maintained in mkdocs.yml

## Participants

- Project maintainers

## Related

- [MkDocs documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [mkdocs.yml](../../mkdocs.yml)
