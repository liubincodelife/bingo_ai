import sys
def splittrain_val(fileall,valratio=0.1):
    fileids = fileall.split('.')
    fileid = fileids[len(fileids)-2]
    print("fileid:", fileid)
    f=open(fileall);
    ftrain=open(fileid+"_shuffle_train.txt",'w');
    fval=open(fileid+"_shuffle_val.txt",'w');
    count = 0
    if valratio == 0 or valratio >= 1:
        valratio = 0.1
    
    interval = (int)(1.0 / valratio)
    while 1:
        line = f.readline()
        if line:
            count = count + 1
            if count % interval == 0:
                fval.write(line)
            else:
                ftrain.write(line)
        else:
            break

if __name__ == '__main__':
    splittrain_val("all.txt",0.1)
