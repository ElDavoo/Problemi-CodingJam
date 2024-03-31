E = 17459243613
N = 66624478857659
Cs = [35784176028369,
        63561241316534,
        40946911928892,
        56405696498538,
        38978109180990,
        16444276162313,
        38053979586003,
        57562671757853]
w = 1825
x = 3338
y = 2866
z = 3816
import threading
import os
#M=xy-1
#e=wM+x
#d=zM+y
#n= (ed-1) / M

#e=w(xy-1)+x = wxy-w+x


def main():
    d = z * (x * y - 1) + y
    for c in Cs:
        r = c * d % N
        rr = r.to_bytes((r.bit_length() + 7) // 8, 'big').hex()
        print(bytes.fromhex(rr).decode('utf-8'))


def brute_z():
    for z in range(1024,4097):
        d = z*(x*y-1) + y
        r = Cs[0]*d % N
        rr = r.to_bytes((r.bit_length() + 7) // 8, 'big').hex()
        try:
            print(bytes.fromhex(rr).decode('utf-8'))
            print(z)

        except UnicodeDecodeError:
            pass


def brute(b,e):
    # first bruteforce version, single thread
    for w in range(b,e):
        if w % 100 == 0 :
            print(f'w={w}')
        for x in range(1024,4097):
            for y in range(1024,4097):

                if w*((x*y)-1) + x == E:
                    print(f'w={w}, x={x}, y={y}')
                    return 0

def brute_mt():
    threads = []
    num_cpus = os.cpu_count()
    for i in range(num_cpus):
        # Split the range (1024,4097) in num_cpus parts
        b = 1024 + (3072 // num_cpus) * i
        e = 1024 + (3072 // num_cpus) * (i + 1)
        threads.append(threading.Thread(target=main, args=(b,e)))
        threads[i].start()
    for i in range(num_cpus):
        threads[i].join()


if __name__ == '__main__':
    # step 1: find w,x,y with bruteforce
    # this takes a few minutes
    #brute_mt()
    # step 2: find z, just printing the decrypted msg for each z
    # and take the first z for which decrypted makes sense
    # brute_z()
    # step 3: decrypt
    main()
