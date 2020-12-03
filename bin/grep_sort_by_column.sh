grep 'isLinkPath:False' ~/log.log | sort -n | cut -d " " -f 3- > ~/found.log 

grep 'isLinkPath:False' ~/log.log | cut -d ' ' -f 3- | awk '{ print length($0) " " $0; }' | sort -r -n | cut -d ' ' -f 2-  > ~/found.log
grep 'isLinkPath:True' ~/log.log | cut -d ' ' -f 3- | awk '{ print length($0) " " $0; }' | sort -r -n | cut -d ' ' -f 2-  > ~/found.log