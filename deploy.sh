cd _cv/ && git pull && cp cv.md ../cv.txt
cd ..
cat _prepend_front_matter.txt cv.txt > cv.md
rm cv.txt

git add -A
git commit -m "Automatic push"
git push origin master
