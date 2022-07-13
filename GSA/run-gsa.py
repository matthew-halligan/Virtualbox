import os
import sys

# This Index would be sent by the Flask App
# Lets GSA know which directory in /uploads to analyze binary metrics
i = int(sys.argv[1])

#Global list variable to manage metric result paths
metric_paths = []


# Parses the uploads folder for the original and reduced binary paths
# We can change the postfix parsing file extension to what we want
# Right now its .origin and .reduced based on the sample binaries inside /samples/CHISEL
def parse_uploads(index):
    binary_paths = []
    filepath = "uploads/{}".format(index)
    offset_index = 0
    for file in os.listdir(filepath):
        if file.endswith(".origin"):
            binary_paths.append(os.path.join(filepath, file ))
        elif file.endswith(".reduced"):
            binary_paths.append(os.path.join(filepath, file ))
        else:
            print("Could not find binary in directory...")
    
    #Taking the name of the binary for later use when printing metricsdate
    for path in binary_paths:

        #binary_paths will always have even number since it compares 2 binaries
        #We only want to take 1 of each type of binary and add it to metric_paths 
        if offset_index % 2 == 0:

            #May need to redo this piece later depending on our naming conventions for binaries
            new_paths = os.path.split(path) #splits the full /uploads/1/<binary name> path into head & tail
            paths = new_paths[1].split("-") #splits the tail(full binary name) into head & tail
            metric_path = paths[0] + "-metrics" #takes the head and appends -results to it
            metric_paths.append(metric_path) #append the tail end of path (binary name)
        
        offset_index += 1
        
    return binary_paths


# TODO: Make sure the prefixes of the binaries to be analyzed match
# Loops through the uploads/index folder and assigns binaires paths to b1 & b2
# Pops the two assigned binaries out of the binaries array
# Runs GSA on the source & hardened binary
def gsa_analyze():
    binaries = parse_uploads(i)
    analysis_count = 0

    while len(binaries) != 0:
        b1 = binaries[0] #source binary path
        b2 = binaries[1]

        binaries.pop(0)
        binaries.pop(0)
        metric_str = f"{metric_paths[analysis_count]}" #the metric result folder name
        analysis_count += 1
        sub_str = "{" + "'Aggressive':'../src/{}'".format(b2) + "}" #hardened binary path
        command_str = "python3 GSA.py --output_metrics --result_folder_name {} ../src/{} \"{}\"".format(metric_str,b1,sub_str)
        print("")
        
        os.system(command_str)

    
    # After metric results are generated, move from from their folder into /uploads/<job index>
    while analysis_count != 0 and len(metric_paths) !=0:
        os.system(f"mv ../src/results/{metric_paths[analysis_count - 1]} ../src/uploads/{i}")
        analysis_count -= 1
    
    print("")
    print("=========================================================")
    print("================**GSA Process Complete**=================")
    print("=========================================================")
    print("")
    print(f"Gadget Reduction Metrics can be found in /uploads/{1}")

if __name__ == "__main__":
    gsa_analyze()