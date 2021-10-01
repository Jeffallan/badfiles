build:
	./random_files.sh
	rm ./test/*.bin
	rm ./test/*.sh
	rm ./test/*.jpg
	rm ./test/zip-bomb.py
	pytest -v .

clean:
	rm -rf test

run_test:
	pytest -v . # -s for print statements

prepare:
	tox
	pre-commit run --all-files
