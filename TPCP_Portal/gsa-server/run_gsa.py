import os
import sys

# Index, Binary and Transformed Binary are passed in by the Server
index = int(sys.argv[1])
binary = str(sys.argv[2])
transformed_binary = str(sys.argv[3])
metrics_collection = str(sys.argv[4])

# Runs GSA on the source & hardened binary
def gsa_analyze():
    analysis_count = 0
    results_name = f"gsa-metrics-{metrics_collection}-{transformed_binary}"
    command_sub_str = "{" + f"'{metrics_collection}':'../src/uploads/{index}/{transformed_binary}'"+"}" #hardened binary path
    command_str = f"python3 GSA.py --output_metrics --result_folder_name {results_name} ../src/uploads/{index}/{binary} \"{command_sub_str}\""
    print("")
        
    os.system(command_str)
    analysis_count += 1

    # After metric results are generated, move from their folder into /uploads/<job index>
    while analysis_count != 0:
        os.system(f"mv ../src/results/{results_name} ../src/uploads/{index}")
        analysis_count -= 1
    
    print("")
    print("=========================================================")
    print("================**GSA Process Complete**=================")
    print("=========================================================")
    print("")
    print(f"Gadget Reduction Metrics can be found in folder {results_name} in directory /uploads/{index}")

if __name__ == "__main__":
    gsa_analyze()