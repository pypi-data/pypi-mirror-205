import click
import os
import re as regex
import subprocess
from ext_pathlib import Path, PurePath
from natsort import natsorted
from PIL import Image, ImageFile, ExifTags
from pillow_heif import register_heif_opener

register_heif_opener()


def rotation_fix(im: Image.Image) -> Image.Image:
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == "Orientation":
            break

    try:
        exif = im._getexif()

        if exif[orientation] == 3:
            im = im.rotate(180, expand=True)
        elif exif[orientation] == 6:
            im = im.rotate(270, expand=True)
        elif exif[orientation] == 8:
            im = im.rotate(90, expand=True)

    except (AttributeError, KeyError, TypeError):
        # No EXIF tags
        return im

    return im


class ImageConv(object):
    def __init__(
        self,
        iview_exe: str | PurePath = r"C:\Program Files\IrfanView\i_view64.exe",
        ini_file: str | PurePath = "",
    ) -> None:
        self.iview_exe = Path(iview_exe)
        self.ini_file = Path(ini_file)
        self._image_extensions: tuple = ("*.jpg", "*.jpeg", "*.png")
        self._odd_extensions: tuple = ("*.webp", "*.heic")
        self._all_extensions: tuple = self._image_extensions + self._odd_extensions

    def get_pics(self, path: str | PurePath = ".") -> list[PurePath]:
        """Searchs a folder for all image files with the extensions .jpg, .jpeg, and .png. Returning a list of pathlib objects"""
        return natsorted(Path(path).scan(self._all_extensions), key=lambda x: x.name)

    def PIL_conv(self, fl, quality=50, load_truncated: bool = False) -> PurePath | None:
        """Uses PIL (Python Imaging Library) to convert and compress an image.
        Output will be a jpeg file set at 50% quality, and if the resolution is high enough,
        it will resize it with the minimum dimension is 1280, while preserving aspect ratio.
        Function will return nothing and not convert an image if the a file matching the converted filename exists.
        If it does conver the image, a pathlib object of the converted image will be returned."""
        fl = Path(fl)
        out_file = Path(fl.parent, f"{fl.stem}_conv.jpg")

        if out_file.exists():
            return

        ImageFile.LOAD_TRUNCATED_IMAGES = load_truncated
        register_heif_opener()

        img = Image.open(fl)
        img = rotation_fix(im=img)
        img = img.convert("RGB")

        in_wh = img.size
        minimum = min(in_wh)
        ratio_wh = in_wh[0] / in_wh[1]
        ratio_hw = in_wh[1] / in_wh[0]
        if in_wh.index(minimum) == 0:
            res = (1280, int(1280 * ratio_hw))
        else:
            res = (int(1280 * ratio_wh), 1280)

        if minimum > 1280:
            img_out = img.resize(res, Image.ANTIALIAS)
        else:
            img_out = img

        img_out.save(out_file, "JPEG", quality=quality)
        return out_file

    def irf_conv(self, img_in: str | PurePath) -> PurePath | None:
        """Uses IrfanView to convert and compress an image.
        Output will be a jpg, with the specific settings based on the ini file provided in the __init__.
        Function will return nothing and not convert an image if the a file matching the converted filename exists.
        If it does conver the image, a pathlib object of the converted image will be returned."""
        img_in = Path(img_in)
        img_out = Path(img_in.parent, f"{img_in.stem}_conv.jpg")
        if img_out.exists():
            return

        cmd = f'"{self.iview_exe}" "{img_in}" /advancedbatch="{self.ini_file}" /silent /convert="{img_out}"'
        subprocess.run(cmd, shell=True)
        return img_out

    def convert_list(
        self,
        img_list: list[PurePath],
        convert_method: str = "pil",
        size_thres: int = 256,
        quality: int = 50,
        quiet: bool = False,
        load_truncated: bool = False,
    ) -> None:
        """Iterate over the img_list, using the selected conversion method and quality, to convert all images under the size threshold."""
        for file in img_list:
            if regex.search("_conv", file.stem, regex.I):
                continue
            if file.kb() > size_thres or file.suffix.lower() in (".webp", ".heic"):
                try:
                    if convert_method.lower() == "irf":
                        if not self.ini_file.is_file():
                            raise Exception("No ini file provided, stopping.")
                        out = self.irf_conv(file)
                    else:
                        out = self.PIL_conv(
                            file, quality=quality, load_truncated=load_truncated
                        )
                        if not out:
                            continue
                        atime, mtime = file.getatime(), file.getmtime()
                        os.utime(out, (atime, mtime))
                except Exception as e:
                    if not quiet:
                        print(f"Error on file: {file.name}")
                    raise e
                if out:
                    if not quiet:
                        print(
                            f"In: {file.kb():>5}kb, Out: {out.kb():>4}kb | {file.name}"
                        )

    def move_images(self, img_list: list[PurePath], quiet: bool = False) -> None:
        """Move's the original files of those converted to a new directory inside the image's folder named \"OG's\"."""
        bsize, asize, count = 0, 0, 0
        for conv in img_list:
            if regex.search("_conv", conv.stem, regex.I):
                fn = regex.sub("_conv", "", conv.stem, regex.I)
                og_jpeg = Path(conv.parent, f"{fn}.jpeg")
                og_jpg = Path(conv.parent, f"{fn}.jpg")
                og_png = Path(conv.parent, f"{fn}.png")
                og_webp = Path(conv.parent, f"{fn}.webp")
                og_heic = Path(conv.parent, f"{fn}.heic")
                og_pic = ""

                for f in [og_jpeg, og_jpg, og_png, og_webp, og_heic]:
                    if f.exists():
                        og_pic = f
                        break

                if not og_pic:
                    continue

                bsize += og_pic.kb()
                asize += conv.kb()
                count += 1
                dest = Path(conv.parent, "OG's", og_pic.name)
                try:
                    og_pic.move(dest)
                except FileNotFoundError:
                    pass

        try:
            if not quiet:
                print(
                    f"{count:> 3} Files | Before: {bsize/1024:.2f}MB, After: {asize/1024:.2f}MB | {asize/bsize:.2%}"
                )
        except ZeroDivisionError:
            if not quiet:
                print("No files to move, continuing.")

    def clean_dir(self, path: PurePath, preserve_root: bool = False) -> None:
        """BE CAREFUL! THIS WILL DELETE FILES WITHOUT CHECKING!
        Used to delete all files and subfolders in the provided directory, and optionally the provided directory itself."""
        if isinstance(path, str):
            path = Path(path)
        files = [x for x in path.scanr(self._all_extensions) if x.is_file()]
        folders = [x for x in path.scanr("*") if x.is_dir()]
        folders = sorted(folders, key=lambda x: len(x.parents), reverse=True)
        for file in files:
            file.unlink()
        for folder in folders:
            folder.rmdir()
        if not preserve_root:
            path.rmdir()

    def batch_convert(
        self,
        path: str | PurePath = ".",
        convert_method: str = "pil",
        size_thres: int = 256,
        quality: int = 50,
        clean_up: bool = True,
        no_ask: bool = False,
        quiet: bool = False,
        load_truncated: bool = False,
    ) -> None:
        """Scan all images inside the provided path, and convert all within the size threshold and compresses them."""
        img_list = self.get_pics(path=path)
        self.convert_list(
            img_list=img_list,
            convert_method=convert_method,
            size_thres=size_thres,
            quality=quality,
            quiet=quiet,
            load_truncated=load_truncated,
        )

        if not no_ask:
            input("Press [enter] to move files.")

        img_list = self.get_pics(path=path)
        self.move_images(img_list=img_list, quiet=quiet)

        if not no_ask:
            clean = input(
                "Type 'y' to delete OG's folder, type 'n' or nothing to preserve it: "
            )
            if regex.search("^\s*y\s*$", clean, regex.I):
                clean_up = True
            else:
                clean_up = False

        if clean_up:
            og_dir = Path(path, "OG's")
            if og_dir.exists():
                self.clean_dir(path=og_dir, preserve_root=False)

        if not no_ask:
            input("Press [enter] to close window.")

    def extension_fixer(self, path: str | PurePath = ".", quiet: bool = False) -> None:
        self.format_extensions = {
            v: k for k, v in Image.registered_extensions().items()
        }
        self.format_extensions["JPEG"] = ".jpg"
        self.format_extensions["PNG"] = ".png"

        img_list = self.get_pics(path=path)
        for file in img_list:
            suffix = file.suffix.lower()
            with Image.open(file) as im:
                fmt = im.format

            proper_ext = self.format_extensions[fmt]
            if suffix != proper_ext:
                out = Path(file.parent, f"{file.stem}{proper_ext}")
                file.move2(out)
                if not quiet:
                    print(f"{out.name}: {suffix[1:]} -> {proper_ext[1:]}")


@click.command()
@click.argument("path", nargs=-1)
@click.option("-ini", "--ini_file", "ini_file", type=str)
@click.option("-c", "--convert_method", "convert_method", type=str)
@click.option("-s", "--size_thres", "size_thres", type=int)
@click.option("-q", "--quality", "quality", type=int)
@click.option("-clean", "--clean_up", "clean_up", is_flag=True)
@click.option("-na", "--no_ask", "no_ask", is_flag=True)
@click.option("-quiet", "--quiet", "quiet", is_flag=True)
def cli_imageconv(
    ini_file: str | PurePath = "",
    path: str | PurePath = ".",
    convert_method: str = "pil",
    size_thres: int = 256,
    quality: int = 50,
    clean_up: bool = True,
    no_ask: bool = False,
    quiet: bool = False,
) -> None:
    if ini_file:
        imgconv = ImageConv(ini_file=ini_file)
    else:
        imgconv = ImageConv()
    path = "." if not path else path[0]
    imgconv.batch_convert(
        path=path,
        convert_method=convert_method,
        size_thres=size_thres,
        quality=quality,
        clean_up=clean_up,
        no_ask=no_ask,
        quiet=quiet,
    )
    pass


if __name__ == "__main__":
    # iview_exe = Path(r"C:\Program Files\IrfanView\i_view64.exe")
    # config_ini = Path(r"C:\Users\Matt\Documents\irf_resize if and smart crop.ini")
    # imgconv = ImageConv(ini_file=config_ini)
    # imgconv.batch_convert(
    #     path=".",
    #     convert_method="pil",
    #     size_thres=256,
    #     quality=50,
    #     clean_up=False,
    #     no_ask=False,
    #     quiet=False,
    # )
    cli_imageconv()
    pass
