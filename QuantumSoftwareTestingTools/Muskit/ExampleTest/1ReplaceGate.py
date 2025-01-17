"""
Quantum Random Access Memory circuit
"""
import math
from qiskit import *

q = QuantumRegister(7, 'q')
c = ClassicalRegister(7, 'c')
qc = QuantumCircuit(q, c)

qc.x(q[2])
qc.p(math.pi/3,q[2])
qc.h(q[2])
qc.cswap(q[2],q[3],q[5])
qc.cswap(q[2],q[4],q[6])
qc.swap(q[0],q[3])
qc.swap(q[1],q[4])
qc.cx(q[0],q[1])
qc.x(q[0])
