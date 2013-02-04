from PIL import Image
import argparse
import os
import imghdr
import shutil
import Tkinter


help_message = """
Searches a directory for images over a given size.

Usage:
    python find_desktops.py [OPTS]

Requires:
    PIL

Options:
    --path          Path to search on. Defaults to ./
    --min-width     Minimum width for images to be. Defaults to screen resolution
    --min-height    Minimum height for images to be. Defaults to screen resolution
    --copy-dir      Directory to copy desktops to. Default: ./DesktopsFound
    --orientation   Orientation to limit to (horizontal or vertical)
"""

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=help_message)
    parser.add_argument('--path', 
            help="Path to search for images",
            default="./"
        )

    parser.add_argument('--min-width',
            help="Minimum width for images",
            default=None
        )

    parser.add_argument('--min-height',
            help="Minimum height for images",
            default=None
        )

    parser.add_argument('--copy-dir',
            help="Directory to copy the images to. Uses ./DesktopsFound as a default",
            default="./DesktopsFound")

    parser.add_argument('--orientation',
            help="Desktop orientation, checks that the image is either horizontal or vertical",
            default="horizontal")

    args = parser.parse_args()

    if args.min_width is None and args.min_height is None:
        # If they don't specify the min height or width, we use Tkinter to make a guess:
        root = Tkinter.Tk()
        args.min_width = root.winfo_screenwidth()
        args.min_height = root.winfo_screenheight()
        orientation = "horizontal" if args.min_width > args.min_height else "vertical"

    print ""
    print "Searching for desktops on %s..." % args.path
    if not os.path.exists(args.path):
        print "ERROR: Source directory doesn't exist!"
        exit(1)

    print "Creating output directory %s..." % args.copy_dir
    if not os.path.exists(args.copy_dir):
        os.makedirs(args.copy_dir)

    found_images = 0
    found_desktops = 0
    files_scanned = 0

    if args.min_height:
        min_height = int(args.min_height)

    if args.min_width:
        min_width = int(args.min_width)

    for root, _, files in os.walk(args.path):
        for f in files:
            fullpath = os.path.join(root, f)
            files_scanned = files_scanned + 1
            if not imghdr.what(fullpath) == None:
                # Got an image that imghdr and PIL will understand. Let's get us some info!
                found_images = found_images + 1
                img = Image.open(fullpath)

                is_desktop = False
                img_width, img_height = img.size

                # First, check sizes:
                if args.min_width and args.min_height:
                    if img_height >= args.min_height and img_width >= args.min_width:
                        is_desktop = True
                elif args.min_width:
                    if img_width >= min_width:
                        is_desktop = True
                elif args.min_height:
                    if img_height >= args.min_height:
                        is_desktop = True


                # And now check orientation:
                if args.orientation == "horizontal":
                    if img_width < img_height:
                        is_desktop = False
                elif args.orientation == "vertical":
                    if img_height < img_width:
                        is_desktop = False

                # If we have an image, copy it!
                if is_desktop:
                    # To avoid filename conflicts, prepend the index of this file:
                    shutil.copy2(fullpath, os.path.join(args.copy_dir, str(found_desktops) + '-' + f))
                    found_desktops = found_desktops + 1
                    


    print "Scanned %d files, found %d images and, drumroll please..." % (files_scanned, found_images)
    print ""
    print "%d desktops! All files copied." % found_desktops
    print ""
    print "You have a wonderful day now"
    print ""
    exit(0)
    