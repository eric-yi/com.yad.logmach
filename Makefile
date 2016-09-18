#************************************************
# Makefile
# -----
# 05/31/2016
#------------------------------------------------

ROOT =.
SRC =$(ROOT)/src
DEPS =$(ROOT)/requirements.txt
TARGET =$(ROOT)/target
PIP =pip

.PHONY : clean init

default: clean init

init:
	$(PIP) install -r ${DEPS}

clean:
	$(RM) -r ${TARGET}
