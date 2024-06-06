import os
import pandas as pd
import itertools

IMAGE_DIR = 'static/images'
image1 = []
image2 = []

images = [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if os.path.isfile(os.path.join(IMAGE_DIR, f))]
for pair in itertools.combinations(images, 2):
    image1.append(pair[0])
    image2.append(pair[1])

df = pd.DataFrame({'image1': image1, 'image2': image2, 'labelled': False, 'label': ''})

set_size = len(df) // 3

# Step 2: Split the DataFrame into three sets
set1 = df.iloc[:set_size]
set2 = df.iloc[set_size:set_size*2]
set3 = df.iloc[set_size*2:]

set1.to_csv('./sets/set1.csv', index = False)
set2.to_csv('./sets/set2.csv', index = False)
set3.to_csv('./sets/set3.csv', index = False)