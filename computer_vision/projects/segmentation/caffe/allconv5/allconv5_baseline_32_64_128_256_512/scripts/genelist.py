# _*_ coding:utf8 _*_
import os
import sys
def listfiles(rootDir,txtfile):
    ftxtfile = open(txtfile,'w')
    list_dirs = os.walk(rootDir)
    count = 0
    dircount = 0
    for root, dirs, files in list_dirs:
        for d in dirs:
            print (os.path.join(root,d))
            dircount = dircount + 1
        for f in files:
            print (os.path.join(root,f))
            ftxtfile.write(os.path.join(root,f))
            filename = f.split('.')[0]
            filename = filename + "_mask.jpg"
            #print("filename", filename)
            rootPath = root.rsplit('/', 1)[0]
            #print("rootPath", rootPath)
            rootPath = rootPath + "/images_binary_mask"
            maskPath = os.path.join(rootPath,filename)
            #print("maskPath: ", maskPath)
            ftxtfile.write(" " + maskPath)
            ftxtfile.write('\n')
            count = count + 1
    print (rootDir+"  has  "+str(count)+"files")

if __name__ == '__main__':
    listfiles('../../../../../../datas/portrait/images_data','all.txt')

