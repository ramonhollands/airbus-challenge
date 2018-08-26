# Draft plan

# 1. Decode masks to rotated bounding boxes
From mark rle to rotated bounding boxes
TO be discussed: is this a good approach? Main reason, less outputs to learn and it enabled me to use lesson 8 and 9 from fastAi course.

# 2. Learn coordinates 1 ship
Create a CSV containing all pictures including 1 ship
Updated CoordTransform to enable augmentation for these bounding boxes
Learn with fastai 'default' settings

# 3. Implement lesson 9 for airbus dataset
And first submit to kaggle

# 4. Try and implement other ideas from lesson 10 onwards
