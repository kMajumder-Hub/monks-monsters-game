import streamlit as st

TOTAL_MONKS = 3
TOTAL_MONSTERS = 3
BOAT_CAPACITY = 2

# --- Game logic ---
def bank_safe(monks, monsters):
    return monks == 0 or monks >= monsters

def state_safe(Lm, Lx):
    Rm = TOTAL_MONKS - Lm
    Rx = TOTAL_MONSTERS - Lx
    return bank_safe(Lm, Lx) and bank_safe(Rm, Rx)

def reset_game():
    st.session_state.Lm = TOTAL_MONKS
    st.session_state.Lx = TOTAL_MONSTERS
    st.session_state.boat = 0  # 0=left, 1=right
    st.session_state.moves = 0
    st.session_state.msg = "Game reset."

def apply_move(m, x):
    Lm, Lx, boat = st.session_state.Lm, st.session_state.Lx, st.session_state.boat

    if m < 0 or x < 0:
        st.session_state.msg = "Invalid move."
        return
    if m + x == 0:
        st.session_state.msg = "Boat must carry at least 1."
        return
    if m + x > BOAT_CAPACITY:
        st.session_state.msg = f"Boat capacity is {BOAT_CAPACITY}."
        return

    if boat == 0:  # left -> right
        if m > Lm or x > Lx:
            st.session_state.msg = "Not enough people on left bank."
            return
        nLm, nLx = Lm - m, Lx - x
    else:          # right -> left
        Rm, Rx = TOTAL_MONKS - Lm, TOTAL_MONSTERS - Lx
        if m > Rm or x > Rx:
            st.session_state.msg = "Not enough people on right bank."
            return
        nLm, nLx = Lm + m, Lx + x

    if not state_safe(nLm, nLx):
        st.session_state.msg = "Unsafe: monsters outnumber monks on a bank."
        return

    st.session_state.Lm = nLm
    st.session_state.Lx = nLx
    st.session_state.boat = 1 - boat
    st.session_state.moves += 1
    st.session_state.msg = f"Moved: {m} monk(s), {x} monster(s)."

def winners_text():
    return st.session_state.Lm == 0 and st.session_state.Lx == 0 and st.session_state.boat == 1

# --- Session state init ---
if "Lm" not in st.session_state:
    reset_game()

# --- UI ---
st.title("Monks & Monsters River Crossing")

Lm, Lx, boat = st.session_state.Lm, st.session_state.Lx, st.session_state.boat
Rm, Rx = TOTAL_MONKS - Lm, TOTAL_MONSTERS - Lx

col1, col2 = st.columns(2)

with col1:
    st.subheader("Left bank")
    st.write(f"Monks: {Lm}")
    st.write(f"Monsters: {Lx}")

with col2:
    st.subheader("Right bank")
    st.write(f"Monks: {Rm}")
    st.write(f"Monsters: {Rx}")

st.divider()
st.write(f"Boat is on the: **{'Left' if boat == 0 else 'Right'}**")
st.write(f"Moves: {st.session_state.moves}")
st.info(st.session_state.msg)

if winners_text():
    st.success(f"You win in {st.session_state.moves} moves!")
    st.button("Play again", on_click=reset_game)
    st.stop()

st.subheader("Send passengers")

# Common allowed transfers for capacity=2:
# (2,0), (0,2), (1,1), (1,0), (0,1)
moves = [(2,0), (0,2), (1,1), (1,0), (0,1)]

bcols = st.columns(len(moves))
for i, (m, x) in enumerate(moves):
    label = f"{m}M {x}X"
    bcols[i].button(label, on_click=apply_move, args=(m, x))

st.button("Reset", on_click=reset_game)
