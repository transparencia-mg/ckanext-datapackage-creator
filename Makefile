.PHONY: help update-package clean-build build publish-build

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'

update-package: clean-build build publish-build ## Clean, build and publish new package version, python virtual env must be activated.

clean-build: ## Clean folders and files needed to build and publish package (build e dist folders and .egg-info file).
	@echo "Cleaning folders and files needed to build and publish package"
	@rm --force --recursive build/
	@rm --force --recursive dist/
	@rm --force --recursive *.egg-info
	@rm --force --recursive LICENCE.txt

build: ## Build folders and files needed to build and publish package
	@echo "Building package"
	@python setup.py sdist bdist_wheel

publish-build: ## Publish packate on Pypi
	@echo "Publishing package. Make sure package version was updated on setup.py file"
	@twine upload dist/*