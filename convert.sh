# resize and crop files in batch

for file in *.JPG; do convert -enhance -contrast -gravity Center -crop 3500x2500+140+0 -resize '792x528^' $file $file; done

# resize ^ at end -> preserve aspect ratio
# -gravity Center -crop 1024x682+0+0 -> crop in middle
