#!/bin/bash

# Script to run Jekyll site locally

echo "🚀 Starting local Jekyll server..."
echo ""

# Check Ruby version
RUBY_VERSION=$(ruby -v | grep -oE '[0-9]+\.[0-9]+' | head -1)
REQUIRED_VERSION="3.0"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$RUBY_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Ruby version $RUBY_VERSION is too old. Ruby >= 3.0 is required."
    echo ""
    echo "To upgrade Ruby on macOS:"
    echo "  1. Install Homebrew (if not installed): https://brew.sh"
    echo "  2. Install rbenv: brew install rbenv ruby-build"
    echo "  3. Add to ~/.zshrc: eval \"\$(rbenv init - zsh)\""
    echo "  4. Restart terminal"
    echo "  5. Install Ruby 3.3: rbenv install 3.3.0"
    echo "  6. Set as default: rbenv global 3.3.0"
    echo "  7. Verify: ruby -v"
    echo ""
    exit 1
fi

# Check if bundle is installed
if ! command -v bundle &> /dev/null
then
    echo "❌ Bundler is not installed. Please install it first:"
    echo "   gem install bundler"
    exit 1
fi

# Check if Gemfile.lock exists, if not, run bundle install
if [ ! -f "Gemfile.lock" ]; then
    echo "📦 Installing dependencies..."
    bundle install
    echo ""
fi

# Start Jekyll server
echo "🌐 Starting server at http://localhost:4000"
echo "Press Ctrl+C to stop the server"
echo ""

bundle exec jekyll serve --livereload
