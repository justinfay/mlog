devbuild:
	rm -rf html && python -m mlog && cd html && python -m http.server

test:
	nosetests test/*

pyclean:
	find ./mlog/* -name "*.pyc" -delete

.PHONY: test
