import os

def Output(content,filename):
    if(os.path.isfile(filename)):
        os.remove(filename)

    with open(filename, "a") as f:
                        print(content,file=f)