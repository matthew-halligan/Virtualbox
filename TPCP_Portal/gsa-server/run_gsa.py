import os
import sys

# Index, Binary and Transformed Binary are passed in by the Server
index = int(sys.argv[1])
binary = str(sys.argv[2])
transformedBinary = str(sys.argv[3])

# Runs GSA on the source & hardened binary
def gsa_analyze():
    analysis_count = 0
    results_name = transformedBinary + "-gsa-metrics"
    command_sub_str = "{" + "'Aggressive':'../src/uploads/{}/{}'".format(index,transformedBinary) + "}" #hardened binary path
    command_str = "python3 GSA.py --output_metrics --result_folder_name {} ../src/uploads/{}/{} \"{}\"".format(results_name,index,binary,command_sub_str)
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