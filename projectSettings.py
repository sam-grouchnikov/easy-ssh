import wandb

api = wandb.Api()

project = "sudoku-featureless"
entity = "sam-grouchnikov-kennesaw-state-university"

runs = api.runs(f"{entity}/{project}")

print(f"Runs in {project}:")
for r in runs:
    print("-", r.name, "| ID:", r.id)

    history = r.history()
    print(history)
