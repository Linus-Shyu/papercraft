.PHONY: test test-fast lint install audit-mini

test-fast:
	bash scripts/selftest.sh
	bash scripts/selftest_extended.sh
	bash scripts/install_selftest.sh
	bash scripts/template_selftest.sh
	bash scripts/resubmit_selftest.sh
	bash scripts/directory_selftest.sh

test:
	bash scripts/smoke_test.sh
	bash scripts/selftest.sh
	bash scripts/selftest_extended.sh
	bash scripts/install_selftest.sh
	bash scripts/autopilot_selftest.sh
	bash scripts/template_selftest.sh
	bash scripts/resubmit_selftest.sh
	bash scripts/directory_selftest.sh

lint:
	python3 -m py_compile scripts/*.py
	python3 scripts/check_conference.py conferences/*.md
	python3 scripts/check_directory.py --directory conferences/directory.json

install:
	./install.sh

audit-mini:
	bash scripts/audit.sh examples/mini-paper examples/mini-paper/paper_state

selftest:
	bash scripts/selftest.sh
