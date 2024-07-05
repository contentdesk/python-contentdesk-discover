
def getEnvironment(sys):
    # Set Environments
    if sys.argv[1] == "all":
        environments = getEnvironment()
    else:
        environments = [sys.argv[1]]
    return environments

def getArguments(sys):
    if sys.argv[2:] == []:
        arguments = None
    else:
        arguments = sys.argv[2:]
    print(arguments)
    return arguments