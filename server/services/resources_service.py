import os
from datetime import datetime
from flask_login import current_user



def save_file_locally(file, requirement, user_id):
    """
    :param file: the document who will scan / the documents the user sent
    :param requirement: the current requirement / the requirement of this document
    :return: the path who the file saved at
    """
    if not user_id:
        user_id = current_user.get_id()
    file_type = f".{file.content_type[file.content_type.index('/') + 1:]}"
    relative_path: str = "Uploaded files"  # The directory in which the files will be stored
    dt_string = datetime.now().strftime("%d_%m_%Y %H_%M_%S")
    folder = relative_path + "//" + str(user_id)
    file_path = f"{folder}/{requirement} {dt_string}{file_type}"
    file_path = os.path.abspath(file_path)

    """
    print("please make sure that this path exist on your computer:")
    print(os.path.abspath(relative_path))
    print("The file will be saved in folder: " ,os.path.abspath(folder))
    """

    if not os.path.exists(os.path.abspath(folder)):
        os.mkdir(folder)
    file.save(file_path)
    # file_path = os.path.abspath(file_path)
    return file_path


async def remove_file_locally(file_path):
    pass


async def save_files_in_db(files_paths, submit_id):
    pass


def remove_file(file_path):
    os.remove(file_path)  # delete document file
