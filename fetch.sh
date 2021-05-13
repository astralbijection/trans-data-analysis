#!/bin/sh

OUTFILE="$1"

twarc --recursive search '"transgender" OR "trans person" OR "trans people" OR "transmasc" OR "transfem" OR "trans man" OR "trans woman" OR "trans boy" OR "trans girl" OR "trans men" OR "trans women" OR "enby" OR "non binary"' | tee /dev/tty | gzip --stdout > $OUTFILE