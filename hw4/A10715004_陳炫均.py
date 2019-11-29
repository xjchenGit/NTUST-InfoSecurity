import random, sys
# set recursion limit to 10000 or it will reach the init limit 1000 when running extend_gcd()
sys.setrecursionlimit(10000)

############# Encrypt and Decrypt ##########

# Encryption
def encrypt(plaintext, N, e):
    ciphertext = []
    for p in plaintext:
        ciphertext.append(square_and_multiply(ord(p), e, N))

    return ciphertext

# Decryption with normal method
def decrypt(ciphertext, N, d):
    plaintext = ""
    for c in ciphertext:
        plaintext += chr(square_and_multiply(c, d, N))

    return plaintext

# Decrypt with Chinese remainder theorem
def decrypt_with_CRT(ciphertext, d, p, q):
    dp = d % (p-1)
    dq = d % (q-1)
    invert_q = invert(q, p)

    plaintext = ""
    for c in ciphertext:
        m1 = square_and_multiply(c, dp, p)
        m2 = square_and_multiply(c, dq, q)
        h = (invert_q * (m1 - m2)) % p
        m = m2 + h * q
        plaintext += chr(m)

    return plaintext

########### Utility function #########

# Square and multiply(x ^ h mod n)
def square_and_multiply(x, h, n):
     y = 1
     h = bin(h)[2:] # convert h into binary
     for i in range(len(h)):
         y = (y ** 2) % n
         if h[i] == '1':
             y = (y * x) % n
     return y

# Euclidean algorithm
def gcd(x, y):
	while y is not 0:
		x, y = y, x % y
	return x

# Extend Euclidean algorithm
def extend_gcd(c, d):
     if d == 0:
         return 1, 0, c
     else:
         s, t, gcd = extend_gcd(d, c % d)
         s, t = t, (s - (c // d) * t)
         return s, t, gcd

# Find the inverse multiplication of a for m
def invert(a, m):
    x, y, gcd = extend_gcd(a, m)
    if (gcd == 1):
        return x % m
    else:
        return None

# Produces large prime numbers
def pro_big_prime(bits=1024):
    b_prime = random.getrandbits(bits)
    # if the prime < 5, there will be an error when running 'random.randrange(2,n - 2)' in miller_rabin_test() 
    while miller_rabin_test(b_prime) == False or b_prime < 5:
        b_prime = random.getrandbits(bits)
    return b_prime

# Produce private_key(N, d) and public_key(N, e)
def pro_key(bits=1024):
    p = pro_big_prime(bits)
    q = pro_big_prime(bits)
    phi = (p - 1) * (q - 1)
    N = p * q

    d = None
    while d is None:
        e = 0
        while gcd(e, phi) != 1:
            e = random.randrange(phi)
        d = invert(e, phi)

    return N, d, e, p, q

# Miller-Rabin Test
def miller_rabin_test(n, repeat=45):
    k = 0
    m = (n - 1)
    if m % 2 == 0:
        m = m // 2
        k = k + 1
    if repeat > 0:
        # choose only odd a
        a=0
        while a % 2 == 0:
            a = (random.randrange(2, n - 2))
        # Compute b = a^m(mod N)
        b = square_and_multiply(a, m, n)

        #Output "Probable Prime"
        if b != 1 and b != n - 1:
            i = 1
            while i < k and b != n - 1:
                b = (b ** 2) % n
                # Output(Composite,a)
                if b == 1:
                    return False
                i = i + 1
            # Output(Composite,a)
            if b != n - 1:
                return False
        repeat -= 1

    return True

#################### main #######################

if __name__=="__main__":
    key_bits = input("Please input key bits : ")
    plaintext = input("Please input plaintext: ")
    
    print("Producing keys...")
    N, d, e, p, q = pro_key(int(key_bits))
    print("")

    print("-----private_key-----")
    print("private_key: " + str(N+d))
    print("-------public_key-------")
    print("public_key: " + str(N+e))
    print("--------------")

    print("")

    print("----plaintext----")
    print("plaintext: " + str(plaintext))

    print("----Encrypt Result----")
    ciphertext = encrypt(plaintext, N, e)
    print("ciphertext: " + str(ciphertext))
    print("--------------\n")

    print("")

    print("----Decrypt Result----")
    decrypt_result_normal = decrypt(ciphertext, N, d)
    print("Decrypt Answer(normal)   : ", decrypt_result_normal)

    decrypt_result_CRT = decrypt_with_CRT(ciphertext, d, p, q)
    print("Decrypt Answer (with CRT): ", decrypt_result_CRT)

    print("--------------\n")
