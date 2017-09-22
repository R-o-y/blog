import os
import shutil
import zipfile

from bs4 import BeautifulSoup


def extract_uploaded_zip_file_into_post_folder(zip_uploaded, post_folder_path):
    """
    :param zip_uploaded: the zip file uploaded using HTML form file input 
    :param post_folder_path: 
    """
    zip_on_disk_path = os.path.join(post_folder_path, 'upload.zip')
    zip_on_disk = open(zip_on_disk_path, 'wb+')
    for chunk in zip_uploaded.chunks():
        zip_on_disk.write(chunk)
    zip_on_disk.close()
    zip_file = zipfile.ZipFile(zip_on_disk_path, "r")
    zip_file.extractall(post_folder_path)
    zip_file.close()
    os.remove(zip_on_disk_path)


def remove_old_version_post_folder_on_disk_if_exists(post_folder_path):
    if os.path.isdir(post_folder_path):
        # if there has already been a folder containing the old version,
        # remove that entire folder (together with content inside) and create a new one
        shutil.rmtree(post_folder_path)


def get_raw_text(html_file_path):
    html = open(html_file_path, 'r')
    soup = BeautifulSoup(html, "html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def get_first_image_url(html_file_path):
    html = open(html_file_path, 'r')
    soup = BeautifulSoup(html, "html.parser")

    image = soup.find("img")
    if image is None:
        return None
    else:
        return image['src']
