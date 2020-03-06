cat hoang_history.txt | awk '{ {printf "%04d", $1}; $1=""; print $0}' | sort > temp.txt; mv temp.txt hoang_history.txt
