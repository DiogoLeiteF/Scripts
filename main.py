import os


def clean_duplicates():
    directory = input('input folder directory: ')
    if os.path.exists(directory):
        video_dir = os.listdir(directory)
        print(f'''You are in: 
{directory}

The current folder contains {len(video_dir)} files:\n ''')
        see_files = input('Do you want to list the files: y/n: ')
        if see_files.lower() == 'y':
            for file in video_dir:
                print('=>', file)

        rigth_dir = input('\nIs this the correct directory? \ntype y or n:  ')
        if rigth_dir.lower() == 'y':
            delete_list = []
            for file in video_dir:
                if 'Cópia' in file:
                    w = file.replace(' - Cópia', '', 1)
                    if w in video_dir:
                        delete_list.append(file)

                elif '(1)' in file:
                    y = file.replace('(1)', '')
                    if y in video_dir:
                        delete_list.append(file)

                elif '(2)' in file:
                    x = file.replace('(2)', '')
                    if x in video_dir:
                        delete_list.append(file)

            print(f'\n_______File to be deleted:______ \n')
            for file in delete_list:
                print('>>>', file)
            print(f'\n {len(delete_list)} Files to be deleted\n ')

            auth = input('\nMay we proced? y/n ')

            if auth.lower() == 'y':
                for file in delete_list:
                    os.remove(f'{directory}/{file}')
            for file in os.listdir(directory):
                print('=>', file)
            print(
                f'''__________DONE___________
 {len(os.listdir(directory))} files remaining
 The remaining file in directory are:
''')

        elif rigth_dir.lower() == 'n':
            clean_duplicates()
        else:
            print('wrong input, try again\n')

    else:
        print('path does not exists')
        clean_duplicates()


if __name__ == '__main__':
    clean_duplicates()
