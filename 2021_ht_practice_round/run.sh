for file in *.in ; do 
  echo $file
  /Users/zexuan/opt/anaconda3/bin/python s.py < $file > ${file%.in}.out
done
