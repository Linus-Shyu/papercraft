.PHONY: test lint install audit-mini

test:
	bash scripts/smoke_test.sh

lint:
	python3 -m py_compile scripts/*.py
	python3 scripts/check_conference.py conferences/*.md

install:
	./install.sh

audit-mini:
	bash scripts/audit.sh examples/mini-paper examples/mini-paper/paper_state
