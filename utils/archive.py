from icecream import ic


def archive_directory(archive_name: str, directory: str, base_dir: str = None, format='zip') -> str:
    import shutil

    # with tempfile.TemporaryDirectory() as temp_dir:
    #     subprocess.run(command, cwd=temp_dir)

    created_archive_loc = shutil.make_archive(
        archive_name, format, directory, base_dir, True,
    )

    ic(created_archive_loc)

    return created_archive_loc


def archive_in_mem():
    import io
    import zipfile

    # Create BytesIO object
    in_memory_zip = io.BytesIO()

    # Create a ZipFile object
    with zipfile.ZipFile(in_memory_zip, 'w') as zf:
        zf.writestr('file1.txt', 'This is content of file1')
        zf.writestr('file2.txt', 'This is content of file2')

    # Get data from BytesIO object
    data = in_memory_zip.getvalue()

    return zipfile


def zip_directory(directory):
    import io
    import zipfile
    import os

    # Create BytesIO object
    in_memory_zip = io.BytesIO()

    # Create a ZipFile object
    with zipfile.ZipFile(in_memory_zip, 'w') as zf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Create a file path
                file_path = os.path.join(root, file)

                # Add file to zip
                zf.write(
                    file_path, arcname=os.path.relpath(
                        file_path, directory,
                    ),
                )

    # Get data from BytesIO object
    data = in_memory_zip.getvalue()

    return data
