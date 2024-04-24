from ortools.sat.python.cp_model import *

# Each employee can only work one shift per day
def one_shift_per_day(model,
                     data,
                     employee_dv):
    for s in data["STAFF"]:
        for d in data["DAYS"]:
            constraint = [employee_dv[s, d, t]
                          for t in data["SHIFTS"]]
            model.Add(sum(constraint) <= 1)

# Shift Rotation
def shift_rotation(model,
                     data,
                     employee_dv):
    for s in data["STAFF"]:
        for d in data["DAYS"][:-1]:
            for t in data["SHIFTS"]:
                for r in [item[2] for item in data["SECTION_SHIFTS"] if item[0] == t][0]:
                    model.Add(employee_dv[s, d, t] + employee_dv[s, d + 1, r] <= 1)

# maximum number of shifts
def max_shifts(model,
                     data,
                     employee_dv):
    for s in data["STAFF"]:
        staff = [item for item in data["SECTION_STAFF"] if item[0] == s][0]
        for t in data["SHIFTS"]:
            max_shifts = [item[1] for item in staff[1] if item[0] == t][0]
            constraint = [employee_dv[s, d, t]
                        for d in data["DAYS"]]
            model.Add(sum(constraint) <= max_shifts)

# min work time
def max_work_time(model,
                     data,
                     employee_dv):
    for s in data["STAFF"]:
        staff = [item for item in data["SECTION_STAFF"] if item[0] == s][0]
        max_time = staff[2]
        constraint = [employee_dv[s, d, t] * [item[1] for item in data["SECTION_SHIFTS"] if item[0] == t][0]
                    for d in data["DAYS"]
                    for t in data["SHIFTS"]]
        model.Add(sum(constraint) <= max_time)

# min work time
def min_work_time(model,
                     data,
                     employee_dv):
    for s in data["STAFF"]:
        staff = [item for item in data["SECTION_STAFF"] if item[0] == s][0]
        min_time = staff[3]
        constraint = [employee_dv[s, d, t] * [item[1] for item in data["SECTION_SHIFTS"] if item[0] == t][0]
                    for d in data["DAYS"]
                    for t in data["SHIFTS"]]
        model.Add(sum(constraint) >= min_time)

# max consecutive days
def max_consecutive_shifts(model,
                     data,
                     employee_dv):
    for s in data["STAFF"]:
        staff = [item for item in data["SECTION_STAFF"] if item[0] == s][0]
        max_cons_days = staff[4]
        for d in data["DAYS"][:data["SECTION_HORIZON"] - max_cons_days]:
            constraint = [employee_dv[s, j, t]
                    for j in data["DAYS"][d - 1 :d + max_cons_days]
                    for t in data["SHIFTS"]]
            model.Add(sum(constraint) <= max_cons_days)

# min consecutive days
def min_consecutive_shifts(model,
                     data,
                     employee_dv):
    for s in data["STAFF"]:
        staff = [item for item in data["SECTION_STAFF"] if item[0] == s][0]
        min_cons_days = staff[5]
        for temp in range(1, min_cons_days - 1 + 1):
            for d in data["DAYS"][:data["SECTION_HORIZON"] - (temp + 1)]:
                constraint1 = [employee_dv[s, d, t] 
                                for t in data["SHIFTS"]]
                constraint2 = [employee_dv[s, j, t] 
                                for j in data["DAYS"][d:d+temp]
                                for t in data["SHIFTS"]]
                constraint3 = [employee_dv[s, d + temp + 1, t] 
                                for t in data["SHIFTS"]]
        
                model.Add(sum(constraint1) + (temp - sum(constraint2)) + sum(constraint3) > 0)

# min consecutive days off
def min_consecutive_shifts_off(model,
                     data,
                     employee_dv):
    for s in data["STAFF"]:
        staff = [item for item in data["SECTION_STAFF"] if item[0] == s][0]
        min_cons_days = staff[6]
        for temp in range(1, min_cons_days - 1 + 1):
            for d in data["DAYS"][:data["SECTION_HORIZON"] - (temp + 1)]:
                constraint1 = [employee_dv[s, d, t] 
                                for t in data["SHIFTS"]]
                constraint2 = [employee_dv[s, j, t] 
                                for j in data["DAYS"][d:d+temp]
                                for t in data["SHIFTS"]]
                constraint3 = [employee_dv[s, d + temp + 1, t] 
                                for t in data["SHIFTS"]]
        
                model.Add((1 - sum(constraint1)) + sum(constraint2) + (1 - sum(constraint3)) > 0)

# max weekends
def max_weekends(model,
                     data,
                     employee_dv,
                     weekend_dv):
    for s in data["STAFF"]:
        for w in data["WEEKENDS"]:
            constraint1 = [employee_dv[s, ((7 * w) - 1), t]
                        for t in data["SHIFTS"]]
            constraint2 = [employee_dv[s, (7 * w), t]
                        for t in data["SHIFTS"]]
            
            model.Add(sum(constraint1) + sum(constraint2) <= 2 * weekend_dv[s, w])
            model.Add(sum(constraint1) + sum(constraint2) >= weekend_dv[s, w])

        staff = [item for item in data["SECTION_STAFF"] if item[0] == s][0]
        max_weekends = staff[7]
        constraint3 = [weekend_dv[s, w]
                        for w in data["WEEKENDS"]]

        model.Add(sum(constraint3) <= max_weekends)

# days off
def days_off(model,
                data,
                employee_dv):
    for s in data["STAFF"]:
        requests = [item for item in data["SECTION_DAYS_OFF"] if item[0] == s][0][1:]
        print(requests)
        for d in requests:
            for t in data["SHIFTS"]:
                model.Add(employee_dv[s, d + 1, t] == 0)

# cover requirement
def coverage(model,
                data,
                employee_dv,
                above_dv,
                below_dv,
                scenarios):
    for d in data["DAYS"]:
        for t in data["SHIFTS"]:
            for k in scenarios:
                requirement = [item for item in data[f"SECTION_COVER{k}"] if item[0] == d - 1 and item[1] == t][0]
                coverage_req = requirement[2]
                constraint1 = [employee_dv[s, d, t]
                            for s in data["STAFF"]]
                model.Add(sum(constraint1) - above_dv[d, t, k] + below_dv[d, t, k] == coverage_req)

# cover requirement
def coverage2(model,
                data,
                employee_dv,
                above_dv,
                below_dv,
                add_dv,
                subtract_dv,
                scenarios):
    for d in data["DAYS"]:
        for t in data["SHIFTS"]:
            for k in scenarios:
                requirement = [item for item in data[f"SECTION_COVER{k}"] if item[0] == d - 1 and item[1] == t][0]
                coverage_req = requirement[2]
                constraint1 = [employee_dv[s, d, t]
                            for s in data["STAFF"]]
                model.Add(sum(constraint1) - above_dv[d, t, k] + below_dv[d, t, k] + add_dv[d, t, k] - subtract_dv[d, t, k ] == coverage_req)
            
# add_dv
def add_staff(model,
                data,
                add_dv,
                below_dv,
                scenarios):
    for d in data["DAYS"]:
        for t in data["SHIFTS"]:
            for k in scenarios:
                model.Add(add_dv[d, t, k] <= below_dv[d, t, k])

# add_dv
def remove_staff(model,
                data,
                subtract_dv,
                above_dv,
                scenarios):
    for d in data["DAYS"]:
        for t in data["SHIFTS"]:
            for k in scenarios:
                model.Add(subtract_dv[d, t, k] <= above_dv[d, t, k])

# days off
def days_off(model,
                data,
                employee_dv):
    for s in data["STAFF"]:
        requests = [item for item in data["SECTION_DAYS_OFF"] if item[0] == s][0][1:]
        for d in requests:
            for t in data["SHIFTS"]:
                model.Add(employee_dv[s, d + 1, t] == 0)