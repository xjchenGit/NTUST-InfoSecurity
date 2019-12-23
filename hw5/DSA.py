import hashlib
import random, sys

# set recursion limit to 10000 or it will reach the init limit 1000 when running extend_gcd()
sys.setrecursionlimit(10000)

#### key generation & signature generation & signature vaerify ####
def key_generation(q_bits=160,p_bits=1024, is_prime = False):
    if not is_prime:
        S = random.getrandbits(20)
        q = pro_big_prime(q_bits)
        n = (p_bits-1) // q_bits
        b = (q >> 5) & 15
        C = 0
        N = 2
        V = {}
        pow1 = pow(2, b)
        pow2 = pow(2, p_bits-1)

        while C < 4096:
            for k in range(0, n+1):
                V[k] = sha_to_int(S + N + k)
            W = V[n] % pow1
            for k in range(n-1, -1, -1):
                W = (W << q_bits) + V[k]
            X = W + pow2
            p = X-(X % (2 * q) - 1)
            if(pow2 <= p and miller_rabin_test(p)):
                is_prime = True
                break;
            C += 1
            N += n + 1
    alpha = square_and_multiply(2, (p - 1) // q, p)
    d = random.randrange(1, q)
    beta = square_and_multiply(alpha, d, p)
    return p, q, alpha, beta, d

def signature_generation(message, p, q, alpha, d):
    s = 0
    if s == 0:
        k = random.randrange(2, q)
        r = square_and_multiply(alpha, k, p) % q
        s =  (sha_string_to_int(message) + d * r) * invert(k, q) % q
    return r, s

def signature_verify(message, r, s, p, q):
    if not (0 < r < q or 0 < s < q):
        print("r and s are both 160 bits")

    w = invert(s, q)
    u1 = (sha_string_to_int(message) * w) % q
    u2 = (r * w) % q
    v = ((square_and_multiply(alpha, u1, p) * square_and_multiply(beta, u2, p)) % p) % q
    
    return v == r

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

# Produces large prime numbers
def pro_big_prime(bits=1024):
    b_prime = random.getrandbits(bits)
    # if the prime < 5, there will be an error when running 'random.randrange(2,n - 2)' in miller_rabin_test() 
    while miller_rabin_test(b_prime) == False or b_prime < 5:
        b_prime = random.getrandbits(bits)
    return b_prime

# SHA1
def sha_string_to_int(m):
    return int(hashlib.sha1(m.encode()).hexdigest(), 16)

def sha_to_int(n):
    return int(hashlib.sha1(bin(n).encode()).hexdigest(), 16)

if __name__=="__main__":
    print("Producing keys...")
    keygen=input("Please enter how many bits do you need in q : ")
    p, q, alpha, beta, d = key_generation(q_bits=int(keygen))
    
    print("")
    # The keys are: public key(p,q,alpha,beta), private key(d)
    print("-----key generations-----")
    print("p =", p, "\nq =", q, "\nalpha =", alpha, "\nbeta =", beta, "\nd =", d)
    print("--------------")

    print("")
    print("----message----")
    message = input("Please input message : ")
    
    print("")
    # Given: message, private key d and public key(p,q,alpha,beta)
    print("----signature----")
    r, s = signature_generation(message, p, q, alpha, d)
    print("r =", r)
    print("s =", s)
    print("--------------\n")

    print("")
    # Given: message, signature(r,s) and public key(p,q,alpha,beta)
    print("----verify----")
    v = signature_verify(message, r, s, p, q)
    if v:
        print("valid")
    elif not v:
        print("invalid")
    print("--------------\n")