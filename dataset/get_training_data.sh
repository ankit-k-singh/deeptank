# Render and Download Images of the tanks
python download_tank_images.py --output_dir ./tanks/

# Download some training videos consisting only of empty maps
# mkdir ../samples/backgrounds
# wget http://somewhere

# Extract backgrounds from said videos
python extract_backgrounds.py --input_dir ../samples/backgrounds --output_dir ./backgrounds/ --skip_start 15 --skip_end 15 --threshold 0.5

# Combine the tanks with the background data resulting in the final training data
python combine_tanks_backgrounds.py --tanks_dir ./tanks --backgrounds_dir ./backgrounds --output_dir ./training_data