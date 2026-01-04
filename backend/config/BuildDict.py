import pprint


def build_nested_dict(raw_text):
    # 1. Split into lines and remove empty lines
    raw_lines = [line.strip() for line in raw_text.split('\n') if line.strip()]

    # 2. Fix fragmented lines (handles the 'checkpoint\ns/epoch' issue)
    fixed_paths = []
    for line in raw_lines:
        # If the line doesn't start with '.' or '/', it belongs to the previous line
        if not (line.startswith('./') or line.startswith('/')) and fixed_paths:
            fixed_paths[-1] += line
        else:
            fixed_paths.append(line)

    # 3. Build the actual dictionary
    tree = {}
    for path in fixed_paths:
        # Standardize: remove leading './'
        clean_path = path.replace('./', '', 1)

        # Skip the root dot or empty strings
        if not clean_path or clean_path == ".":
            continue

        parts = clean_path.split('/')
        current_level = tree

        for part in parts:
            if not part: continue
            # setdefault ensures we don't overwrite an existing folder
            current_level = current_level.setdefault(part, {})

    return tree

items = ("""
.
./CreativityLLM
./CreativityLLM/DataRearranging.py
./CreativityLLM/README.md
./CreativityLLM/pred_vs_actual.csv
./CreativityLLM/HeldOutTest.csv
./CreativityLLM/TimeTesting.py

./CreativityLLM/home
./CreativityLLM/home/sam
./CreativityLLM/home/sam/checkpoints
./CreativityLLM/home/sam/checkpoints/best-model.ckpt
./CreativityLLM/random-testing
./CreativityLLM/random-testing/7tobjk43
./CreativityLLM/random-testing/7tobjk43/checkpoints
./CreativityLLM/random-testing/7tobjk43/checkpoints/epoch=2-step=1497.ckpt
./CreativityLLM/random-testing/hx87fevm
./CreativityLLM/random-testing/hx87fevm/checkpoints
./CreativityLLM/random-testing/hx87fevm/checkpoints/epoch=2-step=1497.ckpt
./CreativityLLM/random-testing/hdu5cu2m

./CreativityLLM/random-testing/hdu5cu2m/checkpoints
./CreativityLLM/random-testing/hdu5cu2m/checkpoints/epoch=2-step=1497.ckpt
./CreativityLLM/random-testing/muf800f7
./CreativityLLM/random-testing/muf800f7/checkpoints
./CreativityLLM/random-testing/muf800f7/checkpoints/epoch=2-step=1497.ckpt
./CreativityLLM/random-testing/18llrume
./CreativityLLM/random-testing/18llrume/checkpoints
./CreativityLLM/random-testing/18llrume/checkpoints/epoch=2-step=1497.ckpt
./CreativityLLM/random-testing/ygf7sl0m
./CreativityLLM/random-testing/ygf7sl0m/checkpoints
./CreativityLLM/random-testing/ygf7sl0m/checkpoints/epoch=2-step=1497.ckpt
./CreativityLLM/random-testing/931ze6p7
./CreativityLLM/random-testing/931ze6p7/checkpoints
./CreativityLLM/random-testing/931ze6p7/checkpoints/epoch=2-step=1497.ckpt
./CreativityLLM/random-testing/aa4nkghb
./CreativityLLM/random-testing/aa4nkghb/checkpoints
./CreativityLLM/random-testing/aa4nkghb/checkpoints/epoch=1-step=998.ckpt
./CreativityLLM/random-testing/35du6nzc
./CreativityLLM/random-testing/35du6nzc/checkpoints
./CreativityLLM/random-testing/35du6nzc/checkpoints/epoch=0-step=299.ckpt
./CreativityLLM/random-testing/qyzhd17x
./CreativityLLM/random-testing/qyzhd17x/checkpoints
./CreativityLLM/random-testing/qyzhd17x/checkpoints/epoch=0-step=299.ckpt
./CreativityLLM/random-testing/aeyhkvfq
./CreativityLLM/random-testing/aeyhkvfq/checkpoints
./CreativityLLM/random-testing/aeyhkvfq/checkpoints/epoch=1-step=698.ckpt
./CreativityLLM/random-testing/tbngxwcd
./CreativityLLM/random-testing/tbngxwcd/checkpoints
./CreativityLLM/random-testing/tbngxwcd/checkpoints/epoch=7-step=3992.ckpt
./CreativityLLM/random-testing/rrcwa1rd
./CreativityLLM/random-testing/rrcwa1rd/checkpoints
./CreativityLLM/random-testing/rrcwa1rd/checkpoints/epoch=2-step=1497.ckpt
./CreativityLLM/random-testing/5bagacwm
./CreativityLLM/random-testing/5bagacwm/checkpoints
./CreativityLLM/random-testing/5bagacwm/checkpoints/epoch=3-step=1696.ckpt
./CreativityLLM/random-testing/8l8umtlg
./CreativityLLM/random-testing/8l8umtlg/checkpoints
./CreativityLLM/random-testing/8l8umtlg/checkpoints/epoch=2-step=1497.ckpt
./CreativityLLM/random-testing/w4clwrxa
./CreativityLLM/random-testing/w4clwrxa/checkpoints
./CreativityLLM/random-testing/w4clwrxa/checkpoints/epoch=2-step=1497.ckpt

./CreativityLLM/ComprehensionData
./CreativityLLM/ComprehensionData/Data Analysis Playground.ipynb
./CreativityLLM/ComprehensionData/DataByPrompt
./CreativityLLM/ComprehensionData/DataByPrompt/SenseOfHumor.csv
./CreativityLLM/ComprehensionData/DataByPrompt/WarmerLake.csv
./CreativityLLM/ComprehensionData/DataByPrompt/Friendliness.csv
./CreativityLLM/ComprehensionData/DataByPrompt/StudentsSinging.csv
./CreativityLLM/ComprehensionData/DataByPrompt/Jungle.csv
./CreativityLLM/ComprehensionData/DataByPrompt/OceanFloor.csv
./CreativityLLM/ComprehensionData/DataByPrompt/Robots.csv
./CreativityLLM/ComprehensionData/DataByPrompt/StarsDisappearing.csv
./CreativityLLM/ComprehensionData/DataByPrompt/Galaxy.csv
./CreativityLLM/ComprehensionData/DataByPrompt/Holds.csv
./CreativityLLM/ComprehensionData/DataByPrompt/WaterSunlight.csv
./CreativityLLM/ComprehensionData/DataByPrompt/MindReading.csv
./CreativityLLM/DataGeneration.py
./CreativityLLM/best_model.ckpt

./CreativityLLM/pred_vs_actual_perprompt.png
./CreativityLLM/pred_vs_actual_perprompt.csv
./CreativityLLM/requirements.txt
./CreativityLLM/TrainingData

./CreativityLLM/TrainingData/Filtered.csv
./CreativityLLM/TrainingData/TrainData.csv
./CreativityLLM/TrainingData/TestData.csv
./CreativityLLM/TrainingData/sctt.csv
./CreativityLLM/roberta.ckpt
./CreativityLLM/test.py
./CreativityLLM/poly-m-comps

./CreativityLLM/poly-m-comps/ht0nzumj
./CreativityLLM/poly-m-comps/ht0nzumj/checkpoints
./CreativityLLM/poly-m-comps/ht0nzumj/checkpoints/epoch=5-step=2794.ckpt
./CreativityLLM/poly-m-comps/kazmsqd2
./CreativityLLM/poly-m-comps/kazmsqd2/checkpoints
./CreativityLLM/poly-m-comps/kazmsqd2/checkpoints/epoch=5-step=2694.ckpt
./CreativityLLM/poly-m-comps/kfkybmz8
./CreativityLLM/poly-m-comps/kfkybmz8/checkpoints
./CreativityLLM/poly-m-comps/kfkybmz8/checkpoints/epoch=6-step=3193.ckpt
./CreativityLLM/poly-m-comps/mbnk3u98
./CreativityLLM/poly-m-comps/mbnk3u98/checkpoints
./CreativityLLM/poly-m-comps/mbnk3u98/checkpoints/epoch=5-step=2694.ckpt
./CreativityLLM/Model
./CreativityLLM/Model/train.py
./CreativityLLM/Model/Dataset.py
./CreativityLLM/Model/PolyEncoder.py
./datasets
./datasets/val.csv
./datasets/test.csv
./datasets/train.csv

./sudoku
./sudoku/cnn_8out_400k.ckpt
./sudoku/sudoku-cp-ai
./sudoku/sudoku-cp-ai/cnn_16out_3.7m.ckpt
./sudoku/sudoku-cp-ai/solver
./sudoku/sudoku-cp-ai/solver/SudokuBoardSolver.py
./sudoku/sudoku-cp-ai/solver/heuristics.py
./sudoku/sudoku-cp-ai/PreprocessData.py
./sudoku/sudoku-cp-ai/README.md
./sudoku/sudoku-cp-ai/latest.ckpt
./sudoku/sudoku-cp-ai/row_ckpt_large.ckpt

./sudoku/sudoku-cp-ai/sudoku-cnn-comps
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/s2vlb8jg
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/s2vlb8jg/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/s2vlb8jg/checkpoints/epoch=6-step=114849.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/frwptzud

./sudoku/sudoku-cp-ai/sudoku-cnn-comps/frwptzud/checkpoints

./sudoku/sudoku-cp-ai/sudoku-cnn-comps/frwptzud/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/5qio6wl7
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/5qio6wl7/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/5qio6wl7/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/q0btu4cq
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/q0btu4cq/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/q0btu4cq/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/n1070lo1
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/n1070lo1/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/n1070lo1/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/ubcejzv7
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/ubcejzv7/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/ubcejzv7/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/intax5ul
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/intax5ul/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/intax5ul/checkpoints/epoch=1-step=32814.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/pdng25x5
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/pdng25x5/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/pdng25x5/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/wiw0ppz5
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/wiw0ppz5/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/wiw0ppz5/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/rwc3tzl3
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/rwc3tzl3/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/rwc3tzl3/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/mm59ixw1
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/mm59ixw1/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/mm59ixw1/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/r64ryyup
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/r64ryyup/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/r64ryyup/checkpoints/epoch=5-step=98442.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/xmpaext4
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/xmpaext4/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/xmpaext4/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/kxipfu98
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/kxipfu98/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/kxipfu98/checkpoints/epoch=6-step=114849.ckpt
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/h27x6i7t
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/h27x6i7t/checkpoints
./sudoku/sudoku-cp-ai/sudoku-cnn-comps/h27x6i7t/checkpoints/epoch=9-step=164070.ckpt

./sudoku/sudoku-cp-ai/sudoku-testing
./sudoku/sudoku-cp-ai/sudoku-testing/kfayvs9y
./sudoku/sudoku-cp-ai/sudoku-testing/kfayvs9y/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/kfayvs9y/checkpoints/epoch=3-step=65628.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/kchmf0e0
./sudoku/sudoku-cp-ai/sudoku-testing/kchmf0e0/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/kchmf0e0/checkpoints/epoch=7-step=65632.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/43i8o2m3
./sudoku/sudoku-cp-ai/sudoku-testing/43i8o2m3/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/43i8o2m3/checkpoints/epoch=1-step=32814.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/kl926d3h
./sudoku/sudoku-cp-ai/sudoku-testing/kl926d3h/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/kl926d3h/checkpoints/epoch=3-step=52502.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/ehrksxcd
./sudoku/sudoku-cp-ai/sudoku-testing/ehrksxcd/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/ehrksxcd/checkpoints/epoch=6-step=14301.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/ixgp0393
./sudoku/sudoku-cp-ai/sudoku-testing/ixgp0393/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/ixgp0393/checkpoints/epoch=0-step=16407.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/ssbxd5fz
./sudoku/sudoku-cp-ai/sudoku-testing/ssbxd5fz/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/ssbxd5fz/checkpoints/epoch=7-step=65632.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/gccx48am
./sudoku/sudoku-cp-ai/sudoku-testing/gccx48am/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/gccx48am/checkpoints/epoch=14-step=246105.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/qmgjc0cw
./sudoku/sudoku-cp-ai/sudoku-testing/qmgjc0cw/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/qmgjc0cw/checkpoints/epoch=5-step=49224.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/py3yj8o9
./sudoku/sudoku-cp-ai/sudoku-testing/py3yj8o9/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/py3yj8o9/checkpoints/epoch=2-step=49221.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/jv57j7ek
./sudoku/sudoku-cp-ai/sudoku-testing/jv57j7ek/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/jv57j7ek/checkpoints/epoch=0-step=16407.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/4iva580y
./sudoku/sudoku-cp-ai/sudoku-testing/4iva580y/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/4iva580y/checkpoints/epoch=4-step=82035.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/30p1jb90
./sudoku/sudoku-cp-ai/sudoku-testing/30p1jb90/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/30p1jb90/checkpoints/epoch=3-step=65628.ckpt
./sudoku/sudoku-cp-ai/sudoku-testing/vdcqkxpl
./sudoku/sudoku-cp-ai/sudoku-testing/vdcqkxpl/checkpoints
./sudoku/sudoku-cp-ai/sudoku-testing/vdcqkxpl/checkpoints/epoch=4-step=82033.ckpt
./sudoku/sudoku-cp-ai/data_generation
./sudoku/sudoku-cp-ai/data_generation/GenerateData_HybridMRV.py
./sudoku/sudoku-cp-ai/fc1024.ckpt
./sudoku/sudoku-cp-ai/visualizations
./sudoku/sudoku-cp-ai/visualizations/metrics
./sudoku/sudoku-cp-ai/visualizations/metrics/metric-viz.ipynb
./sudoku/sudoku-cp-ai/visualizations/DataVisualization.ipynb
./sudoku/sudoku-cp-ai/requirements.txt
./sudoku/sudoku-cp-ai/sudoku-featureless
./sudoku/sudoku-cp-ai/sudoku-featureless/hdli3yk4
./sudoku/sudoku-cp-ai/sudoku-featureless/hdli3yk4/checkpoints

./sudoku/sudoku-cp-ai/sudoku-featureless/hdli3yk4/checkpoints/epoch=0-step=16407.ckpt
./sudoku/sudoku-cp-ai/sudoku-featureless/754860gz
./sudoku/sudoku-cp-ai/sudoku-featureless/754860gz/checkpoints
./sudoku/sudoku-cp-ai/sudoku-featureless/754860gz/checkpoints/epoch=0-step=16407.ckpt
./sudoku/sudoku-cp-ai/sudoku-featureless/5d5mhayi

./sudoku/sudoku-cp-ai/sudoku-featureless/5d5mhayi/checkpoints
./sudoku/sudoku-cp-ai/sudoku-featureless/5d5mhayi/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-featureless/7ajqg7as
./sudoku/sudoku-cp-ai/sudoku-featureless/7ajqg7as/checkpoints
./sudoku/sudoku-cp-ai/sudoku-featureless/7ajqg7as/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-featureless/zximyti2
./sudoku/sudoku-cp-ai/sudoku-featureless/zximyti2/checkpoints
./sudoku/sudoku-cp-ai/sudoku-featureless/zximyti2/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-featureless/o29ll069
./sudoku/sudoku-cp-ai/sudoku-featureless/o29ll069/checkpoints

./sudoku/sudoku-cp-ai/sudoku-featureless/o29ll069/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-featureless/6umvcrb3
./sudoku/sudoku-cp-ai/sudoku-featureless/6umvcrb3/checkpoints
./sudoku/sudoku-cp-ai/sudoku-featureless/6umvcrb3/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-featureless/s5zqemdb
./sudoku/sudoku-cp-ai/sudoku-featureless/s5zqemdb/checkpoints
./sudoku/sudoku-cp-ai/sudoku-featureless/s5zqemdb/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-featureless/h9vgkwga
./sudoku/sudoku-cp-ai/sudoku-featureless/h9vgkwga/checkpoints
./sudoku/sudoku-cp-ai/sudoku-featureless/h9vgkwga/checkpoints/epoch=0-step=16407.ckpt
./sudoku/sudoku-cp-ai/sudoku-featureless/8ynfsu1e
./sudoku/sudoku-cp-ai/sudoku-featureless/8ynfsu1e/checkpoints
./sudoku/sudoku-cp-ai/sudoku-featureless/8ynfsu1e/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/sudoku-featureless/my9hxgak
./sudoku/sudoku-cp-ai/sudoku-featureless/my9hxgak/checkpoints
./sudoku/sudoku-cp-ai/sudoku-featureless/my9hxgak/checkpoints/epoch=9-step=164070.ckpt
./sudoku/sudoku-cp-ai/Model
./sudoku/sudoku-cp-ai/Model/train.py
./sudoku/sudoku-cp-ai/Model/Dataset.py
./sudoku/sudoku-cp-ai/Model/model_normal.py
./sudoku/sudoku-cp-ai/Model/model_cnn.py
./sudoku/sudoku-cp-ai/performance_data.csv
./sudoku/sudoku-cp-ai/Testing
./sudoku/sudoku-cp-ai/Testing/Graphs.py
./sudoku/sudoku-cp-ai/Testing/GenerateData.py
./sudoku/sudoku.csv
./sudoku/sudoku_board_samples.csv
./sudoku/row_data.csv
./sudoku/sudoku-3m.csv
./sudoku/hybrid_mrv_data.csv
""")

if __name__ == '__main__':
    tree = build_nested_dict(items)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(tree)