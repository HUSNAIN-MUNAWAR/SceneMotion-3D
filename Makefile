PYTHON ?= python
PIP ?= pip
VIDEO ?=

setup:
	$(PIP) install -r backend/requirements.txt

generate-sample:
	$(PYTHON) scripts/generate_sample_video.py

demo: generate-sample
	$(PYTHON) scripts/run_demo_pipeline.py

demo-custom:
	@if [ -z "$(VIDEO)" ]; then echo "Usage: make demo-custom VIDEO=path/to/video.mp4"; exit 1; fi
	$(PYTHON) scripts/run_demo_pipeline.py --video "$(VIDEO)" --out outputs/demo_custom

backend-dev:
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

frontend-dev:
	cd frontend && npm install && npm run dev

dev:
	@echo "Start backend with 'make backend-dev' and frontend with 'make frontend-dev'"

docker-up:
	docker compose up --build

backend-test:
	pytest tests -q

test:
	pytest tests -q

frontend-check:
	node scripts/check_frontend.mjs

benchmark-demo:
	$(PYTHON) scripts/run_benchmark_demo.py

bundle-demo: demo
	$(PYTHON) scripts/run_bundle_demo.py

screenshots:
	$(PYTHON) scripts/generate_screenshots.py

validate-final:
	$(PYTHON) scripts/validate_final.py

clean:
	rm -rf .pytest_cache **/__pycache__ outputs/runtime outputs/test_job outputs/demo_custom .next frontend/.next
