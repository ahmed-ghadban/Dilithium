from dilithium import Dilithium2
pk, sk = Dilithium2.keygen()
msg = b"Your message signed by Dilithium"
sig = Dilithium2.sign(sk, msg)
assert Dilithium2.verify(pk, msg, sig)
assert not Dilithium2.verify(pk, b"", sig)
pk_new, sk_new = Dilithium2.keygen()
assert not Dilithium2.verify(pk_new, msg, sig)