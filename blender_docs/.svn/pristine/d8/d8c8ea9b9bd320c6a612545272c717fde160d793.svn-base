#!/bin/bash
# Apache License, Version 2.0

# This script is to reduce tedious steps involved when updating PO files.
# It looks more complex then it really is, since we do multi-processing
# to update the PO files, to save some time.

# Subversion Checkout Location
# ============================
#
# Note: this script supports subversion repositories at these locations:
#
# ./local/(.svn)          All languages in one checkout.
# ./local/{LANG}/(.svn)   Each language in it's own checkout.
#
# All commands run from the project root, passing in paths
# without changing directories.
#
# This works since subversion will detect the parent directories ".svn"
# path without us having to change directories.


# Trap on the ERR pseudo signal
# http://stackoverflow.com/a/4384381/432509
err_trap () {
  errcode=$? # save the exit code as the first thing done in the trap function
	echo "  Error($errcode) on line ${BASH_LINENO[0]}, in command:"
  echo "  $BASH_COMMAND"
  exit $errcode
}
trap err_trap ERR

# Python needs utf
export LANG="en_US.UTF-8"

# Ensure we're in the repo's base:
BASEDIR="$(dirname $0)"
cd $BASEDIR
cd ../
ROOTDIR="$(pwd)"


# All directories containing '.svn' (the parent directory).
SVN_DIRS_ALL="$(find locale/ -name '.svn' -printf '%h\n')"

# Update the locale dir:
for SVNDIR in "$SVN_DIRS_ALL"; do
  svn cleanup "$SVNDIR"
  svn up "$SVNDIR"
done
unset SVNDIR

# Create PO files:
rm -rf build/locale
make gettext


# Update PO files
#
# note, this can be slow so (multi-process)
for PO_LANG in $(find locale/ -maxdepth 1 -mindepth 1 -type d -not -iwholename '*.svn*' -printf '%f\n' | sort); do
	sphinx-intl --config=manual/conf.py update --pot-dir=build/locale --language="$PO_LANG" &
done
unset PO_LANG

FAIL=0
for JOB in $(jobs -p); do
  echo "$JOB"
  wait $JOB || let "FAIL+=1"
done
unset JOB
if [ "$FAIL" != "0" ]; then
	echo "Error updating"
	exit 1
fi
unset FAIL

# Add newly created PO files:
for SVNDIR in "$SVN_DIRS_ALL"; do

  NEW_FILES=$(svn status "$SVNDIR" | grep -e "\.po$" | awk '/^[?]/{print $2}')
  if [ "$NEW_FILES" != "" ]; then
    # Multiple args, don't quote.
    svn add $NEW_FILES
  fi
  unset NEW_FILES

  # Note, the Python part filters only for directories.
  # There may be a cleaner way to do this in shell.
  NEW_DIRS=$(svn status "$SVNDIR" | grep -v -e "\.po$" | awk '/^[?]/{print $2}' | python -c "import sys, os; sys.stdout.write('\n'.join([f for f in sys.stdin.read().split('\n') if os.path.isdir(f)]))")
  if [ "$NEW_DIRS" != "" ]; then
    # Multiple args, don't quote.
    svn add $NEW_DIRS
  fi
  unset NEW_DIRS
done

# Notify on redundant PO files
python3 tools_rst/rst_check_locale.py

# Print Commit message:
REVISION=$(svn info "$ROOTDIR" | grep '^Revision:' | sed -e 's/^Revision: //')
for SVNDIR in "$SVN_DIRS_ALL"; do
  echo " svn ci \"$SVNDIR\" -m \"Update r"$REVISION\"""
done
