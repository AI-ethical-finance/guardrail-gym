from __future__ import annotations

def dominates(a: dict, b: dict, keys: list[str]) -> bool:
    ge = all(a.get(k, 0.0) >= b.get(k, 0.0) for k in keys)
    gt = any(a.get(k, 0.0) > b.get(k, 0.0) for k in keys)
    return ge and gt

def pareto_front(rows: list[dict], keys: list[str]) -> list[dict]:
    front = []
    for row in rows:
        dominated = False
        for other in rows:
            if other is row:
                continue
            if dominates(other, row, keys):
                dominated = True
                break
        if not dominated:
            front.append(row)
    return front
