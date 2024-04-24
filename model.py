from ortools.sat.python.cp_model import *
from typing import Dict, List, Tuple

def create_model() -> CpModel:
    return CpModel()

def create_solver(time_seconds: int) -> CpSolver:
    solver = CpSolver()
    solver.parameters.max_time_in_seconds = time_seconds
    solver.parameters.num_search_workers = 4
    return solver

def create_employee_dv(model: CpModel,
                           prefix: str,
                           staff: List[int],
                           days: List[int],
                           shifts: List[int]) -> Dict[Tuple, IntVar]:
    return {(m, d, t):
            model.NewBoolVar(f"{prefix}_staff_{m}_day_{d}_shift_{t}")
            for m in staff
            for d in days
            for t in shifts}

def create_above_coverage_dv(model: CpModel,
                           ub,
                           prefix: str,
                           days: List[int],
                           shifts: List[int],
                           scenarios: List[int]) -> Dict[Tuple, IntVar]:
    return {(d, t, k):
            model.NewIntVar(0, ub, f"{prefix}_day_{d}_shift_{t}_scenario_{k}")
            for d in days
            for t in shifts
            for k in scenarios}

def create_below_coverage_dv(model: CpModel,
                           ub,
                           prefix: str,
                           days: List[int],
                           shifts: List[int],
                           scenarios: List[int]) -> Dict[Tuple, IntVar]:
    
    return {(d, t, k):
            model.NewIntVar(0, ub, f"{prefix}_day_{d}_shift_{t}_scenario_{k}")
            for d in days
            for t in shifts
            for k in scenarios}

def create_weekend_dv(model: CpModel,
                           prefix: str,
                           staff: List[int],
                           weekends: List[int]) -> Dict[Tuple, IntVar]:
    
    return {(d, t):
            model.NewBoolVar(f"{prefix}_staff_{d}_weekend_{t}")
            for d in staff
            for t in weekends}


def create_add_dv(model: CpModel,
                           ub,
                           prefix: str,
                           days: List[int],
                           shifts: List[int],
                           scenarios: List[int]) -> Dict[Tuple, IntVar]:
    
    return {(d, t, k):
            model.NewIntVar(0, ub, f"{prefix}_day_{d}_shift_{t}_scenario_{k}")
            for d in days
            for t in shifts
            for k in scenarios}


def create_subtract_dv(model: CpModel,
                           ub,
                           prefix: str,
                           days: List[int],
                           shifts: List[int],
                           scenarios: List[int]) -> Dict[Tuple, IntVar]:
    
    return {(d, t, k):
            model.NewIntVar(0, ub, f"{prefix}_day_{d}_shift_{t}_scenario_{k}")
            for d in days
            for t in shifts
            for k in scenarios}