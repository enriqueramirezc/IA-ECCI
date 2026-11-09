import csv
import random
from pathlib import Path
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "emociones_embeddings.csv"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "clusters.png"

CLUSTER_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
                  "#e87ba4", "#008300", "#6250d6", "#e34948"]
CLUSTER_MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]


def load_embeddings(path: Path = DATA_PATH) -> dict[str, npt.NDArray[np.float64]]:
    embeddings: dict[str, npt.NDArray[np.float64]] = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header: palabra,d0,...,d299
        for row in reader:
            if not row:
                continue
            word, *values = row
            embeddings[word] = np.array(values, dtype=np.float64)
    return embeddings

def dist(vec1: npt.NDArray[np.float64], vec2: npt.NDArray[np.float64]) -> float:
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    dot_prod = np.vdot(vec1, vec2)

    dist = float(1.0 - dot_prod / (norm1 * norm2))

    return dist

def kmeans( embeddings: dict[str, npt.NDArray[np.float64]], k: int) -> dict[str, int]:
    words = list(embeddings.keys())
    centroids = [embeddings[p].copy() for p in random.sample(words, k)]

    assignment: dict[str, int] = {}
    while True:
        new_assignment: dict[str, int] = {}
        for p in words:
            distances = [dist(embeddings[p], c) for c in centroids]
            new_assignment[p] = distances.index(min(distances))

        if new_assignment == assignment:
            return assignment
        assignment = new_assignment

        # La implementacion de recalcular los centroides se hizo con ayuda de IA
        for i in range(k):
            members = [embeddings[p] for p in words if assignment[p] == i]
            if members:
                total = np.zeros_like(centroids[i])
                for v in members:
                    total += v / float(np.linalg.norm(v))
                centroids[i] = total / len(members)
            else:
                centroids[i] = embeddings[random.choice(words)].copy()

def hac(embeddings: dict[str, npt.NDArray[np.float64]], level: int = 2) -> dict[str, int]:
    words = list(embeddings.keys())
    n = len(words)

    dist_mat = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dist_mat[i, j] = dist_mat[j, i] = dist(embeddings[words[i]], embeddings[words[j]])

    np.fill_diagonal(dist_mat, np.inf)

    children: dict[int, tuple[int, int]] = {}
    slot_node = list(range(n))
    active = set(range(n))
    next_node = n

    while len(active) > 1:
        i, j = np.unravel_index(np.argmin(dist_mat), dist_mat.shape)
        i, j = int(min(i, j)), int(max(i, j))

        new_row = np.maximum(dist_mat[i], dist_mat[j])

        children[next_node] = (slot_node[i], slot_node[j])
        slot_node[i] = next_node
        next_node += 1
        active.remove(j)

        dist_mat[i, :] = new_row
        dist_mat[:, i] = new_row
        dist_mat[i, i] = np.inf
        dist_mat[j, :] = np.inf
        dist_mat[:, j] = np.inf

    # El cortado de los niveles del HAC se implemento con IA
    groups = [next_node - 1]
    for _ in range(level):
        groups = [c for g in groups for c in children.get(g, (g,))]

    def leaves(node: int) -> list[int]:
        if node not in children:
            return [node]
        left, right = children[node]
        return leaves(left) + leaves(right)

    assignment: dict[str, int] = {}
    for c, node in enumerate(groups):
        for idx in leaves(node):
            assignment[words[idx]] = c
    return assignment


def print_clusters(assignment: dict[str, int]) -> None:
    clusters: dict[int, list[str]] = {}
    for word, c in assignment.items():
        clusters.setdefault(c, []).append(word)
    for c, members in sorted(clusters.items()):
        print(f"Cluster {c}: {', '.join(members)}")

# Las funciones para graficar los resultados se hizo con IA.

def project_2d(embeddings: dict[str, npt.NDArray[np.float64]]) -> dict[str, npt.NDArray[np.float64]]:
    """Proyecta los embeddings a 2D con PCA (SVD) sobre vectores normalizados."""
    words = list(embeddings.keys())
    X = np.array([embeddings[w] / np.linalg.norm(embeddings[w]) for w in words])
    X -= X.mean(axis=0)
    _, _, vt = np.linalg.svd(X, full_matrices=False)
    coords = X @ vt[:2].T
    return {w: coords[i] for i, w in enumerate(words)}


def plot_clusters(ax, coords: dict[str, npt.NDArray[np.float64]],
                  assignment: dict[str, int], title: str) -> None:
    for c in sorted(set(assignment.values())):
        members = [w for w in assignment if assignment[w] == c]
        pts = np.array([coords[w] for w in members])
        ax.scatter(pts[:, 0], pts[:, 1], s=40,
                   color=CLUSTER_COLORS[c % len(CLUSTER_COLORS)],
                   marker=CLUSTER_MARKERS[c % len(CLUSTER_MARKERS)],
                   edgecolors="white", linewidths=0.8,
                   label=f"Cluster {c} ({len(members)})")
        for w, (x, y) in zip(members, pts):
            ax.annotate(w, (x, y), xytext=(3, 3), textcoords="offset points",
                        fontsize=6, color="#555555")
    ax.set_title(title)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.grid(True, color="#e5e5e5", linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(loc="best", fontsize=8, frameon=False)


def plot_results(embeddings: dict[str, npt.NDArray[np.float64]],
                 results: dict[str, dict[str, int]],
                 output: Path | None = OUTPUT_PATH, show: bool = True) -> None:
    coords = project_2d(embeddings)
    fig, axes = plt.subplots(1, len(results), figsize=(9 * len(results), 8),
                             sharex=True, sharey=True, squeeze=False)
    for ax, (title, assignment) in zip(axes[0], results.items()):
        plot_clusters(ax, coords, assignment, title)
    fig.suptitle("Clusters de embeddings (distancia coseno, proyección PCA 2D)")
    fig.tight_layout()
    if output is not None:
        fig.savefig(output, dpi=150)
        print(f"\nGráfica guardada en {output}")
    if show:
        plt.show()


if __name__ == "__main__":
    k = 4
    hac_level = 2  # segundo nivel del dendrograma -> 4 grupos
    embeddings = load_embeddings()

    km = kmeans(embeddings, k)
    hc = hac(embeddings, hac_level)

    print("=== K-means ===")
    print_clusters(km)

    print("\n=== HAC (complete linkage, nivel 2 del dendrograma) ===")
    print_clusters(hc)

    plot_results(embeddings, {
        f"K-means (k={k})": km,
        f"HAC enlace completo (nivel {hac_level} del dendrograma)": hc,
    })
