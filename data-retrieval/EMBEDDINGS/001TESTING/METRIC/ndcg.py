import numpy as np
import csv

def dcg_at_k(r, k):
    r = np.asfarray(r)[:k]
    if r.size:
        return np.sum(np.divide(np.power(2, r) - 1, np.log2(np.arange(2, r.size + 2))))
    return 0.

def ndcg_at_k(r, k):
    idcg = dcg_at_k(sorted(r, reverse=True), k)
    if not idcg:
        return 0.
    # 4 decimal places
    return round(dcg_at_k(r, k) / idcg, 3)

def precision_at_k(relevance_scores, k):
    relevant_count = sum(relevance_scores[:k])
    return relevant_count / k if k != 0 else 0


def compute_metrics(category, r_alb, r_ber, k_values):
    results_dict_alb = {}
    results_dict_ber = {}
    for k in k_values:
        results_dict_alb[f"NDCG@{k}"] = ndcg_at_k(r_alb, k)
        results_dict_alb[f"Precision@{k}"] = precision_at_k(r_alb, k)
        results_dict_ber[f"NDCG@{k}"] = ndcg_at_k(r_ber, k)
        results_dict_ber[f"Precision@{k}"] = precision_at_k(r_ber, k)
    
    return results_dict_alb, results_dict_ber

categories = {
    "CULTURA": ([1,0,1,1,0,1,0,1,0,0], [1,1,1,1,1,0,0,0,0,0]),
    "FUNICULAR": ([0,1,1,1,0,0,1,1,0,0], [1,1,0,1,1,1,0,0,0,0]),
    "MÚSICA": ([1,1,0,0,0,0,1,1,0,1], [1,1,0,0,0,1,1,1,0,0]),
    "POLÍTICA": ([1,1,1,1,0,0,1,0,0,0], [1,1,1,0,1,0,0,1,0,0]),
    "RELIGIÃO": ([1,1,0,0,0,0,1,0,1,1], [1,1,0,0,0,0,0,1,1,1]),
    "SPORTING DA COVILHÃ": ([1,1,1,1,1,0,0,0,0,0], [1,1,1,1,1,0,0,0,0,0]),
    "UBI": ([1,1,1,1,0,1,0,0,0,0], [1,1,1,1,1,0,0,0,0,0]),
    "PORTAGENS": ([1,1,1,1,0,0,1,0,0,0], [1,1,1,1,0,0,0,0,1,0]),
    "ACIDENTES": ([1,1,1,1,1,0,0,0,0,0], [1,1,1,1,1,0,0,0,0,0]),
    "MATERNIDADE": ([1,1,1,1,1,0,0,0,0,0], [1,1,1,0,0,1,1,0,0,0])
}

k_values = [5]

for model in ['Albertina', 'BERTimbau']:
    rows = []
    for category, (r_alb, r_ber) in categories.items():
        alb_metrics, ber_metrics = compute_metrics(category, r_alb, r_ber, k_values)
        for k in k_values:
            if model == 'Albertina':
                rows.append((category, alb_metrics[f"Precision@{k}"], alb_metrics[f"NDCG@{k}"]))
            else:
                rows.append((category, ber_metrics[f"Precision@{k}"], ber_metrics[f"NDCG@{k}"]))

    with open(f'results_{model.lower()}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Category", "Precision@5", "NDCG@5"])
        writer.writerows(rows)
