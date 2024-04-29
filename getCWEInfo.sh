#!/bin/bash

#pre-clean and setup
echo "performing pre-clean and setup..."
rm -rf temp
rm -rf $1_results
rm -f *.xml *.dot
mkdir $1_results

#collect last 100 non-merge commits
python3 getCommits.py $1 > $1_results/$1.commits
#python3.9 getCommitsInfo.py $1

ver=0
cat $1_results/$1.commits | while IFS= read -r line; do
	
	#checkout commit
	python3 checkout.py $1 $line
	
	cp -r $1 $1_results/v${ver}
	ver=$((ver+1))
done

#run SATs on each version
collection=`ls -d $1_results/*/`
for file in ${collection};
do
	# Get the current working directory
	current_directory=${file}

	# Recursively find each directory in the current directory and create __init__.py in each, if it does not already exist
	find "$current_directory" -type d -exec bash -c 'if [ ! -f "$0/__init__.py" ]; then
		echo "Entering directory $0"
		touch "$0/__init__.py"
		echo "Created __init__.py in $0"
	else
		echo "__init__.py already exists in $0"
	fi' {} \;

	echo "executing pylint on [$file]..."
	pylint --disable missing-function-docstring ${file} > ${file}pylint.txt

done

rm -rf $1

