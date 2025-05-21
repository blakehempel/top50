import pandas as pd
import os
import sys


def main(getdata, research):
    
    print('Project Top 50')
    if getdata:
        import top50.engine.eikondataloader as edl
        edl.start()
    
    if research:
        import top50.engine.researchengine as re
        re.start()
    
    return
        

if __name__ == "__main__":
    def clear_console():
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    clear_console()
    
    getdata = False
    research = False

    # Check if any arguments were passed
    if len(sys.argv) > 1:
        # The first argument is sys.argv[1], the second is sys.argv[2], etc.
        argument1 = sys.argv[1]
        if argument1 == "getdata":
            print("Running getdata mode.")
            getdata=True
        elif argument1 == "backtest":
            print("Running backtest mode.")
            research=True
        else:
            print(f"Unknown argument: {argument1}. Valid inputs are 'getdata' or 'backtest'.")

    else:
        print("No arguments provided. Starting ResearchEngine using ResearchEngine.")
        research=True
        
    main(getdata, research)
    exit(0)


