import numpy as np

def read_data(filename):

    data = {}

    with open(filename) as f:

        record = []
        name = ""
        
        while True:
            line = f.readline()
            if not line or line == "":
                data[name] = record
                record = []
                break
            if line[0] == "#":
                continue
            if len(line) > 8 and line[0:7] == "SECTION":
                name = line[:-1]
                continue
            if line[0] == '\n':
                data[name] = record
                record = []
            else:
                record.append(line[:-1])
            
    return data

def process_data(data):
    data["SECTION_HORIZON"] = int(data["SECTION_HORIZON"][0])

    data["DAYS"] = range(1, data["SECTION_HORIZON"] + 1)

    data["WEEKENDS"] = range(1, data["SECTION_HORIZON"] // 7 + 1)

    data["SHIFTS"] = [x[0] for x in data["SECTION_SHIFTS"]]

    data["STAFF"] = [x[0] for x in data["SECTION_STAFF"]]

    data["SCENARIOS"] = range(10)

    data["SECTION_SHIFTS"] = [(id, int(length), list(filter(None, forbid.split('|')))) for id, length, forbid in
                                [x.split(",") for x in data["SECTION_SHIFTS"]]]
    
    data["SECTION_STAFF"] = [(id, 
                                [(y[0], int(y[1])) for y in [x.split("=") for x in maxs.split("|")]],
                                int(maxt), int(mint), int(maxc), int(minc), int(mind), int(maxw)) for
                                id, maxs, maxt, mint, maxc, minc, mind, maxw in
                                [x.split(",") for x in data["SECTION_STAFF"]]]

    
    data["SECTION_DAYS_OFF"] = [x.split(",") for x in data["SECTION_DAYS_OFF"]]
    for idx, lst in enumerate(data["SECTION_DAYS_OFF"]):
        for idx2, elem in enumerate(lst):
            if idx2 == 0:
                continue
            else: 
                data["SECTION_DAYS_OFF"][idx][idx2] = int(elem)

    data["SECTION_SHIFT_ON_REQUESTS"] = {(id, int(days), shift): int(weight) for id, days, shift, weight in
                            [x.split(",") for x in data["SECTION_SHIFT_ON_REQUESTS"]]}
    
    data["SECTION_SHIFT_OFF_REQUESTS"] = {(id, int(days), shift): int(weight) for id, days, shift, weight in
                            [x.split(",") for x in data["SECTION_SHIFT_OFF_REQUESTS"]]}
    
    data["SECTION_COVER0"] = [(int(day), shift, int(requirement), int(under), int(over)) for day, shift, requirement, under, over in
                            [x.split(",") for x in data["SECTION_COVER"]]]
    
    data["SECTION_COVER1"] = [(int(day), shift, int(requirement) + 1, int(under), int(over)) for day, shift, requirement, under, over in
                            [x.split(",") for x in data["SECTION_COVER"]]]
    
    data["SECTION_COVER2"] = [(int(day), shift, int(requirement) + 2, int(under), int(over)) for day, shift, requirement, under, over in
                            [x.split(",") for x in data["SECTION_COVER"]]]
    
    data["SECTION_COVER3"] = [(int(day), shift, int(requirement) - 1, int(under), int(over)) for day, shift, requirement, under, over in
                            [x.split(",") for x in data["SECTION_COVER"]]]
    
    data["SECTION_COVER4"] = [(int(day), shift, int(requirement) - 2, int(under), int(over)) for day, shift, requirement, under, over in
                            [x.split(",") for x in data["SECTION_COVER"]]]
    

    
    data["SECTION_COVER5"] = [(int(day), shift, int(requirement), int(under) + np.random.uniform(-50, 50), int(over) + np.random.uniform(-1, 5)) for day, shift, requirement, under, over in
                            [x.split(",") for x in data["SECTION_COVER"]]]
    
    data["SECTION_COVER6"] = [(int(day), shift, int(requirement) + 1, int(under) + np.random.uniform(-50, 50), int(over) + np.random.uniform(-1, 5)) for day, shift, requirement, under, over in
                            [x.split(",") for x in data["SECTION_COVER"]]]
    
    data["SECTION_COVER7"] = [(int(day), shift, int(requirement) + 2, int(under) + np.random.uniform(-50, 50), int(over) + np.random.uniform(-1, 5)) for day, shift, requirement, under, over in
                            [x.split(",") for x in data["SECTION_COVER"]]]
    
    data["SECTION_COVER8"] = [(int(day), shift, int(requirement) - 1, int(under) + np.random.uniform(-50, 50), int(over) + np.random.uniform(-1, 5)) for day, shift, requirement, under, over in
                            [x.split(",") for x in data["SECTION_COVER"]]]
    
    data["SECTION_COVER9"] = [(int(day), shift, int(requirement) - 2, int(under) + np.random.uniform(-50, 50), int(over) + np.random.uniform(-1, 5)) for day, shift, requirement, under, over in
                            [x.split(",") for x in data["SECTION_COVER"]]]

    return data
    
def get_data(filename):
    return process_data(read_data(filename))