def rol(x, n, size=2):
    n = n % (size * 8)
    return int('0b' + bin((x << n) | (x >> (size * 8 - n)))[-size * 8:], 2)


class CryptoSystem:
    def __init__(self, key, text):
        self.key = int.from_bytes(key, 'big')
        self.text = text
        self.S = [9, 15, 3, 13, 12, 0, 2, 10, 8, 11, 1, 7, 5, 6, 14, 4]
        self.SP_A = 29
        self.SP_B = 31
        self.key_part1 = (self.key & 0xffff0000) >> 16
        self.key_part2 = self.key & 0x0000ffff
        self.key1 = rol(self.key_part1, 10)
        self.key2 = self.key_part1 ^ 17361 ^ self.key_part2
        self.key3 = (((self.key_part1 ^ 9860) | self.key_part2) << 16) | (self.key_part1 & (self.key_part2 ^ 16759))
        self.key4 = self.key_part1 & self.key_part2

    def job(self, plainText):
        lenPlainText = len(plainText)
        result = 0

        plainText = int.from_bytes(plainText, 'big')
        shiftBits = lenPlainText*8 - 32
        while shiftBits > -1:
            bits_32 = plainText >> shiftBits
            bits_32 &= 0xffffffff
            encryptedBits_32 = self.calculate(bits_32)
            result |= encryptedBits_32
            if shiftBits >= 32:
                result <<= 32
            shiftBits -= 32
        return result

    def calculate(self, plaintText):
        resultText = self.layMessi(plaintText, self.key1)
        resultText = self.festel(resultText, self.key2)
        resultText = self.sp(resultText, self.key3, 32)
        resultText = self.layMessi(resultText, self.key4)
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


