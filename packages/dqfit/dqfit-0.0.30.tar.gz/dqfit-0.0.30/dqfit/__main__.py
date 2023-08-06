import sys
import json
import pandas as pd

import dqfit as dq

def main(dir: str, outdir:str, contexts: str) -> None:
    # revist
    print("...Designed for NCQA Data Quality Pilot...")

    print(f"Loading FHIR from {dir}...")
    
    fhir = dq.read_fhir(dir=dir)
    
    for context_key in contexts.split("|"):
        """
            Writes:
                result to json
                and context-summary to html
        """
        model = dq.DQI3(context_key=context_key)
        result: pd.DataFrame = model.fit(bundles=fhir)
        OUT = {
            "index": model.index(result=result), # scalar
            "context_fitness": model.context_fitness(result=result), # (m, M)
            "path_level_result": result.to_dict(orient='records'), #
        }
        with open(f"{outdir}/{context_key}-result.json", "w") as f:
            json.dump(OUT, f)
        fig = model.visualize(result=result)
        fig.write_html(f"{outdir}/{context_key}-context-report.html")

     
if __name__ == "__main__":
    try:
        main(
            dir=sys.argv[1], 
            outdir=sys.argv[2],
            contexts=sys.argv[3],
            n=int(sys.argv[4])
        )
    except Exception as e:
        print(e)
        print("To run the package: ")
        print("$ python -m dqfit DIR OUTDIR 'CONTEXTS' N\n")
        print("For example:")
        print("$ python -m dqfit bundles/A . 'COLE|BCSE' N\n")
        print("DIR: directory of FHIR (Bulk or Bundles) as .json or .json.gz")
        print("OUTDIR: directory to for .json and .html output")
        print("CONTEXTS is pipe delimited string context keys in COLE|BCSE|PSA|ASFE; e.g. 'BCSE|COLE' ")
        print("N is number of bundles to include in model")
        


