import os
import queue

def normalize(infile, outfile):
    obj = ""
    q = queue.Queue()
    outfile = open(outfile, "w")
    cnt = 0
    with open(infile, "r") as f:
        while True:
            c = f.read(1)
            if not c:
                print("EOF")
                break
            elif c == "{":
                q.put(c)
            elif c == "}":
                q.get()
                if q.empty():
                    print("{}\tfinished queue...".format(cnt))
                    outfile.write(obj + c)
                    obj = ""
                    cnt += 1
                    continue
            else:
                obj += c
    print("FINISHED NORMALIZING")
