# exec(open(r"D:\develop\roBaLow\pcb\v2R-Low\roba_R_outerline.py").read())
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

sw1_x, sw1_y = get_ref_pos_mm("SW17")
right_x = sw1_x + sw_mgn_x

u1_x, u1_y = get_ref_pos_mm("U1")
top_y = u1_y + u1_mgn_y

dsw_x, _ = get_ref_pos_mm("SW21")
left_x = dsw_x - dsw_mgn_x

_, sw23_y = get_ref_pos_mm("SW21")
_, sw4_y = get_ref_pos_mm("SW20")
sw_m_y = max(sw23_y, sw4_y)
bottom_y = sw_m_y + sw_mgn_y

top_left = (left_x, top_y)
top_right = (right_x, top_y)
bottom_right = (right_x, bottom_y)

ms_x, ms_y = get_ref_pos_mm("J1")
sw16_x, _ = get_ref_pos_mm("SW16")
sw16_x_mgn = 10
ms_x_mgn = 2.2
ms_y_mgn = -25
ms_1 = (ms_x - ms_x_mgn, bottom_y)
ms_2 = (ms_x - ms_x_mgn, bottom_y + ms_y_mgn)
ms_3 = (sw16_x + sw16_x_mgn, bottom_y + ms_y_mgn)
ms_4 = (sw16_x + sw16_x_mgn, bottom_y)

bottom_left = (left_x, bottom_y)


pts_mm = [
    top_left,
    top_right,
    bottom_right,
    ms_1,
    ms_2,
    ms_3,
    ms_4,
    bottom_left,
]
for pt in pts_mm:
    print("pt:", pt)


clear_edge_cuts(board)

draw_outerline(pts_mm)

pcbnew.Refresh()
# %%
