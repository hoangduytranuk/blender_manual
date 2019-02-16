#!/bin/bash
# Apache License, Version 2.0

# This script is to reduce tedious steps involved when updating PO files.
# It looks more complex then it really is, since we do multi-processing
# to update the PO files, to save some time.
# Last-Updater: Hoang Duy Tran <hoangduytran1960@googlemail.com>
# Last-Update-Date: 2018-11-18 17:51+0000
#

# Ensure we're in the repo's base:
function setBaseDirectory()
{
	BASEDIR=$(cd "$(dirname 0)"; pwd -P)
	if [ ! -e Makefile ]; then
		echo "The base [$BASEDIR] doesn't contain Makefile required. Terminate the process."
		exit 1
	else
		#echo "The base directory is: [$BASEDIR]"
		cd $BASEDIR
	fi
}

# Update the locale dir:
function updateLocaleDir()
{
	#Locate the SVN directory under locale.
	#It could be deeper than expected, depending on how the source has been checked out
	LOCALE_SVN_DIR=$(find ./locale -type d -name ".svn" -print)
	if [ -z $LOCALE_SVN_DIR ]; then
		echo "Unable to find SVN directory for ./locale"
		exit 1
	fi
	locale_dir=$(dirname $LOCALE_SVN_DIR)
	cd "$locale_dir"
	svn cleanup .
	svn up .
	cd -
}

# Create POT files:
function createPOTFiles()
{
	rm -rf build/locale
	make gettext
}

# Update PO files
#
# note, this can be slow so (multi-process)
function updatePOFiles()
{
	for lang in `find locale/ -maxdepth 1 -mindepth 1 -type d -not -iwholename '*.svn*' -printf '%f\n' | sort`; do
		sphinx-intl update -p build/locale -l $lang &
	done

	FAIL=0
	for job in `jobs -p`; do
		echo $job
		wait $job || let "FAIL+=1"
	done
	if [ "$FAIL" != "0" ]; then
		echo "Error updating"
		exit 1
	fi
	unset FAIL
}

# Add newly created PO files:
function svnAddPOFiles()
{
	cd $LOCALE_SVN_DIR
	NEW_FILES=`svn status . | grep -e "\.po$" | awk '/^[?]/{print $2}'`
	if [ "$NEW_FILES" != "" ]; then
		svn add $NEW_FILES
	fi
	unset NEW_FILES
}

# note, the Python part filters only for directories
# there may be a cleaner way to do this in shell.
function svnAddNewDirs()
{
	NEW_DIRS=`svn status . | grep -v -e "\.po$" | awk '/^[?]/{print $2}' | python -c "import sys, os; sys.stdout.write('\n'.join([f for f in sys.stdin.read().split('\n') if os.path.isdir(f)]))"`
	if [ "$NEW_DIRS" != "" ]; then
		svn add $NEW_DIRS
	fi
	unset NEW_DIRS
	cd -
}

# Notify on redundant PO files
function notifyRedundantPOFiles()
{
	python3 tools_rst/rst_check_locale.py
}

# Print Commit message:
function printCommitMessages()
{
	REVISION=`svn info . | grep '^Revision:' | sed -e 's/^Revision: //'`
	echo " cd locale; svn ci . -m \"Update r"$REVISION\""; cd .."
}

function performUpdatePO()
{
	setBaseDirectory
	updateLocaleDir
	createPOTFiles
	updatePOFiles
	svnAddPOFiles
	svnAddNewDirs
	notifyRedundantPOFiles
	printCommitMessages
}

# Python needs utf
export LANG="en_US.UTF8"

# Trap on the ERR pseudo signal
# http://stackoverflow.com/a/4384381/432509
err_trap () {
    errcode=$? # save the exit code as the first thing done in the trap function
	echo "  Error($errcode) on line ${BASH_LINENO[0]}, in command:"
    echo "  $BASH_COMMAND"
    exit $errcode
}
trap err_trap ERR
performUpdatePO
