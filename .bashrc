export PS1="\[\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\w\[\033[m\]\$ "
export CLICOLOR=1
export LSCOLORS=ExFxBxDxCxegedabagacad

export HOME_BIN=~/bin
export OLD_HOME_BIN=$HOME_BIN/old_bin
export LDFLAGS="-L/usr/local/opt/gettext/lib"
export CPPFLAGS="-I/usr/local/opt/gettext/include"
export GETTEXT="/usr/local/opt/gettext"
export CMAKE_HOME=/Applications/CMake.app/Contents
export CMAKE_BIN=$CMAKE_HOME/bin
export BLENDER_DOC=~/blender_docs
export BLENDER_MAN_EN=$BLENDER_DOC/
export BLENDER_MAN_VI=$BLENDER_DOC/locale/vi
export BLENDER_GITHUB=~/blender_manual
export BLENDER_GITHUB_MANUAL=$BLENDER_GITHUB/blender_docs
export LOCAL_BIN=$HOME/Library
export LOCAL_PYTHON=$LOCAL_BIN/Python
export LOCAL_PYTHON_3=/Library/Python/3.7/site-packages
export PATH=$GETTEXT/bin:$CMAKE_BIN:$HOME_BIN:$OLD_HOME_BIN:$LOCAL_BIN:$LOCAL_PYTHON_3/bin:$PATH
export PYTHONPATH=$LOCAL_PYTHON_3/lib

if [ -f ~/.aliasrc ]; then . ~/.aliasrc; fi
