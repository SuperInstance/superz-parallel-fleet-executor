# Super Z — Parallel Fleet Executor
# Common operations

.PHONY: help test boot validate scan health quality stats clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test: ## Run all tests
	python -m pytest tests/ -v

boot: ## Run boot sequence
	python3 vessel/tools/boot.py

validate: ## Validate lighthouse config
	python3 vessel/tools/boot.py --validate

scan: ## Scan for pending directives
	python3 vessel/tools/boot.py --scan

health: ## Generate health response
	python3 vessel/tools/boot.py --health

quality: ## Run quality validator on docs/
	python3 vessel/tools/quality_validator.py check-dir docs/

stats: ## Show quality stats for a file (usage: make stats FILE=path/to/file)
	python3 vessel/tools/quality_validator.py stats $(FILE)

wave: ## Plan a wave (usage: make wave TASKS="task1, task2, task3")
	python3 vessel/tools/wave_launcher.py plan "$(TASKS)"

wave-status: ## Show current wave status
	python3 vessel/tools/wave_launcher.py status

audit: ## Generate audit checklist (usage: make audit TARGET=path/to/file)
	python3 vessel/tools/audit_checklist.py run $(TARGET)

clean: ## Remove generated/temporary files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -f agent-personallog/wave-state.json
