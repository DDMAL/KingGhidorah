PACKAGE_VERSION = `cat pyproject.toml | grep version | head -1 | sed 's/version = //g' | sed 's/"//g'`
build:
	@git tag -a "v$(PACKAGE_VERSION)" -m "New Release"

publish:
	@git push origin --tags
	@poetry build
	@poetry publish