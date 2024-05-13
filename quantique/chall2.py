import numpy as np
import perceval as pcvl

from perceval import pdisplay, PS, BS, Circuit, BasicState, Processor, StateVector
from perceval.backends import BackendFactory
from perceval.algorithm import Analyzer
from exqalibur import FockState
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
from numpy import pi, cos, sin
from typing import Optional, List, Tuple


# On reprend notre encodage par rail
qubits = {
    "0": BasicState([1, 0]),
    "1": BasicState([0, 1])
}
qubits_ = {qubits[k]: k for k in qubits}
sqlist = [qubits["0"], qubits["1"]]

# Analyse du circuit
def analyze(circuit: Circuit, input_states: Optional[FockState] = None, output_states: Optional[FockState] = None) \
        -> None:
    if input_states is None:
        input_states = sqlist
    if output_states is None:
        output_states = sqlist
    p = Processor("Naive", circuit)
    a = Analyzer(p, input_states, output_states, mapping=qubits_)
    pdisplay(a)

# Analyse du circuit en calculant les amplitudes
def amplitudes(circuit: Circuit, input_state: Optional[FockState] = None, output_states: Optional[FockState] = None) \
        -> (complex, complex):
    if input_state is None:
        input_state = qubits["0"]
    if output_states is None:
        output_states = sqlist
    b = BackendFactory.get_backend("Naive")
    b.set_circuit(circuit)
    b.set_input_state(input_state)
    return {qubits_[k]: roundc(b.prob_amplitude(k)) for k in output_states}

# Affichage de la sphère de Bloch
def circuit_to_state_vector(circuit: Circuit) -> Statevector:
    ampl0, ampl1 = amplitudes(circuit)
    return Statevector([ampl0, ampl1])
plot_bloch = lambda circuit : plot_bloch_multivector(circuit_to_state_vector(circuit))

# Rotations
x_rot = lambda x: Circuit(2) // (0, PS(pi)) // BS.Rx(theta=x) // (0, PS(pi)) 
y_rot = lambda x: BS.Ry(theta=x)
z_rot = lambda x: BS.H() // x_rot(x) // BS.H() 

# Trigonométrie avec Matplotlib 
def plot_trig(angles, colors=None, annotations=None):
    r = 1.5
    if colors is None:
        colors = ["blue"] * len(angles)
    if annotations is None:
        annotations = [""] * len(angles)
    for angle, color, annotation in zip(angles, colors, annotations):
        pos_x = r * cos(angle)
        pos_y = r * sin(angle)
        plt.plot([0, pos_x], [0, pos_y], color=color)
        pos_x_a = pos_x + np.sign(pos_x) * 0.1 - (0.05 * len(annotation) if np.sign(pos_x) < 0 else 0)
        pos_y_a = pos_y + np.sign(pos_y) * 0.1
        plt.gca().annotate(annotation, xy=(pos_x_a, pos_y_a), xycoords='data', fontsize=10)

    plt.plot(0, 0, color='black', marker='o')
    a = np.linspace(0 * pi, 2 * pi, 100)
    xs, ys = r * cos(a), r * sin(a)
    plt.plot(xs, ys, color="black")
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.gca().set_aspect('equal')
    plt.show()

# Version de `round()` pour les nombres complexes.
def roundc(c: complex, decimals: int = 2) -> complex:
    return round(c.real, decimals) + round(c.imag, decimals) * 1j

hadamard_gate = BS.H()
print(amplitudes(hadamard_gate))
analyze(hadamard_gate)
plot_bloch(hadamard_gate)

plot_trig([0, pi/2, pi/4, -pi/4], ["blue", "blue", "red", "red"], ["|0>", "|1>", "|+>", "|->"])



N = 100
bits_alice = np.random.randint(low=0, high=2, size=(4 * N,))
plot_trig([0, pi/2, pi/4, 3*pi/4], ["blue", "blue", "red", "red"], ["0 (+)", "1 (+)", "0 (x)", "1 (x)"])
bases_alice = np.array(["+" if b == 0 else "x" for b in np.random.randint(low=0, high=2, size=(4 * N,))])
qubits_alice = []
qubits["0x"] = qubits["0"] + qubits["1"] 
qubits["1x"] = qubits["1"] - qubits["0"] 
print(type(qubits["0"]), type(qubits["0x"]))
for bit, basis  in zip(bits_alice, bases_alice):
    if basis == "+":
        s = pcvl.StateVector(qubits["0"]) if bit == 0 else pcvl.StateVector(qubits["1"])
    else: 
        s = qubits["0x"] if bit == 0 else qubits["1x"]
    qubits_alice.append(s)

    # On affiche les 9 premiers pour vérifier :
    if len(qubits_alice) < 10: 
        print(f"Bit à encoder : {bit}, base choisie : {basis}, qubit correspondant : {s}")

bases_bob = np.array(["+" if b == 0 else "x" for b in np.random.randint(low=0, high=2, size=(4*N,))])
def measure(input_state, circuit, full=False):
    p = pcvl.Processor("SLOS", circuit)
    p.with_input(input_state)
    sampler = pcvl.algorithm.Sampler(p)

    # Mesure (complète) faite avec 1000 essais, on se retrouve donc avec un résultat semblable 
    # à l'Analyser
    if full:
        sample_count = sampler.sample_count(1000)
        return sample_count['results']
        
    sample_count = sampler.sample_count(1)
    return list(sample_count['results'].keys())[0]

base_p = Circuit(2)
print(f"""
0 dans la base + : {measure(qubits["0"], base_p, full=True)}
1 dans la base + : {measure(qubits["1"], base_p, full=True)}
0 dans la base x ({qubits["0x"]}) mesurée dans la base + : {measure(qubits["0x"], base_p, full=True)}
1 dans la base x ({qubits["1x"]}) mesurée dans la base + : {measure(qubits["1x"], base_p, full=True)}
""")

base_x = y_rot(-pi/2)

print(f"""
0 dans la base x : {measure(qubits["0x"], base_x, full=True)}
1 dans la base x : {measure(qubits["1x"], base_x, full=True)}
0 dans la base + ({qubits["0"]}) mesurée dans la base x : {measure(qubits["0"], base_x, full=True)}
1 dans la base + ({qubits["1"]}) mesurée dans la base x : {measure(qubits["1"], base_x, full=True)}
""")

bits_bob = []
for q, b in zip(qubits_alice, bases_bob): 
    if b == "+":
        bits_bob.append(0 if measure(q, base_p) == qubits["0"] else 1)
    else:
        bits_bob.append(0 if measure(q, base_x) == qubits["0"] else 1)
bits_bob = np.array(bits_bob)

correspondance_secret_key_bits_bob = bits_bob == bits_alice
np.sum(correspondance_secret_key_bits_bob) / (4 * N)

correspondance_bases_alice_bob = bases_bob == bases_alice 
half_bits_bob = bits_bob[correspondance_bases_alice_bob]
half_bits_alice = bits_alice[correspondance_bases_alice_bob]
# ATTENTION : Ne pas relancer la cellule toute seule, relancer tout le notebook pour rafraichir cette cellule correctement. 

last_slice = len(half_bits_bob) // 2
verification = half_bits_bob[:last_slice] == half_bits_alice[:last_slice]
print(f"Pourcentage de correspondance : {int(np.sum(verification) / last_slice * 100)}%")

secret_key = half_bits_bob[last_slice:]
print(f"Secret key : {secret_key}, taille : {len(secret_key)}")




N = 100

# Alice prépare ses qubits
bits_alice = np.random.randint(low=0, high=2, size=(4 * N,))
bases_alice = np.array(["+" if b == 0 else "x" for b in np.random.randint(low=0, high=2, size=(4 * N,))])
qubits_alice = []
for bit, basis  in zip(bits_alice, bases_alice):
    if basis == "+":
        s = pcvl.StateVector(qubits["0"]) if bit == 0 else pcvl.StateVector(qubits["1"])
    else:
        s = qubits["0x"] if bit == 0 else qubits["1x"]
    qubits_alice.append(s)


# Ève les intercepte et applique la même méthode que Bob en se faisant passer pour lui
bases_eve = np.array(["+" if b == 0 else "x" for b in np.random.randint(low=0, high=2, size=(4 * N,))])
bits_eve = []
for q, b in zip(qubits_alice, bases_eve):
    if b == "+":
        bits_eve.append(0 if measure(q, base_p) == qubits["0"] else 1)
    else:
        bits_eve.append(0 if measure(q, base_x) == qubits["0"] else 1)

bits_eve = np.array(bits_eve)



# Elle renvoie ensuite les qubits correspondants pour se faire passer pour Alice
qubits_eve = []
for bit, basis  in zip(bits_eve, bases_eve):
    if basis == "+":
        s = pcvl.StateVector(qubits["0"]) if bit == 0 else pcvl.StateVector(qubits["1"])
    else:
        s = qubits["0x"] if bit == 0 else qubits["1x"]
    qubits_eve.append(s)

# Bob reçoit les qubits d'Ève et applique la même méthode que précédemment 
bases_bob = np.array(["+" if b == 0 else "x" for b in np.random.randint(low=0, high=2, size=(4 * N,))])
bits_bob = []
for q, b in zip(qubits_eve, bases_bob):
    if b == "+":
        bits_bob.append(0 if measure(q, base_p) == qubits["0"] else 1)
    else:
        bits_bob.append(0 if measure(q, base_x) == qubits["0"] else 1)
bits_bob = np.array(bits_bob)


# Dernière étape : mise en commun
correspondance_bases_alice_bob = bases_bob == bases_alice
half_bits_alice = bits_alice[correspondance_bases_alice_bob]
half_bits_bob = bits_bob[correspondance_bases_alice_bob]
last_slice = len(half_bits_alice) // 2


# Vérification du bon déroulé 
verification = half_bits_alice[:last_slice] == half_bits_bob[:last_slice]
correspondance_percentage = int(np.sum(verification) / last_slice * 100)

print(f"Pourcentage de correspondance : {correspondance_percentage}%, d'où une erreur de {100 - correspondance_percentage}%.")

secret_key_step_1 = half_bits_bob[:last_slice]
print(secret_key_step_1)



# ETAPE 2
N = 100
# Alice prépare ses qubits
bits_alice = np.random.randint(low=0, high=2, size=(4 * N,))
bases_alice = np.array(["+" if b == 0 else "x" for b in np.random.randint(low=0, high=2, size=(4 * N,))])
qubits_alice = []
for bit, basis  in zip(bits_alice, bases_alice):
    if basis == "+":
        s = pcvl.StateVector(qubits["0"]) if bit == 0 else pcvl.StateVector(qubits["1"])
    else:
        s = qubits["0x"] if bit == 0 else qubits["1x"]
    qubits_alice.append(s)


# Ève les intercepte et applique la même méthode que Bob en se faisant passer pour lui
base_b = y_rot(-pi/4)
bits_eve = []
qubits["0b"] = 2 * qubits["0"] + qubits["1"]
qubits["1b"] = 2 * qubits["1"] - qubits["0"]

for q in qubits_alice:
    bits_eve.append(0 if measure(q, base_b) == qubits["0"] else 1)
bits_eve = np.array(bits_eve)

# Elle renvoie ensuite les qubits correspondants pour se faire passer pour Alice
qubits_eve = []
for bit in bits_eve:
    s = qubits["0b"] if bit == 0 else qubits["1b"]
    qubits_eve.append(s)




# Bob reçoit les qubits d'Ève et applique la même méthode que précédemment 
bases_bob = np.array(["+" if b == 0 else "x" for b in np.random.randint(low=0, high=2, size=(4 * N,))])
bits_bob = []
for q, b in zip(qubits_eve, bases_bob):
    if b == "+":
        bits_bob.append(0 if measure(q, base_p) == qubits["0"] else 1)
    else:
        bits_bob.append(0 if measure(q, base_x) == qubits["0"] else 1)
bits_bob = np.array(bits_bob)


# Dernière étape : mise en commun
correspondance_bases_alice_bob = bases_bob == bases_alice
half_bits_alice = bits_alice[correspondance_bases_alice_bob]
half_bits_bob = bits_bob[correspondance_bases_alice_bob]
last_slice = len(half_bits_alice) // 2


# Vérification du bon déroulé 
verification = half_bits_alice[:last_slice] == half_bits_bob[:last_slice]
correspondance_percentage = int(np.sum(verification) / last_slice * 100)

print(f"Pourcentage de correspondance : {correspondance_percentage}%, d'où une erreur de {100 - correspondance_percentage}%.")

secret_key_step_2 = half_bits_bob[:last_slice]


def circuit_to_list(circuit: Circuit) -> List[List[Tuple[float, float]]]:
    return [[(x.real, x.imag) for x in l] for l in np.array(circuit.compute_unitary())]
    
def state_vector_to_list(sv: StateVector) -> List[Tuple[float, float]]:
    if type(sv) is not StateVector:
        sv = pcvl.StateVector(sv)
    sv.normalize()
    r = [(0., 0.), (0., 0.)]
    for k, v in sv:
        r[int(qubits_[k])] = (v.real, v.imag)
    return r

def list_to_state_vector(p: List[Tuple[float, float]]) -> StateVector:
    return complex(p[0][0], p[0][1]) * StateVector([1, 0]) + complex(p[1][0], p[1][1]) * StateVector([0, 1]) 


d = {
    "base_eve_1": circuit_to_list(base_b),
    "base_eve_2": circuit_to_list(base_b),
    "qubit_eve_1": state_vector_to_list(qubits["0b"]),
    "qubit_eve_2": state_vector_to_list(qubits["1b"]),
    "qubit_eve_3": state_vector_to_list(qubits["0b"]),
    "qubit_eve_4": state_vector_to_list(qubits["1b"])
}

import requests as rq

URL = "https://perceval.challenges.404ctf.fr"
rq.get(URL + "/healthcheck").json()
response = rq.post(URL + "/challenges/2", json=d).json()
print(response)