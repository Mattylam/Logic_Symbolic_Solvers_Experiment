import json
pyke_path = 'Processed_Datasets/ProofWriter_OWA_d5_Pyke_gpt-3.5-turbo.json'
#prover9_path =
z3_path = 'Processed_Datasets/ProofWriter_OWA_d5_Z3_gpt-3.5-turbo.json'

prontoQA_Prover9_path = 'Processed_Datasets/ProntoQA_Prover9_gpt-3.5-turbo.json'
def openworld_analysis(path):
    with open(path, 'r') as f:
        raw_dataset = json.load(f)

    Total_Executable = 0
    Exec_A = 0
    Correct_A = 0
    Exec_B = 0
    Correct_B = 0
    Exec_C = 0
    Correct_C = 0

    for example in raw_dataset:
        if example["flag"] == "success":
            Total_Executable += 1
            if example["answer"] == "A":
                Exec_A += 1
                if example["predicted_answer"] == "A":
                    Correct_A += 1
            elif example["answer"] == "B":
                Exec_B += 1
                if example["predicted_answer"] == "B":
                    Correct_B += 1
            else:
                Exec_C += 1
                if example["predicted_answer"] == "C":
                    Correct_C += 1

    print(f"Total Executable: {Total_Executable}")
    print(f"Correct A%: {Correct_A/Exec_A}")
    print(f"Correct B%: {Correct_B/Exec_B}")
    #print(f"Correct C%: {Correct_C/Exec_C}")
    print(f"Correct A: {Correct_A}")
    print(f"Correct B: {Correct_B}")
    print(f"Correct C: {Correct_C}")
    print(f"Exec A: {Exec_A}")
    print(f"Exec B: {Exec_B}")
    print(f"Exec C: {Exec_C}")
    print(f"Incorrect A: {Exec_A - Correct_A}")
    print(f"Incorrect B: {Exec_B - Correct_B}")
    print(f"Incorrect C: {Exec_C - Correct_C}")
openworld_analysis(prontoQA_Prover9_path)