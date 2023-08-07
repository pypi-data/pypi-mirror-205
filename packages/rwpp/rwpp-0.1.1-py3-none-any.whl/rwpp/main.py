import inspect
import os

import redditwarp.SYNC
import requests
import typer
from redditwarp.models.submission_SYNC import LinkPost

app = typer.Typer()


#  Main download function
# @app.command()
def download(subreddit, limit, download_path, time=None, sort_by=None):
    # Check for download path
    if not os.path.isdir(f"{download_path}/{subreddit}"):
        os.makedirs(f"{download_path}/{subreddit}")

    downloaded_images = os.listdir(f"{download_path}/{subreddit}")

    accepted_formats = [".jpg", ".jpeg", ".png"]

    if sort_by:
        client = redditwarp.SYNC.Client()
        method = getattr(client.p.subreddit.pull, sort_by)
        if time and callable(getattr(method, '__call__')) and len(inspect.signature(method).parameters) == 2:
            # The method doesn't accept any parameters, so don't pass `time`
            raise ValueError(
                f"Method '{sort_by}' doesn't accept any parameters.")
        elif time:
            # The method accepts a `time` parameter, so pass it
            posts = method(subreddit, amount=limit, time=time)
        else:
            # The method doesn't accept a `time` parameter, so call it without the `time` argument
            posts = method(subreddit, amount=limit)
    else:
        raise ValueError("sort_by parameter is missing or invalid.")

    for post in posts:
        if not isinstance(post, LinkPost):
            continue
        if post.link.split("/")[-1] not in downloaded_images:
            if post.link.endswith(tuple(accepted_formats)):

                # Retrive the image
                r = requests.get(post.link)

                # Save image to file
                with open(
                    f"{download_path}/{subreddit}/{post.link.split('/')[-1]}", "wb"
                ) as f:
                    f.write(r.content)

                typer.echo(f"{post.link} saved to file")

            else:
                typer.echo("URL does not contain a valid image format...")

        else:
            typer.echo("Image already downloaded...")


# @app.callback()
def main(
    subreddit: str = typer.Argument(
        ...,
        help="The given subreddit(s) to pull images from"
    ),
    limit: int = typer.Option(
        10,
        help="The amount of posts to pull from subreddit(s)",
        prompt="How many images would you like to download? "
    ),
    download_path: str = typer.Option(
        "./downloads",
        help="The path where you would like to save images",
        prompt="Where would you like to save the images? "
    ),
    sort_by: str = typer.Option(
        "hot",
        help="The sort order to pull images by",
        prompt="Sort order for images?: [hot, new, top, rising] "
    ),
    time: str = typer.Option(
        "",
        help="The time period to pull images from, only needed for top posts",
        prompt="Time period for images? (Only needed for top posts): [hour, day, week, month, year, all] "
    )
):
    download(subreddit, limit, download_path, time, sort_by)


# Main function to be called from terminal
@app.callback()
def cli():
    typer.run(main)


# For when the file is called explicitly like during development
if __name__ == "__main__":
    typer.run(main)
