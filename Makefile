.PHONY: test lint install audit-mini

test:
	bash scripts/smoke_test.sh
	bash scripts/selftest.sh
	bash scripts/selftest_extended.sh
	bash scripts/install_selftest.sh
	bash scripts/autopilot_selftest.sh

lint:
	python3 -m py_compile scripts/*.py
	python3 scripts/check_conference.py conferences/*.md

install:
	./install.sh

audit-mini:
	bash scripts/audit.sh examples/mini-paper examples/mini-paper/paper_state

selftest:
	bash scripts/selftest.sh
