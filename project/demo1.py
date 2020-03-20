import sys
import time
import traceback
def print_(f):
    try:
        assert f in ["dai", "ji"]
        print(f)
    except AssertionError as e:
        traceback.print_exc()
    print("ok")

def demo(size):
    for i in range(size):
        sys.stdout.write('\r>> Converting image %d shard' % (i+1))
        sys.stdout.flush()
        time.sleep(1)



if __name__ == '__main__':

    demo(220)
