"""
Download images from web page(s) and save them as .pdf or concatenate them into a single image
"""
from Downloader import Downloader, IGNORE, SAVE_PATH, URL_FILENAME
from io import BytesIO
from os import listdir
from os.path import basename, isdir, join 
from PIL.Image import Image, new, open as open_img
from time import perf_counter

CSS_SELECTOR: str = "img"
"""Pattern used to select `img` element(s) from HTML"""

EXTENSION: str = "jpg"
"""Image extension"""

IGNORE: list[str] = [ ]
"""List of filenames to ignore (i.e. won't save images containing these strings in their name)"""

IMG_MODE: str = "RGB"
"""Image mode"""

MIN_HEIGHT: int = 300
"""Minimum image height (i.e. only save images with heights greater than this value)"""

class ImageDownloader(Downloader):
    """
    Various methods to download images from web page(s), save images from web or directory as pdf,
    concatenate images into a single image, etc.
    """
    def __init__(self, save_path: str = SAVE_PATH, url_filename: str = URL_FILENAME):
        super().__init__(save_path, url_filename)

        # URL, image list cache
        self._cache: dict[str, list[Image]] = { }

    def _is_img(self, file_path: str) -> bool:
        """
        Checks if file is an image

        Args:
            file_path (str): Path of file to check

        Returns:
            bool: True if file is an image, else False
        """        
        try:
            with open_img(file_path) as img:
                img.verify()
                return True

        except: return False

    def _get_imgs(self, folder_path: str, mode: str = IMG_MODE) -> list[Image]:
        """
        Get all images in folder path

        Args:
            folder_path (str): Path of folder containing images
            mode (str, optional): Image mode (see `PIL.concept-modes`); defaults to IMG_MODE

        Returns:
            list[Image]: List of all images in folder
        """
        img_paths = [ ]

        for file_path in listdir(folder_path):
            img_abs_path = join(folder_path, file_path)
            if self._is_img(img_abs_path): img_paths.append(img_abs_path)

        # Sort by filename (i.e. ascending order) rather than by full path
        img_paths.sort(key = basename)
        
        return [ open_img(img).convert(mode) for img in img_paths ]

    def _download(self, img_url: str, mode: str = IMG_MODE) -> Image | None:
        """
        Save image

        Args:
            img_url (str): URL of image to download
            mode (str, optional): Image mode (see `PIL.concept-modes`); defaults to IMG_MODE
        """
        img_response = self._connect(img_url)
        
        if img_response and img_response.status_code == 200:
            with self.handle_download(img_url):
                img = open_img(BytesIO(img_response.content)).convert(mode)
                if img.height > MIN_HEIGHT: return img

        else: print(f"Skipping: Unable to get image at {img_url}\n")

    def generate_pdf(self, src: str | None = None, dest: str | None = None, save_name: str | None = None, combine: bool = False, mode: str = IMG_MODE) -> None:
        """
        Gets all images from directory and/or online pages and saves them into a single pdf
        Assumes images are to be saved in ascending order (i.e. ascending integer filenames)

        Args:
            src (str | None, optional): Path containing images to save to pdf; if None, images
            are downloaded online via provided URLs in urls.txt
            save_name (str | None, optional): New pdf's name; defaults to randomly generated name if None
            combine (bool, optional): Whether to combine all images into single pdf or
            save separately as multiple pdfs; defaults to False
            mode (str, optional): Image mode (see `PIL.concept-modes`); defaults to IMG_MODE
        """
        self._generator(src, dest, save_name, combine, "pdf", mode)

    def stack_imgs(self, src: str | None = None, dest: str | None = None, save_name: str | None = None, combine: bool = False, ext: str = EXTENSION, mode: str = IMG_MODE) -> None:
        """
        Stack and save vertical strip of images (i.e. like a webcomic)

        Args:
            src (str | None, optional): Path containing images to stack; if None, images
            dest (str | None, optional): New image stack's save path; defaults to save path in constructor, if None
            save_name (str | None, optional): New stacked image's name; defaults to folder name, if None
            combine (bool, optional): Whether to combine all images into single image or save separately; defaults to False
            ext (str, optional): Image extension (e.g. jpeg, png, etc.) to specify format; defaults to EXTENSION
            mode (str, optional): Image mode (see `PIL.concept-modes`); defaults to IMG_MODE
        """
        self._generator(src, dest, save_name, combine, ext, mode)

    def _generator(self, src: str | None = None, dest: str | None = None, save_name: str | None = None, combine: bool = False, ext: str = EXTENSION, mode: str = IMG_MODE) -> None:
        """
        Base file generator

        Args:
            src (str | None, optional): Path containing images; defaults to images, if None
            dest (str | None, optional): New file's save path; defaults to save path in constructor, if None
            save_name (str | None, optional): New file's name; defaults to folder name, if None
            combine (bool, optional): Whether to combine all images into single file or save separately; defaults to False
            ext (str, optional): Image extension (e.g. jpeg, png, pdf, etc.) to specify format; defaults to EXTENSION
            mode (str, optional): Image mode (see `PIL.concept-modes`); defaults to IMG_MODE
        """
        try:
            if not dest: dest = self._save_path
            images = self._get_imgs(src, mode) if src and isdir(src) else [ ]
            self.run(images = images, dest = dest, save_name = save_name, combine = combine, ext = ext, mode = mode)            

        except Exception as error:
            print(f"Unexpected error during {ext} file generation ({error})\n")        

    def _run(self, url: str, **kwargs) -> None:
        """
        Run script

        Args:
            url (str): URL containing images to download
        """
        if url not in self._cache:
            new_imgs = self._cache[url] = self.work(url, CSS_SELECTOR, "", IGNORE)

        else: new_imgs = self._cache[url]

        combine = False
        images = [ ]
        save_name = None
        dest = self._save_path
        ext = EXTENSION
        mode = IMG_MODE
        
        for name, value in kwargs.items():
            if images and save_name and combine and ext and mode and dest: break
            elif name == "combine": combine = value
            elif name == "images": images = value
            elif name == "save_name": save_name = value
            elif name == "ext" != EXTENSION: ext = value
            elif name == "mode" != IMG_MODE: mode = value
            elif name == "dest": dest = value

        if not save_name: save_name = self._random_filename(ext, save_name)

        if combine: images.extend(new_imgs)

        else:
            self._save_pdf(new_imgs, dest, save_name) if ext.endswith("pdf") else self._save_imgs(new_imgs, dest, save_name, mode)

        if images:
            self._save_pdf(images, dest, save_name) if ext.endswith("pdf") else self._save_imgs(images, dest, save_name, mode)
                                
    def _save_pdf(self, images: list[Image], dest: str, save_name: str) -> None:
        """
        Combine images into pdf and save

        Args:
            images (list[Image]): Images to combine into pdf
            dest (str): New file's save path
            save_name (str): New pdf's name
        """
        if images and len(images) > 0:
            abs_save_path = join(dest, save_name)
            
            if len(images) == 1: images[0].save(abs_save_path)
            else: images[0].save(abs_save_path, save_all = True, append_images = images[1:])

            print(f"Successfully saved {save_name} to {dest}\n")

        else: print(f"Error: Cannot save empty pdf\n")

    def _save_imgs(self, imgs: list[Image], dest: str, save_name: str, mode: str = IMG_MODE) -> None:
        """
        Stack images into single image and save

        Args:
            imgs (list[Image]): Images to combine
            dest (str): New file's save path
            save_name (str): New image's name
            mode (str, optional): Image mode (see `PIL.concept-modes`); defaults to IMG_MODE
        """
        if imgs and len(imgs) > 0:
            min_width = min(img.width for img in imgs)
            resized_imgs = [ img.resize((min_width, int(img.height * min_width / img.width))) for img in imgs ]
            total_height = sum(img.height for img in resized_imgs)
            final_img, y = new(mode, (min_width, total_height)), 0

            for img in resized_imgs:
                final_img.paste(img, (0, y))
                y += img.height

            abs_save_path = join(dest, save_name)
            
            final_img.save(abs_save_path)

            print(f"Successfully saved {save_name} to {dest}\n")

        else: print(f"Error: Cannot stack empty images\n")

if __name__ == "__main__":
    # START
    print(f"Starting script...\n")
    start = perf_counter()

    # RUN
    img = ImageDownloader()
    img.generate_pdf()
    img.stack_imgs()

    # END
    end = perf_counter()
    print(f"Total runtime: {(end - start):.2f} second(s)")
    exit(0)