# META ]--------------------------------------------------------------------------------------------
.PHONY: help.stub help
help.stub: help

help:
	@echo "help             Display this message."
	@echo "run.             Run SpotiQuote example in foreground with:"
	@echo "  default          defaults (no memos, ads silenced)."
	@echo "  programmer       programmer adages read at the beginning of silenced ads."
	@echo "  japanese         Japanese word learning example."
	@echo "  buddhism         Buddhist quote after every played (reached last 5s) song."
	@echo "  cognitive        Cognitive bias definitions after every played (reached last 5s) song."
	@echo "                     - Memo file of this example uses \"...\" to space defitions/terms."
	@echo "test             Run testing suite."
	@echo "clean            Clean repository."
	@echo "deps             Install dependencies."

# EXAMPLES ]----------------------------------------------------------------------------------------
.PHONY: run.default run.japanese run.buddhism

run.default:
	python SpotiQuote.py

run.programmer:
	python SpotiQuote.py \
	  --memos memos/programmer_adages.txt

run.japanese:
	python SpotiQuote.py \
	  --memos memos/japanese.txt \
	  --voice samantha

run.buddhism:
	python SpotiQuote.py \
	  --memos memos/buddhist_quotes.txt \
	  --voice moira \
	  --after_num_plays 1

run.cognitive:
	python SpotiQuote.py \
	  --memos memos/list_of_cognitive_biases.txt \
	  --voice daniel \
	  --after_num_plays 1

# CORE ]--------------------------------------------------------------------------------------------
.PHONY: test clean deps

test:
	pylint *.py

clean: deps
	rm spotiquote.pid
	black .

deps:
	pip install black
