def build_match_graph(pair_metrics: list[dict]) -> dict:
    nodes = sorted({i for pair in pair_metrics for i in pair.get("pair", [])})
    edges = [
        {"source": p["pair"][0], "target": p["pair"][1], "weight": p.get("inlier_count", 0), "inlier_ratio": p.get("inlier_ratio", 0.0)}
        for p in pair_metrics
    ]
    return {"nodes": nodes, "edges": edges}
