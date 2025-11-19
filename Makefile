.PHONY: help setup install check-env jupyter

# Default target: show help
help:
	@echo "AI Career Advisor - Environment Setup"
	@echo "======================================"
	@echo ""
	@echo "For new users:"
	@echo "  make setup          - Complete first-time setup (install uv, dependencies, configure .env)"
	@echo "  make jupyter        - Start Jupyter Lab to run ai-agent.ipynb"
	@echo ""
	@echo "Individual steps:"
	@echo "  make install        - Install dependencies using uv"
	@echo "  make check-env      - Verify .env file and API key configuration"

# Complete first-time setup for new users
setup: check-uv install check-env
	@echo ""
	@echo "Setup complete! Next steps:"
	@echo "   1. Make sure your GOOGLE_API_KEY is set in .env"
	@echo "   2. Run 'make jupyter' to start Jupyter Lab"
	@echo "   3. Open ai-agent.ipynb and run the cells"

# Check if uv is installed, install if not
check-uv:
	@echo "Checking for uv package manager..."
	@command -v uv >/dev/null 2>&1 || { \
		echo "uv not found. Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "uv installed successfully"; \
	}
	@echo "uv is installed"

# Install dependencies using uv
install:
	@echo "Installing dependencies with uv..."
	uv sync
	@echo "Dependencies installed"
