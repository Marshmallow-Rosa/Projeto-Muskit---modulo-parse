"""
Analyzer configuration that specify: 
1. significance level for a statistical test, e.g., p-value=0.05
2. qubits that should be used as inputs
3. qubits that should be measured
"""
inputQubits = 7 # Number of input qubits of a quantum program out of the total number of qubits the program has
measureQubits = [0, 1] # Qubits that will be measured
p_value = 0.05 # Chosen significance level
