"""
utils.py  –  Helper utilities for the Nonogram CSP homework.

Public API
----------
ROW_CLUES, COL_CLUES          : puzzle definition
build_nonogram_csp(r, c)      : construct a NonogramCSP instance
get_valid_arrangements(clue, length) : enumerate all valid binary lines
is_line_possible(values, clue)       : feasibility check for partial lines
make_animation(csp, logger, ...)     : render solving animation (HTML / GIF)
"""

from __future__ import annotations

from typing import List, Tuple, Optional
from itertools import product

import numpy as np
from models import NonogramCSP, StepLogger, Cell

# ---------------------------------------------------------------------------
# Puzzles definition
# ---------------------------------------------------------------------------

ROW_CLUES_1 = [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
]

COL_CLUES_1 = [
    [1, 1, 1, 1],
    [1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1],
    [1, 1],
    [1, 1, 1, 1],
    [1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
]
ROW_CLUES_2 = [
    (12,), (2,2), (1,8,1), (1,2,2,1),
    (1,1,4,1,1), (1,1,2,2,1,1), (1,1,1,1,1,1), (1,1,1,1,1,1),
    (1,1,2,2,1,1), (1,1,4,1,1), (1,2,2,5), (1,8,1,1),
    (2,1,1,1), (5,3,1,1), (8,1),
]

COL_CLUES_2 = [
    (12,), (2,2), (1,8,1), (1,2,2,1),
    (1,1,4,1,1), (1,1,2,2,1,2), (1,1,1,1,1,1), (1,1,1,1,1,1),
    (1,1,2,2,1,1), (1,1,4,1,1), (1,2,2,1), (1,8,1),
    (2,1), (9,1), (1,), (4,), (1,), (1,3), (1,), (4,),
]

# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def build_nonogram_csp(
    row_clues: List[Tuple[int, ...]],
    col_clues: List[Tuple[int, ...]],
) -> NonogramCSP:
    """Construct a NonogramCSP from row and column clues."""
    N = len(row_clues)
    M = len(col_clues)
    return NonogramCSP(N, M, row_clues, col_clues)


# ---------------------------------------------------------------------------
# Core helpers (provided to students)
# ---------------------------------------------------------------------------

def _clue_to_blocks(line: List[int]) -> Tuple[int, ...]:
    """Extract the run-length clue from a fully-assigned binary line."""
    blocks, in_block = [], False
    current = 0
    for v in line:
        if v == 1:
            current += 1
            in_block = True
        else:
            if in_block:
                blocks.append(current)
                current = 0
                in_block = False
    if in_block:
        blocks.append(current)
    return tuple(blocks) if blocks else (0,)


def get_valid_arrangements(
    clue: Tuple[int, ...],
    length: int,
) -> List[List[int]]:
    """
    Return every binary list of *length* that satisfies *clue*.

    Parameters
    ----------
    clue : tuple of int
        Block lengths, e.g. (2, 1).  Use (0,) for an all-empty line.
    length : int
        Total number of cells in the line.

    Returns
    -------
    list of list[int]
        Each inner list has *length* elements from {0, 1}.

    Examples
    --------
    >>> get_valid_arrangements((2, 1), 5)
    [[1,1,0,1,0], [1,1,0,0,1], [0,1,1,0,1]]
    """
    # Normalise empty clue
    normalised = tuple(clue) if clue != (0,) else ()

    # Minimum length needed
    if normalised:
        min_len = sum(normalised) + len(normalised) - 1
    else:
        min_len = 0

    if min_len > length:
        return []

    results: List[List[int]] = []

    def _place(blocks, pos, current):
        """Recursively place each block starting at pos."""
        if not blocks:
            # Fill the rest with zeros
            full = current + [0] * (length - len(current))
            results.append(full)
            return
        block = blocks[0]
        rest  = blocks[1:]
        # Latest start position for this block so that the remaining
        # blocks can still fit
        if rest:
            min_remaining = sum(rest) + len(rest)
        else:
            min_remaining = 0
        latest_start = length - block - min_remaining

        for start in range(pos, latest_start + 1):
            # Zeros before the block
            prefix = [0] * (start - len(current))
            # The block itself
            block_cells = [1] * block
            new_current = current + prefix + block_cells
            # Gap after block (required unless this is the last block)
            next_pos = start + block + (1 if rest else 0)
            _place(rest, next_pos, new_current)

    _place(list(normalised), 0, [])
    return results


def is_line_possible(values: List[int], clue: Tuple[int, ...]) -> bool:
    """
    Return True if the partial line *values* can still satisfy *clue*.

    Parameters
    ----------
    values : list of int
        Current cell values.  Use -1 for unassigned cells.
    clue : tuple of int
        The target clue, e.g. (2, 1).  Use (0,) for an all-empty line.

    Returns
    -------
    bool
        True if there exists at least one valid arrangement of *clue*
        that is consistent with every assigned cell in *values*.
    """
    length = len(values)
    for arr in get_valid_arrangements(clue, length):
        if all(values[k] == -1 or values[k] == arr[k] for k in range(length)):
            return True
    return False


# ---------------------------------------------------------------------------
# Animation
# ---------------------------------------------------------------------------
def make_animation(
    csp: NonogramCSP,
    logger: StepLogger,
    fps: int = 8,
    last_k: Optional[int] = None,
    stride: int = 1,
):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        from matplotlib.animation import FuncAnimation
        from IPython.display import HTML, display
    except ImportError:
        print("matplotlib / IPython not available – skipping animation.")
        return

    all_events = logger.events

    # ── Split into pre-window and animation window ─────────────────────────
    if last_k is not None and last_k < len(all_events):
        pre_events  = all_events[:-last_k]
        anim_events = all_events[-last_k:]
    else:
        pre_events  = []
        anim_events = all_events

    anim_events = anim_events[::stride]

    if not anim_events:
        print("No events to animate.")
        return

    N, M = csp.N, csp.M

    # ── Silently replay pre-events → correct starting grid ─────────────────
    grid = np.full((N, M), -1, dtype=int)
    for evt in pre_events:
        r, c = evt.cell
        if evt.action == "assign":
            grid[r, c] = evt.value
        elif evt.action == "backtrack":
            grid[r, c] = -1

    # ── Build frames ────────────────────────────────────────────────────────
    frames = []
    # FIX 2: precompute running assign/backtrack counts so update() is O(1)
    assigns_so_far    = sum(1 for e in pre_events if e.action == "assign")
    backtracks_so_far = sum(1 for e in pre_events if e.action == "backtrack")
    for evt in anim_events:
        r, c = evt.cell
        if evt.action == "assign":
            grid[r, c] = evt.value
            assigns_so_far += 1
        elif evt.action == "backtrack":
            grid[r, c] = -1
            backtracks_so_far += 1
        frames.append((grid.copy(), evt, assigns_so_far, backtracks_so_far))

    # ── Palette ─────────────────────────────────────────────────────────────
    DARK       = "#1B2631"
    FILLED     = "#2ECC71"
    EMPTY_C    = "#ECF0F1"
    UNASSIGNED = "#2C3E50"
    ACT_ASSIGN = "#F1C40F"
    ACT_BT     = "#E74C3C"
    CLUE_BG    = "#17202A"
    CLUE_FG    = "#BDC3C7"
    GRID_LINE  = "#AAB7B8"

    # ── Layout ───────────────────────────────────────────────────────────────
    clue_rows = max(len(c) for c in csp.col_clues)
    clue_cols = max(len(c) for c in csp.row_clues)
    CELL = 0.7

    fig_w = (M + clue_cols + 0.6) * CELL
    fig_h = (N + clue_rows + 0.8) * CELL
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), facecolor=DARK)
    ax.set_facecolor(DARK)
    ax.set_aspect("equal")
    ax.axis("off")

    total_cols = clue_cols + M
    total_rows = clue_rows + N
    ax.set_xlim(-0.15, total_cols + 0.15)
    ax.set_ylim(-0.25, total_rows + 0.5)

    # ── Clue backgrounds ─────────────────────────────────────────────────────
    ax.add_patch(mpatches.FancyBboxPatch(
        (0, N), clue_cols + M, clue_rows,
        boxstyle="square,pad=0", linewidth=0,
        facecolor=CLUE_BG, zorder=0,
    ))
    ax.add_patch(mpatches.FancyBboxPatch(
        (0, 0), clue_cols, N,
        boxstyle="square,pad=0", linewidth=0,
        facecolor=CLUE_BG, zorder=0,
    ))

    # ── Clue numbers ─────────────────────────────────────────────────────────
    for j, clue in enumerate(csp.col_clues):
        for k, v in enumerate(clue):
            row_pos = clue_rows - len(clue) + k
            ax.text(
                clue_cols + j + 0.5,
                total_rows - row_pos - 0.5,
                str(v),
                ha="center", va="center",
                fontsize=8, fontweight="bold", color=CLUE_FG,
            )

    for i, clue in enumerate(csp.row_clues):
        for k, v in enumerate(clue):
            col_pos = clue_cols - len(clue) + k
            ax.text(
                col_pos + 0.5,
                total_rows - clue_rows - i - 0.5,
                str(v),
                ha="center", va="center",
                fontsize=8, fontweight="bold", color=CLUE_FG,
            )

    # ── Grid cell patches ─────────────────────────────────────────────────────
    patches = {}
    for i in range(N):
        for j in range(M):
            x = clue_cols + j
            y = total_rows - clue_rows - i - 1
            v = grid[i, j]   # FIX 1: use pre-computed starting grid

            if v == 1:
                init_color = FILLED
            elif v == 0:
                init_color = EMPTY_C
            else:
                init_color = UNASSIGNED

            rect = mpatches.FancyBboxPatch(
                (x + 0.04, y + 0.04), 0.92, 0.92,
                boxstyle="round,pad=0.03",
                linewidth=0, facecolor=init_color, zorder=1,
            )
            ax.add_patch(rect)
            patches[(i, j)] = rect

    # ── Grid lines ────────────────────────────────────────────────────────────
    for i in range(N + 1):
        y  = total_rows - clue_rows - i
        lw = 1.4 if (i % 5 == 0) else 0.4
        ax.plot([clue_cols, clue_cols + M], [y, y],
                color=GRID_LINE, linewidth=lw, zorder=2)
    for j in range(M + 1):
        x  = clue_cols + j
        lw = 1.4 if (j % 5 == 0) else 0.4
        ax.plot([x, x], [total_rows - clue_rows - N, total_rows - clue_rows],
                color=GRID_LINE, linewidth=lw, zorder=2)

    # ── Progress bar ──────────────────────────────────────────────────────────
    BAR_Y    = -0.18
    BAR_H    = 0.08
    bar_bg   = mpatches.Rectangle((0, BAR_Y), total_cols, BAR_H,
                                   linewidth=0, facecolor="#2C3E50", zorder=3)
    bar_fill = mpatches.Rectangle((0, BAR_Y), 0, BAR_H,
                                   linewidth=0, facecolor=FILLED, zorder=4)
    ax.add_patch(bar_bg)
    ax.add_patch(bar_fill)

    # ── Title ─────────────────────────────────────────────────────────────────
    title_obj = ax.text(
        total_cols / 2, total_rows + 0.35,
        "", ha="center", va="bottom",
        fontsize=8.5, color=CLUE_FG, fontweight="bold",
    )

    # ── Update ────────────────────────────────────────────────────────────────
    def update(frame_idx):
        # FIX 3: counts are precomputed in frames — no rescan needed
        grid_f, evt, n_assigns, n_backtracks = frames[frame_idx]
        r_act, c_act = evt.cell

        for i in range(N):
            for j in range(M):
                v      = grid_f[i, j]
                active = (i == r_act and j == c_act)

                if active:
                    color = ACT_ASSIGN if evt.action == "assign" else ACT_BT
                elif v == 1:
                    color = FILLED
                elif v == 0:
                    color = EMPTY_C
                else:
                    color = UNASSIGNED

                patches[(i, j)].set_facecolor(color)

        bar_fill.set_width(total_cols * (frame_idx + 1) / len(frames))
        title_obj.set_text(
            f"Step {frame_idx+1}/{len(frames)}   "
            f"action={evt.action}   cell={evt.cell}   val={evt.value}   "
            f"assigns={n_assigns}   backtracks={n_backtracks}"
        )
        return list(patches.values()) + [bar_fill, title_obj]

    anim = FuncAnimation(
        fig, update, frames=len(frames),
        interval=int(1000 / fps), blit=False,
    )
    plt.tight_layout(pad=0.4)
    try:
        html = anim.to_jshtml()
        plt.close(fig)
        display(HTML(html))
    except Exception:
        plt.show()