devbuild:
	rm -rf html && python -m mlog && cd html && python -m http.server
