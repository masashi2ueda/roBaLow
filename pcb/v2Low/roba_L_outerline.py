# exec(open(r"D:\develop\roBaLow\pcb\v2Low\roba_L_outerline.py").read())
import pcbnew
import math

board = pcbnew.GetBoard()

def nm_to_mm(nm):
    return nm / 1_000_000.0

def mm_to_nm(mm):
    return int(round(mm * 1_000_000.0))


def get_ref_pos_mm(name):
    ref = board.FindFootprintByReference(name)
    pos = ref.GetPosition()
    return nm_to_mm(pos.x), nm_to_mm(pos.y)



def draw_outerline(pts_mm):
    for i in range(len(pts_mm)):
        x1, y1 = pts_mm[i]
        x2, y2 = pts_mm[(i + 1) % len(pts_mm)]
        x1 = mm_to_nm(x1)
        y1 = mm_to_nm(y1)
        x2 = mm_to_nm(x2)
        y2 = mm_to_nm(y2)

        # KiCad は整数座標（nm）なので丸めて int 化
        x1 = int(round(x1))
        y1 = int(round(y1))
        x2 = int(round(x2))
        y2 = int(round(y2))
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetLayer(pcbnew.Edge_Cuts)
        seg.SetStart(pcbnew.VECTOR2I(x1, y1))
        seg.SetEnd(pcbnew.VECTOR2I(x2, y2))
        board.Add(seg)


def clear_edge_cuts(board):
    for d in list(board.GetDrawings()):
        if d.GetLayer() == pcbnew.Edge_Cuts:
            board.Remove(d)


# =======================================
# Pad の座標を取得
# =======================================
sw_mgn_x = 12
sw_mgn_y = 10
u1_mgn_y = 0
dsw_mgn_x = 0

sw1_x, sw1_y = get_ref_pos_mm("SW1")
left_x = sw1_x - sw_mgn_x
u1_x, u1_y = get_ref_pos_mm("U1")
top_y = u1_y + u1_mgn_y
dsw_x, _ = get_ref_pos_mm("SW24")
right_x = dsw_x + dsw_mgn_x

_, sw23_y = get_ref_pos_mm("SW23")
_, sw4_y = get_ref_pos_mm("SW4")
sw_m_y = max(sw23_y, sw4_y)
bottom_y = sw_m_y + sw_mgn_y


pts_mm = [
    (left_x, top_y),
    (right_x, top_y),
    (right_x, bottom_y),
    (left_x, bottom_y),
]
for pt in pts_mm:
    print("pt:", pt)


clear_edge_cuts(board)

draw_outerline(pts_mm)

pcbnew.Refresh()
