import numpy as np
import perceval as pcvl
import requests as rq
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector

qubits = {
    "0": pcvl.BasicState([1, 0]),
    "1": pcvl.BasicState([0, 1])
}
qubits_ = {qubits[k]: k for k in qubits}

# On peut définir des variables symboliques : 
symbolic_alpha = pcvl.P('α')
simple_bs = pcvl.BS(theta=symbolic_alpha)
pcvl.pdisplay(simple_bs.U)

# ETAPE 1 
step_one = simple_bs
pcvl.pdisplay(step_one)

alpha = 2.49809
step_one.assign({'α': alpha})
pcvl.pdisplay(step_one)

p_step_one = pcvl.Processor("Naive", step_one)
a_step_one = pcvl.algorithm.Analyzer(
    p_step_one, 
    input_states=[qubits["0"]], 
    output_states=list(qubits.values()),             
    mapping=qubits_
)

print("L'analyser doit renvoyer : 1/10 pour 0 et 9/10 pour 1")
pcvl.pdisplay(a_step_one)
assert np.isclose(a_step_one.distribution[0][1].real, 0.9) 


# ETAPE 2 
print("---------ETAPE 2 --------------")
symbolic_beta = pcvl.P("β")
symbolic_gamma = pcvl.P("γ")
step_two = pcvl.BS(theta=symbolic_beta) // (1, pcvl.PS(phi=symbolic_gamma))
pcvl.pdisplay(step_two)


beta = 1.05  # radians
gamma = -0.524 - 1.57  # radians, correction incluse

step_two.assign({"β": beta, "γ": gamma})

b_step_two = pcvl.BackendFactory.get_backend("Naive")
b_step_two.set_circuit(step_two)
b_step_two.set_input_state(qubits["0"])

ampl0, ampl1 = b_step_two.prob_amplitude(qubits["0"]), b_step_two.prob_amplitude(qubits["1"])

res = f"|φ> = {np.round(ampl0, 2)} |0> + {np.round(ampl1, 2)} |1>"
sol = f"|φ> = {np.round(np.sqrt(3) / 2 + 0j, 2)} |0> + {np.round(np.sqrt(3) / 4 - 1j / 4, 2)} |1>"

print(f"Résultat : {res}")
print(f"Solution : {sol}")
# On s'assure que la réponse est bien égale à la solution : 
assert res == sol
print("--------- FIN 2 --------------")

def circuit_to_state_vector(circuit):
    backend = pcvl.BackendFactory.get_backend("Naive")
    backend.set_circuit(circuit)
    backend.set_input_state(qubits["0"])
    ampl0, ampl1 = backend.prob_amplitude(qubits["0"]), backend.prob_amplitude(qubits["1"])
    return Statevector([ampl0, ampl1])
plot_bloch = lambda circuit: plot_bloch_multivector(circuit_to_state_vector(circuit))
x_rot = lambda x: pcvl.Circuit(2) // (0, pcvl.PS(np.pi)) // pcvl.BS.Rx(theta=x) // (0, pcvl.PS(np.pi)) 
y_rot = lambda x: pcvl.BS.Ry(theta=x)
z_rot = lambda x: pcvl.BS.H() // x_rot(x) // pcvl.BS.H() 
# (Tous les chemins partent de |0> avec les fontions que j'ai écrites)
the_way = x_rot(-np.pi/4) // z_rot(-np.pi/4)
plot_bloch(the_way)
pcvl.pdisplay(the_way)
start_state = np.array([np.sqrt(2+np.sqrt(2))/2, np.sqrt(2-np.sqrt(2))/2 * (np.sqrt(2)/2 - 1j * np.sqrt(2)/2)])
plot_bloch_multivector(start_state)

step_state = np.array([np.sqrt(2)/2, -np.sqrt(2)/2])
plot_bloch_multivector(step_state)

finish_state = np.array([np.sqrt(2-np.sqrt(2))/2, np.sqrt(2+np.sqrt(2))/2 * (np.sqrt(2)/2 + 1j * np.sqrt(2)/2)])
plot_bloch_multivector(finish_state)

start = y_rot(np.pi/4) // z_rot(-np.pi/4)  # Pour se placer sur le départ

# Définition des angles de rotation
delta = -3*np.pi/4
epsilon = -np.pi/4
zeta = -np.pi/4
eta = -3*np.pi/4

# Une autre façon d'enchaîner les portes 
final_step = (start
                .add(0, z_rot(delta))
                .add(0, y_rot(epsilon))  # Arrivé à l'étape Hadamard
                .add(0, y_rot(zeta))
                .add(0, z_rot(eta))  # Fin du parcours !
             )
plot_bloch(final_step)

##### GET FLAG
def circuit_to_list(circuit):
    return [[(x.real, x.imag) for x in l] for l in np.array(circuit.compute_unitary())]
    
d = {
    "step_one": circuit_to_list(step_one),
    "step_two": circuit_to_list(step_two),
    "final_step": circuit_to_list(final_step)
}

URL = "https://perceval.challenges.404ctf.fr"
rq.get(URL + "/healthcheck")
response = rq.post(URL + "/challenges/1", json=d).json()
print(response)
