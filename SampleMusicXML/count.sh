#!/usr/bin/bash
bash cleanup.sh
echo "passes:"
find testcases/lilypond-passing-tests -type f | wc -l
echo "to-pass:"
find testcases/lilypond-provided-testcases -type f | wc -l
echo "ignored:"
find testcases/ignored-lilypond-testcases -type f | wc -l
