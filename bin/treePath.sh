#!/bin/bash -x
source=$1;
target=$2;

function getWord(){	
	string=$1;
	len=${#string};
	word="";
	for (( i=0; $i < $len; i++ )); do
		c=${string:$i:1};
		if [[ $c == '/' ]]; then
			if [[ -n $word ]]; then
				break;
			fi
			word=$c;
		else
			word="$word$c";
		fi
	done
	echo $word;
}

function relativeSource(){
	source=$1;
	src="";
	temp=$(echo $source | sed 's/[^\/]//g');
	len=${#temp};

	word=`getWord $source`;
	while [[ -n $word ]]; do
		if [[ -z $src ]]; then
			src="..";
		else
			src="../$src";
		fi
		source=${source##$word};
		word=`getWord $source`;
	done
	echo $src;
}

function relativeTarget(){
	target=$1;
	trg=$(echo $target | sed 's/^\///g');
	echo $trg;
}

function relativePath(){
	src=$1;
	trg=$2;
	i=0;

	len_src=${#src};	
	len_trg=${#trg};

	if [[ ( $len_src -eq 0 ) && ( $len_trg -gt 0 ) ]]; then
		path=$2;
	elif [[ $len_src -gt 0  && $len_trg -gt 0 ]]; then
		source_remainder=$src;
		target_remainder=$trg;
		s_word=`getWord $source_remainder`;
		t_word=`getWord $target_remainder`;
		while [[ $s_word == $t_word ]]; do
			source_remainder=${source_remainder##$s_word};
			target_remainder=${target_remainder##$t_word};		
			s_word=`getWord $source_remainder`;
			t_word=`getWord $target_remainder`;
		done
		if [[ $source_remainder == $src ]]; then #nothing changed, found nothing in common
			path=$trg;
		else
			src=`relativeSource $source_remainder`;
			trg=`relativeTarget $target_remainder`;	
			path=$src/$trg;	
		fi
	else
		path="";
	fi
	echo "Path=[$path]";
}


function commonPath(){

	local src=$1; #+ src=/home/hdt/basic_english_bible/old_t/proverbs
	local trg=$2; #+ trg=/home/hdt/basic_english_bible
	local result="";

	local src_tmp=$(echo $src | sed 's/\//;\//g' | sed 's/^;//');
	local trg_tmp=$(echo $trg | sed 's/\//;\//g' | sed 's/^;//');

	IFS=";";
	local src_arr=($src_tmp);
	local trg_arr=($trg_tmp);
	unset IFS;

	local trg_len=${#trg_arr[@]};
	local src_len=${#src_arr[@]};

	local len=$src_len;
	if [ $len -gt $trg_len ]; then 
		len=$trg_len;
	fi

	local common="";
	for (( i=0; $i < $len; i++ ));
	do
		local sword=${src_arr[$i]};
		local tword=${trg_arr[$i]};
		if [[ $sword == $tword ]]; then
			common="$common$sword";
		else
			break;
		fi
	done
	echo $common;
}

function newRelativePath(){
	local src=$1;
	local trg=$2;
	local relPath="";
	# get the common tree above if possible
	local common=$(commonPath "$src" "$trg");
	# get the length of the common part
	local common_len=${#common};

	# if no common part is found
	if [[ $common_len -eq 0 ]]; then 
		relPath=$trg;
	# if there is a common part
	else
		# trim the common part off
		local src_rem=${src#$common};
		local trg_rem=${trg#$common};		

		# the source part will be replaced with "../.."
		if [[ ! -z $src_rem ]]; then
			local src_tmp=$(echo $src_rem | sed 's/\//;\//g' | sed 's/^;//');
			IFS=";";
			local src_arr=($src_tmp);
			unset IFS;
			local src_len=${#src_arr[@]};
			for (( i=0; $i < $src_len; i++ )); do
				if [[ -z $relPath ]]; then
					relPath="..";
				else
					relPath="../$relPath";
				fi
			done
		fi
		if [[ $trg_rem == "/." || $trg_rem == "." ]]; then
			trg_rem="";
		fi
		relPath=$relPath$trg_rem;
	fi
	echo $relPath;
}

function escapeFilePath(){
	sourcePath=$1;
	sourcePath=$(echo $sourcePath | sed 's/\//\\\//g');
	sourcePath=$(echo $sourcePath | sed 's/\./\\\./g');
	echo $sourcePath;
}

#relativePath "$source" "$target";

newRelativePath "$source" "$target";


