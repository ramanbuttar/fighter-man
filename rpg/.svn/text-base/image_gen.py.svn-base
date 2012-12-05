# import imaging modules
import Image, ImageDraw

# import db modules
from model import Fighter, Equipment

# import os methods
import os

def paste_object( img_dst, object ):
  """paste a png to an 'Image' file
  Image  img_dst  - image to paste on
         object   - object to paste onto image (ie.glove)
  """

  # attempt to paste png on destination image

  if object:
    try:
      img_src = Image.open( object.filename )
      img_dst.paste( img_src, (object.offset_x, object.offset_y), img_src )
    except:
      print 'paste_object error: %s' % (object.filename)
  else:
    print 'paste_object error: object = None'

def update_fighter_image( fighter ):
  """Create a profile image for the boxer based on their appearance attributes"""

  # create a new image -- size (250,600)
  img_output = Image.new("RGBA", (250,600), None)

  paste_object( img_output, fighter.body )
  paste_object( img_output, fighter.eyes )
  paste_object( img_output, fighter.hair )
  paste_object( img_output, fighter.mouth )
  paste_object( img_output, fighter.face )
  paste_object( img_output, fighter.trunks )
  paste_object( img_output, fighter.gloves )
  paste_object( img_output, fighter.boots )

  # save to file
  path = 'rpg/static/images/fighters/' + fighter.name + '.png'
  path_sml = 'rpg/static/images/fighters/' + fighter.name + '_sml.png'
  path_med = 'rpg/static/images/fighters/' + fighter.name + '_med.png'
  
  try:
    os.remove( path )
    os.remove( path_sml )
    os.remove( path_med )
  except:
    # no file exists anyways
    print 'no file exists yet'

  # save large image
  img_output.save( path, "PNG" )

  # resize, medium image (70%)
  img_output_med = img_output.resize( (175,420), Image.ANTIALIAS)
  # save small image
  img_output_med.save( path_med, "PNG" )

  # resize, small image (40%)
  img_output_sml = img_output.resize( (100,240), Image.ANTIALIAS)
  # save small image
  img_output_sml.save( path_sml, "PNG" )

