#!/usr/bin/env python3

import sh
import sys
import os
import typer
import math
import tempfile
import zipfile
from typing import List, Optional

from PIL import Image
from humanfriendly import format_size

from .log import logger, Verbosity
from .packer import pack_files_to_png, pack_files_within_streams

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

APP_NAME = "polygone"
app = typer.Typer(
    name=APP_NAME,
    help=f"{APP_NAME}: polyglot file generator",
    no_args_is_help=True,
    context_settings=CONTEXT_SETTINGS,
)


@app.command(help="Embed data into a PNG file")
def pack(
    cover_f: str = typer.Argument(..., help="PNG file to use as cover"),
    content_f: str = typer.Argument(..., help="File containing data to embed"),
    output_file: str = typer.Argument(..., help="Output file"),
    should_zip: bool = typer.Option(
        False, "--zip", "-z", help="Zip the content file before embedding"
    ),
    zip_level: int = typer.Option(
        5,
        "--zip-level",
        "-l",
        help="Compression level to use when zipping the content file",
    ),
):
    logger.info(f"checking cover: {cover_f}")

    with open(cover_f, "rb") as output_f:
        cover_data = output_f.read()

    cover_image = Image.open(cover_f)

    if cover_image.format != "PNG":
        logger.error("  cover image is not a PNG")
        raise typer.Exit(1)

    if should_zip:
        tmp = tempfile.NamedTemporaryFile(suffix=".zip")
        logger.info(f"  zipping content file: {content_f} -> {tmp.name}")
        # compress using zipfile deflate, medium compression
        with zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED, zip_level) as zipf:
            zipf.write(content_f, os.path.basename(content_f))
        content_f = tmp.name

    # get size of content file on disk
    content_file_size = os.path.getsize(content_f)

    # get size of cover image on disk
    cover_file_size = os.path.getsize(cover_f)

    # check dimensions, ensure they are large enough to embed the content
    cover_width, cover_height = cover_image.size
    logger.info(f"  cover image size: {cover_width}x{cover_height}")

    cover_pixel_count = cover_width * cover_height

    cover_remaining_budget = cover_pixel_count - cover_file_size
    cover_can_fit_content = cover_file_size < cover_remaining_budget

    if not cover_can_fit_content:
        logger.error("  cover image is too small to embed the content")
        logger.error(
            f"    failed condition: {cover_file_size} < {cover_remaining_budget} ({cover_pixel_count} - {content_file_size})"
        )
        logger.info(
            f"    hint: try using a larger cover image, or compressing the content file"
        )
        raise typer.Exit(1)

    logger.info(f"packing: {cover_f} + {content_f} -> {output_file}")

    with open(output_file, "wb") as output_f:
        cover_f = open(cover_f, "rb")
        content_f = open(content_f, "rb")

        pack_files_within_streams(cover_f, content_f, output_f)

        cover_f.close()
        content_f.close()

    # check the output file
    output_file_size = os.path.getsize(output_file)

    logger.info("packing complete")
    # logger.info(f"  output size: {output_file_size}")
    # logger.trace(
    #     f"  packed {cover_file_size} (cover) + {content_file_size} (content) -> {output_file_size} (output)"
    # )
    logger.info(
        f"  packed {format_size(cover_file_size)} (cover) + {format_size(content_file_size)} (content)"
        f" -> {format_size(output_file_size)} (output)"
    )


@app.callback()
def app_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Quiet output"),
):
    if verbose:
        logger.be_verbose()
    elif quiet:
        logger.be_quiet()


def main():
    app()
