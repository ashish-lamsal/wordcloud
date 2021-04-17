import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import utils
import click

@click.command()
@click.option("--in", "-i", "infile", required=True,
    help="Path to .txt file to be processed.",
    type=click.Path(exists=True, dir_okay=False, readable=True),
)
@click.option("--out", "-o", "outfile", default="./output.png",
    help="Path to .png file to store the wordcloud.",
    type=click.Path(dir_okay=False),
)
@click.option("--mask", "-m", default=None,
    help="Path to image file for masking.",
    type=click.Path(exists=True, dir_okay=False, readable=True),
)
def main(infile, outfile, mask):
    """ Processes the input file IN and stores the wordcloud to output file OUT.
    """
    input = read_file(infile)
    cloud = process_file(input, mask)
    write_image(cloud, outfile)


def read_file(file_path):
    with open(file_path, 'r') as infile:
        return infile.read()


def process_file(input, mask):
    
    # create dictionary of words from text file
    lines = utils.remove_punctuation(input)
    cleaned_words = utils.filter_text(lines)
    frequencies = utils.calculate_frequencies(cleaned_words)

    # mask for word cloud
    if mask:
        cloud_mask = np.array(Image.open(mask))
    else:
        cloud_mask = None
    # image_colors = ImageColorGenerator(cloud_mask)

    # generate image form word cloud
    cloud = WordCloud(width=1920, height=1080, background_color="white", mask=cloud_mask, contour_width=1, contour_color='black', colormap='Set2', collocations=False)
    cloud.generate_from_frequencies(frequencies)
    # cloud.recolor(color_func=image_colors)
    
    return cloud

def write_image(cloud, outfile):
    cloud.to_file(outfile)

# # Display your word cloud image
# utils.plot_cloud(cloud)

if __name__ =="__main__":
    main()