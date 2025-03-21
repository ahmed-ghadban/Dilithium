from dilithium import Dilithium2

pk, sk = Dilithium2.keygen()
print(pk)
print(sk)

message = 'hi'
message = message.encode('utf-8')

sig = Dilithium2.sign(sk, message)

print(sig)

message = bytes(str(message),'utf-8')
message = eval(message)
plain_text = message.decode('utf-8')
print(plain_text)

valid =  Dilithium2.verify(pk, message, sig)
print("verifed Good Sign")