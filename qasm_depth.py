qasm = """OPENQASM 2.0;
 include "qelib1.inc";
 qreg q[5];
 h q[0];
 h q[2];
 h q[1];
 cz q[0], q[2];
 cz q[0], q[1];
 h q[3];
 cz q[0], q[3];
 h q[4];
 cz q[0], q[4];
 h q[4];
 h q[3];
 h q[2];
 h q[1];"""

def get_depth(qasm):

    qasm_list=qasm.split("\\n")

    occur_dict = dict()

    #Loop to count the two qubit gates and store the qubits they act on
    for element in qasm_list:
        for i,s in enumerate(element):
            if s == 'q':
                qubit = element[i+2]
                if qubit not in occur_dict.keys():
                    occur_dict[qubit] = 1
                else:
                    #else add phase to existing entry
                    occur_dict[qubit] += 1

    return max(occur_dict.values())

print(get_depth(qasm))