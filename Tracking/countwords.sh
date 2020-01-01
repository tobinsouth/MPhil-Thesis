

# Find all tex files
find ../ -name "*.tex" -maxdepth 4 > all_tex_files.out

# To find number of latex words
# example: detex document.tex | wc -w

# Find all word counts and add to file
truncate -s 0 word_counts.out
while read file; do
	echo $file >> word_counts.out 
	detex "$file" | wc -w >> word_counts.out 
done < all_tex_files.out


# Find all raw counts and add to file
truncate -s 0 latex_counts.out
while read file; do
	wc -w $file >> latex_counts.out
done < all_tex_files.out

# Save using python script
python save_word_counts.py


