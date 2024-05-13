from sage.all import *


# Créer un anneau de polynômes avec coefficients entiers
var("x")

# Définir le polynôme P
P = 9621137267597279445*x**14 + 18586175928444648302*x**13 + 32676401831531099971*x**12 + 42027592883389639924*x**11 + 51798494845427766041*x**10 + 63869556820398134000*x**9 + 74077517072964271516*x**8 + 79648012933926385783*x**7 + 69354747135812903055*x**6 + 59839859116273822972*x**5 + 48120985784611588945*x**4 + 36521316280908315838*x**3 + 26262107762070282460*x**2 + 16005081865177344119*x + 5810204145325142255 

# Définir la valeur spécifique k
k = 60130547801168751450983574194169752606596547774564695794919298973251203587128237799602582911050022571941793197314565314876508860461087209144687558341117955877761335067848122512358149929745084363835027292307961660634453113069168408298081720503728087287329906197832876696742245078666352861209105027134133927

# Résoudre l'équation P(x) = k
solutions = solve(P - k == 0, x)

# Afficher les solutions
print("Les solutions de l'équation P(x) = k sont :")
print(solutions)
