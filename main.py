from Cryptosystem import CryptoSystem

if __name__ == '__main__':
    for i in range(1, 11):
        number = i
        f = open('texts\\Lab4\\out\\test' + str(number) + '.out', 'rb')
        #f = open('texts\\test' + str(number) + '.in', 'rb')
        text = f.read()
        f.close()
        f = open('texts\\key' + str(number) + '.in', 'rb')
        key = f.read()
        f.close()
        f = open('texts\\Lab4\\iv\\IV' + str(number) + '.in', 'rb')
        IV = f.read()
        f.close()

        system = CryptoSystem(key, text, IV)
        res = system.job3(text)

        with open('texts\\Lab4\\test_out\\test' + str(number) + '.out', 'wb') as file:
        #with open('texts\\Lab4\\out\\test' + str(number) + '.out', 'wb') as file:
            for block in res:
                file.write(block.to_bytes(4, byteorder="big"))
        # f = open('texts\\test\\out\\test' + str(number) + '.out', 'wb')
        # f.write(res.to_bytes(count_bytes, 'big'))
        file.close()
