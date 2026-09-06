# Operating modes

Four, not two. A mode is defined by **who holds the control loop**.

## 1. Dev-Terminal
ECC only. Operator at a terminal. Frontier models. Building, reviewing, planning.
No on-device weights in the loop.

## 2. Sovereign-Edge
Prime Agent only, on-device weights only, no network. Full autonomy on Alpha.
This is the mode that has to work when the network doesn't.

## 3. Prime-with-Claude-as-Query
Prime Agent holds the loop and stays in control. When it hits a sub-question
beyond the 9B, it calls Claude **as a subprocess**, takes the answer back, and
continues. Claude never holds the loop in this mode.

## 4. Hybrid-Auditor
Post-hoc. The cross-auditor runs over combined traces from both harnesses,
looking for drift between what was declared and what actually ran.

---

**Mode is not model.** Naming a model does not tell you the mode. Naming the
mode tells you who is deciding what happens next.
