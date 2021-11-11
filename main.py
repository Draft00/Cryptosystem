from Cryptosystem import CryptoSystem

if __name__ == '__main__':
    f = open('texts\\example3.in', 'rb')
    text = f.read()
    f = open('texts\\example_key.in', 'rb')
    key = f.read()

    system = CryptoSystem(key, text)
    res = system.job(text)
    print(res)
    #ans = system.sp(text, key, 32)
