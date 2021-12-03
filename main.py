from Cryptosystem import CryptoSystem

if __name__ == '__main__':
    f = open('lastLab\\plain.in', 'rb')
    plainText = f.read()
    f.close()
    f = open('lastLab\\encrypted.out', 'rb')
    encText = f.read()
    f.close()

    system = CryptoSystem()
    res, count_bytes = system.job(plainText, encText)
