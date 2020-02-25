#echo 'This is HOANG Duy Tran'
pman() {
	man -t ${@} | open -f -a Preview
}
if [ -f ~/.bashrc ]; then . ~/.bashrc; fi

