from Cryptosystem import CryptoSystem

if __name__ == '__main__':
    for i in range(1, 11):
        number = i
        f = open('texts\\test' + str(number) + '.in', 'rb')
        text = f.read()
        f.close()
        f = open('texts\\key' + str(number) + '.in', 'rb')
        key = f.read()
        f.close()

        system = CryptoSystem(key, text)
        res, count_bytes = system.job(text)

        f = open('texts\\test' + str(number) + '.out', 'wb')
        f.write(res.to_bytes(count_bytes, 'big'))
        f.close()
