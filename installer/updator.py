import requests
import os
import zipfile
import shutil

# 現在のバージョン
current_version = '1.0.0'

# リポジトリのURL
repo_url = 'https://github.com/username/repo'

def check_for_update():
    response = requests.get(f'{repo_url}/latest_version.txt')
    latest_version = response.text.strip()

    if latest_version > current_version:
        return latest_version

    return None

def download_and_install_update(version):
    response = requests.get(f'{repo_url}/releases/download/v{version}/update.zip')

    with open('update.zip', 'wb') as f:
        f.write(response.content)

    with zipfile.ZipFile('update.zip', 'r') as zip_ref:
        zip_ref.extractall('update')

    shutil.rmtree('your_project_directory')
    shutil.move('update', 'your_project_directory')

    os.remove('update.zip')

def main():
    print(f'Checking for update...')
    new_version = check_for_update()

    if new_version:
        print(f'New version {new_version} found. Updating...')
        download_and_install_update(new_version)
        print(f'Update completed.')
    else:
        print(f'No new updates found.')

if __name__ == '__main__':
    main()