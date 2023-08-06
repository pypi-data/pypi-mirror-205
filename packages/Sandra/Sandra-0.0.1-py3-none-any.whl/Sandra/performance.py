from Crypto.Cipher import AES 
from . import sandra

import timeit
import pandas as pd

def performance_test():
    with open('./txt/taylor_swift_1KB.txt', 'rb') as f:
        taylor_swift_1KB = f.read()

    with open('./txt/taylor_swift_5KB.txt', 'rb') as f:
        taylor_swift_5KB = f.read()

    with open('./txt/taylor_swift_10KB.txt', 'rb') as f:
        taylor_swift_10KB = f.read()

    with open('./txt/taylor_swift_100KB.txt', 'rb') as f:
        taylor_swift_100KB = f.read()

    files = {
        'taylor_swift_1KB.txt'  : taylor_swift_1KB,
        'taylor_swift_5KB.txt'  : taylor_swift_5KB,
        'taylor_swift_10KB.txt' : taylor_swift_10KB,
        'taylor_swift_100KB.txt': taylor_swift_100KB
    }

    iv   = bytes.fromhex('fffffe00000000000000000000000000')
    key  = bytes.fromhex('00000000000000000000000000000000')

    stats = dict()

    def run_n_times(mode_name, encryptor, decryptor, OPENPGP=0, n=100):
        if mode_name + '_enc' not in stats:
            stats[mode_name + '_enc'] = dict()
            stats[mode_name + '_dec'] = dict()
        for filename, file in files.items():
            ct = encryptor.encrypt(file)
            if OPENPGP == 1:
                eiv, ct = ct[:18], ct[18:]
                decryptor = AES.new(key, AES.MODE_OPENPGP, eiv)
            elif OPENPGP == 2:
                eiv, ct = ct[:18], ct[18:]
            t = timeit.Timer(
                lambda: encryptor.encrypt(file)
            )
            stats[mode_name + '_enc'][filename] = t.timeit(n) / n
            t = timeit.Timer(
                lambda: decryptor.decrypt(ct)
            )
            stats[mode_name + '_dec'][filename] = t.timeit(n) / n




    # PyCrypto CFB
    encryptor = AES.new(key, AES.MODE_CFB, iv, segment_size=16)
    decryptor = AES.new(key, AES.MODE_CFB, iv, segment_size=16)
    run_n_times('CFB', encryptor, decryptor, n=1000)
    print(">> Finished running CFB 1000 times")

    # PyCrypto OPENPGP
    encryptor = AES.new(key, AES.MODE_OPENPGP, iv)
    decryptor = None
    run_n_times('OPENPGP',encryptor, decryptor, OPENPGP=1, n=1000)
    print(">> Finished running OPENPGP 1000 times")

    # Sandra OPENPGP
    enc_dec_sandra = sandra.AES(key, sandra.MODE_OPENPGP, iv)
    run_n_times('OPENPGP_SANDRA', enc_dec_sandra, enc_dec_sandra, OPENPGP=2, n=100)
    print(">> Finished running OPENPGP_SANDRA 100 times")

    # Troy RSA (a wrapper around PyCrypto)
    enc_dec_rsa = troy.RSA(1024)
    run_n_times('RSA_TROY', enc_dec_rsa, enc_dec_rsa, n=100)
    print(">> Finished running RSA_TROY 100 times")

    print("======================== Results ==========================")
    df = pd.DataFrame.from_dict(stats, orient='index')
    print(df)
    return stats