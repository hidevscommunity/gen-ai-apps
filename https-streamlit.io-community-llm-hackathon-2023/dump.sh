# bash script to dump out the git objects into a zip file for importing to clarifai
mkdir data
for x in `git rev-list --objects -g --no-walk --all | cut -b1-40`;
do echo $x;
   git show -p $x > data/$x.txt;
done
git log --all --patch  $x > data/all.log;
zip data.zip data/*
