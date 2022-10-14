import os


use_colorful_output=False


if use_colorful_output==True:
    TERMINAL_RED	='\033[31m'
    TERMINAL_GREEN	='\033[32m'
    TERMINAL_YELLOW	='\033[33m'
    TERMINAL_BLUE	='\033[34m'
    TERMINAL_RESET	='\033[0m'
else:
    TERMINAL_RED=''
    TERMINAL_GREEN=''
    TERMINAL_YELLOW=''
    TERMINAL_BLUE=''
    TERMINAL_RESET=''


# return (file_name, extension_name)
# function ver 0.2
def get_filename_and_extension_name(x:str):
    if os.path.isdir(x):
        return None
    for i in range(len(x)-1, 0, -1):
        if x[i]=='.':
            return (x[0:i], x[i+1:])
        if i==0:
            return (x[:], [])



print(f'{TERMINAL_BLUE}Qt Designer .ui -> Python .py AutoConvert Tool{TERMINAL_RESET}')
input(f'{TERMINAL_RED}This Will Cover All Of Your Modification!!!{TERMINAL_RESET}')
for i in os.listdir():
    if os.path.isfile(i):
        name,ext=get_filename_and_extension_name(i)
        if ext=='ui':
            cmd=f'pyuic5.exe "{i}" > "ui_{name}.py"'
            print(f'current command: {TERMINAL_YELLOW}{cmd}{TERMINAL_RESET}', flush=True)
            os.system(cmd)
print(f'{TERMINAL_GREEN}All Done!{TERMINAL_RESET}')
