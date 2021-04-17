import numpy as np
from PIL import Image, UnidentifiedImageError
from wordcloud import WordCloud
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
    cloud_mask = None 
    if mask:
        try:
            # resize the amsk image
            basewidth = 1920
            img = Image.open(mask)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)

            # generate arry of mask image
            cloud_mask = np.array(img)

        except UnidentifiedImageError:
            raise SystemExit(f"Error: cannot identify image file {mask}")

    # generate image form word cloud
    cloud = WordCloud(width=1920, height=1080, background_color="black", mask=cloud_mask, contour_width=1, contour_color='black', colormap='Set2', collocations=False)
    cloud.generate_from_frequencies(frequencies)
    
    return cloud

def write_image(cloud, outfile):
    cloud.to_file(outfile)


if __name__ =="__main__":
    main()