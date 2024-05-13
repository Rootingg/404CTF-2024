from Crypto.Util.number import *
from sage.rings.sum_of_squares import two_squares_pyx
import string
printable_chars = bytes(string.printable, 'ascii')
from Crypto.Util.number import *
flag=b"404CTF{WellDonetheSuperFlag!}"
N=2

class LaSeine:
    def __init__(self, size):
        self.l = 20
        self.p = getStrongPrime(size)

        self.a = getRandomNBitInteger(size // 16) # 64 bits
        self.b = getRandomNBitInteger(size // 16)
        self.X=Matrix(IntegerModRing(self.p),[[self.a,self.b],[self.b,-self.a]])
    def split(self, f):
        if len(f) & 1:
            f += b"\x00"
        h = len(f) // 2
        return (bytes_to_long(f[:h]), bytes_to_long(f[h:]))

    def sign(self, m, b):
        xn, yn = self.split(m)
        k = (getRandomNBitInteger(self.l - 1) << 1) + b

        for _ in range(k):
            xnp1 = (self.a*xn + self.b*yn) % self.p
            ynp1 = (self.b*xn - self.a*yn) % self.p
            xn, yn = xnp1, ynp1
        return (k, xn, yn)

X3=bytes_to_long(b"L'eau est vraiment froide p")
X4=bytes_to_long(b"ar ici (et pas tres propre)")




seine = LaSeine(1024)
print("realA, realB", seine.a, seine.b)
k1, Y1, Y2 = seine.sign(flag, 1)
k2, Y3, Y4 = seine.sign(b"L'eau est vraiment froide par ici (et pas tres propre)", 0)

# A.solve_right(Y) <=> Find Matrix X such that AX=Y
#A.solve_left(Y) <=> Find Matrix X such that XA=Y

p=seine.p

#"""
p=179358513830906148619403250482250880334528756349120678091666297907253922185623290723862265402777434007178297319701286775733620488613530869850160450412929764046707392082705800333548316425165863556480623955587411083384086805686199851628022437853672200835000268893800610064747558825805271528526924659142504913631
Y1,Y2=(151683403543233106224623577311980037274441590153911847119566701699367001537936290730922138442040542620222943385810242081949211326676472369180020899628646165132503185978510932501521730827126356422842852151275382840062708701174847422687809816503983740455064453231285796998931373590630224653066573035583863902921, 76688287388975729010764722746414768266232185597001389966088556498895611351239273625106383329192109917896575986761053032041287081527278426860237114874927478625771306887851752909713110684616229318569024945188998933167888234990912716799093707141023542980852524005127986940863843004517549295449194995101172400759)
k2,Y3,Y4=(929382, 118454610237220659897316062413105144789761952332893713333891996727204456010112572423850661749643268291339194773488138402728325770671625196790011560475297285424138262812704729573910897903628228179414627406601128765472041473647769084599481166191241495167773352105622894240398746332477947478817552973851804951566, 65891615565820497528921288257089595342791556688007325193257144738940922602117787746412089423500836495505254334866586155889060897532850381510520943387446058037766901712521471259853536310481267471645770625452422081411718151580380288380630522313377397166067417623947500542258985636659962524606869196898543973764)
#"""
def all_two_squares(n):
    return [(int(abs(d[0])),int(abs(d[1]))) for d in divisors(GaussianIntegers()(n)) if norm(d)==n]

R=IntegerModRing(p)

Yflag = Matrix(R,[[Y1],[Y2]])
Aseine = Matrix(R,[[X3],[X4]])
Yseine = Matrix(R,[[Y3],[Y4]])

Xk2 = Aseine.solve_left(Yseine)
print("found X ^ k2")
print(Xk2)
#print("X ^ 2")
#print(seine.X^2)
#print("X ^ k2")
#print(seine.X^k2)
#print((seine.X ^ k2)*Aseine==Yseine)
print((Xk2)*Aseine==Yseine)

# we notice that the real A^2+B^2 is only in Xk2[0][0]
B2PlusA2halfK2=Integer(Xk2[0][0])
Xk2Better=Matrix(R,[[B2PlusA2halfK2,0],[0,B2PlusA2halfK2]])
phi=Integer(p-1)
d=pow(Integer(k2//2),-1,phi)
B2PlusA2=Integer(pow(B2PlusA2halfK2,d,p))
print("B2+A2:")
print(B2PlusA2)
#print(seine.a**2+seine.b**2)
allPossible=all_two_squares(B2PlusA2)
print(allPossible)
allPossible=[(pA,pB) for pA,pB in allPossible if pA.bit_length()==64 and pB.bit_length()==64]
print(allPossible)
#print("real a", "real b", seine.a, seine.b)

def printable(testing):
    return all(char in printable_chars for char in testing)

nb=0
for a,b in allPossible:
    nb+=1
    print(f"possibilitie {nb}/{len(allPossible)}")
    if(a.bit_length()==64 and b.bit_length()==64):
        #assert a**2+b**2==B2PlusA2
        X=Matrix(R,[[a, b],[b,-a]])
        #assert (X^k2)*Aseine==Yseine
        #print(seine.a==a, seine.b==b)
        for i in range(2**18,2**19):
            if(i%(2**16)==0):
                print("progress:",(i-2**18)/(2**19-2**18))
            k=(i<<1)+1
            #k=k1
            A=(X^k).solve_right(Yflag)
            #print(long_to_bytes(Integer(A[0][0]))+long_to_bytes(Integer(A[1][0])))
            if(printable(  (long_to_bytes(Integer(A[0][0]))+long_to_bytes(Integer(A[1][0])))[:-1] )):
                print("found")
                print(A)
                print(long_to_bytes(Integer(A[0][0]))+long_to_bytes(Integer(A[1][0])))