import threading
from tqdm import tqdm

def rol(x, n):
    n = n % 16
    bin_n = bin((x << n) | (x >> (16 - n)))
    return int('0b' + bin_n[-min(16, len(bin_n) - 2):], 2)



class CryptoSystem:
    def __init__(self):
        self.S = [9, 15, 3, 13, 12, 0, 2, 10, 8, 11, 1, 7, 5, 6, 14, 4]
        self.SP_A = 29
        self.SP_B = 31

    def getPlainTextBlocks(self, plainText, lenPlainText):
        blocks = []

        shiftBits = lenPlainText * 8 - 32

        while shiftBits >= 0:
            bits_32 = plainText >> shiftBits
            bits_32 &= 0xffffffff
            blocks.append(bits_32)
            shiftBits -= 32
        return blocks

    def getRaundKeys(self, key):
        key_part1 = (key & 0xffff0000) >> 16
        key_part2 = key & 0x0000ffff
        key1 = rol(key_part1, 10)
        key2 = key_part1 ^ 17361 ^ key_part2
        key3 = (((key_part1 ^ 9860) | key_part2) << 16) | (key_part1 & (key_part2 ^ 16759))
        key4 = key_part1 & key_part2
        return key1, key2, key3, key4

    def job(self, plainText, encBlocks):
        lenPlainText = len(plainText)
        lenEncText = len(encBlocks)

        plainText = int.from_bytes(plainText, 'big')
        encText = int.from_bytes(encBlocks, 'big')

        blocks = self.getPlainTextBlocks(plainText, lenPlainText)

        encBlocks = self.getPlainTextBlocks(encText, lenEncText)
        encBlocks2 = []
        key = 0x11223344
        for idx, block in enumerate(blocks):
            encBlock = self.calculate(block, key)
            encBlocks2.append(encBlock)

        for key in range(12345, 2**32):
            found = True
            for idx, block in enumerate(blocks):
                encBlock = self.calculate(block, key)
                if encBlock != encBlocks[idx]:
                    found = False
                    break

            if found:
                print("FOUND KEY: ")
                print(key)
                f = open('key' + str(key) + '.out', 'wb')
                f.write(key.to_bytes(4, 'big'))
                f.close()

        count = 2**32 // 16
        t1 = threading.Thread(target=self.multiThreadJob, args=(0, count, blocks, encBlocks))
        t2 = threading.Thread(target=self.multiThreadJob, args=(count, 2 * count, blocks, encBlocks))
        t3 = threading.Thread(target=self.multiThreadJob, args=(2 * count, 3 * count, blocks, encBlocks))
        t4 = threading.Thread(target=self.multiThreadJob, args=(3 * count, 4 * count, blocks, encBlocks))
        t5 = threading.Thread(target=self.multiThreadJob, args=(4 * count, 5 * count, blocks, encBlocks))
        t6 = threading.Thread(target=self.multiThreadJob, args=(5 * count, 6 * count, blocks, encBlocks))
        t7 = threading.Thread(target=self.multiThreadJob, args=(6 * count, 7 * count, blocks, encBlocks))
        t8 = threading.Thread(target=self.multiThreadJob, args=(7 * count, 8 * count, blocks, encBlocks))
        t9 = threading.Thread(target=self.multiThreadJob, args=(8 * count, 9 * count, blocks, encBlocks))
        t10 = threading.Thread(target=self.multiThreadJob, args=(9 * count, 10 * count, blocks, encBlocks))
        t11 = threading.Thread(target=self.multiThreadJob, args=(10 * count, 11 * count, blocks, encBlocks))
        t12 = threading.Thread(target=self.multiThreadJob, args=(11 * count, 12 * count, blocks, encBlocks))
        t13 = threading.Thread(target=self.multiThreadJob, args=(12 * count, 13 * count, blocks, encBlocks))
        t14 = threading.Thread(target=self.multiThreadJob, args=(13 * count, 14 * count, blocks, encBlocks))
        t15 = threading.Thread(target=self.multiThreadJob, args=(14 * count, 15 * count, blocks, encBlocks))
        t16 = threading.Thread(target=self.multiThreadJob, args=(15 * count, 16 * count, blocks, encBlocks))

        # start threads
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()
        t9.start()
        t10.start()
        t11.start()
        t12.start()
        t13.start()
        t14.start()
        t15.start()
        t16.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        t9.join()
        t10.join()
        t11.join()
        t12.join()
        t13.join()
        t14.join()
        t15.join()
        t16.join()

    def multiThreadJob(self, start, end, blocks, encBlocks):
        for key in range(start, end):
            found = True
            for idx, block in enumerate(blocks):
                encBlock = self.calculate(block, key)
                if encBlock != encBlocks[idx]:
                    found = False
                    break

            if found:
                print("FOUND KEY: ")
                print(key)
                f = open('key' + str(key) + '.out', 'wb')
                f.write(key.to_bytes(4, 'big'))
                f.close()
        print("End of Task with ", start, end)

    def calculate(self, plaintText, key):
        key1, key2, key3, key4 = self.getRaundKeys(key)
        resultText = self.layMessi(plaintText, key1)
        resultText = self.festel(resultText, key2)
        resultText = self.sp(resultText, key3, 32)
        resultText = self.layMessi(resultText, key4)
        return resultText

    def sp(self, plaintText, key, blockSize_bit):
        sBlockResult = 0
        pBlockResult = 0
        text = plaintText
        text ^= key

        shiftBits = blockSize_bit - 4
        while shiftBits > - 1:  # S-block
            bits_4 = text >> shiftBits
            bits_4 &= 0xF
            elem = self.S[bits_4]
            sBlockResult |= elem
            if shiftBits >= 4:
                sBlockResult <<= 4
            shiftBits -= 4

        for i in range(blockSize_bit):  # P-block
            bit = sBlockResult & 1
            shift = (self.SP_A * i + self.SP_B) % blockSize_bit
            bit <<= shift
            pBlockResult |= bit
            sBlockResult >>= 1

        return pBlockResult

    def layMessi(self, plainText, key):
        X2 = plainText & 0x0000ffff
        X1 = (plainText & 0xffff0000) >> 16

        result = ((X1 ^ self.sp(X1 ^ X2, key, 16)) << 16) | (X2 ^ self.sp(X1 ^ X2, key, 16))
        return result

    def festel(self, plaintText, key):
        X2 = plaintText & 0x0000ffff
        X1 = (plaintText & 0xffff0000) >> 16
        return (X2 << 16) | (X1 ^ self.sp(X2, key, 16))


