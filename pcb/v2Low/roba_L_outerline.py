# exec(open(r"D:\develop\roBaLow\pcb\v2Low\roba_L_outerline.py").read())
import pcbnew
import math

board = pcbnew.GetBoard()

def nm_to_mm(nm):
    return nm / 1_000_000.0

def mm_to_nm(mm):
    return int(round(mm * 1_000_000.0))

class Point:
    def __init__(self, x_nm, y_nm):
        self.x_nm = x_nm
        self.y_nm = y_nm

    def __repr__(self):
        return f"({nm_to_mm(self.x_nm):.2f}, {nm_to_mm(self.y_nm):.2f})"
    def to_tuple(self):
        return (self.x_nm, self.y_nm)
    
def get_ref_pos_mm(name):
    ref = board.FindFootprintByReference(name)
    pos = ref.GetPosition()
    return nm_to_mm(pos.x), nm_to_mm(pos.y)


# =======================================
# 凸包（Graham Scan）
# =======================================
def convex_hull(points):
    points = sorted(points)
    if len(points) <= 2:
        return points

    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


# =======================================
# ポリゴンの向き判定（面積）
# 正ならCCW（左回り）／ 負ならCW（右回り）
# =======================================
def polygon_area(points):
    area = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % n]
        area += (x1 * y2 - x2 * y1)
    return area / 2


# =======================================
# ポリゴン拡張（外側マージン）
# ※ ポリゴンは CCW で処理すること
# =======================================
def expand_polygon(points, margin):
    expanded = []
    n = len(points)

    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]

        dx = x2 - x1
        dy = y2 - y1

        length = math.hypot(dx, dy)
        if length == 0:
            continue

        # CCW ポリゴンは (-dy, dx) が必ず外側
        nx = -dy / length
        ny = dx / length

        ex1 = x1 + nx * margin
        ey1 = y1 + ny * margin
        ex2 = x2 + nx * margin
        ey2 = y2 + ny * margin

        expanded.append((ex1, ey1))
        expanded.append((ex2, ey2))

    # 押し出した点群から再び凸包を取ることでキレイな外形に
    return convex_hull(expanded)


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
bottom_y = sw23_y + sw_mgn_y


pts_mm = [
    (left_x, top_y),
    (right_x, top_y),
    (right_x, bottom_y),
    (left_x, bottom_y),
]
for pt in pts_mm:
    print("pt:", pt)

# min_x_mm = 1e+10
# max_x_mm = -1e+10
# min_y_mm = 1e+10
# max_y_mm = -1e+10
# for fp in board.GetFootprints():
#     ref = fp.GetReference()
#     mgn_x_mm = 0
#     mgn_y_mm = 0
#     if "SW" in ref:
#         if ref != "SW24":
#             mgn_x_mm = 10
#             mgn_y_mm = 10
#     # fpname = fp.GetFPID().GetLibItemName()  # フットプリント名
#     # print(ref, fpname)
#     # if ref != "SW1":
#     #     continue
#     bbox = fp.GetBoundingBox()
#     x_mm = nm_to_mm(bbox.GetCenter().x)
#     y_mm = nm_to_mm(bbox.GetCenter().y)
#     for dx in [-mgn_x_mm, mgn_x_mm]:
#         for dy in [-mgn_y_mm, mgn_y_mm]:
#             mgnd_x_mm = x_mm + dx
#             mgnd_y_mm = y_mm + dy
#             if mgnd_x_mm < min_x_mm:
#                 min_x_mm = mgnd_x_mm
#             if mgnd_x_mm > max_x_mm:
#                 max_x_mm = mgnd_x_mm
#             if mgnd_y_mm < min_y_mm:
#                 min_y_mm = mgnd_y_mm
#             add_pt = (x_mm + dx, y_mm + dy)
#             # print("add pt:", add_pt)
#             if min
#             # pts_mm.append(add_pt)
#     # pts_mm.append((x_mm, y_mm))
#     # print("SW1 center:", center_point)
#     # for dx in [-mgn_x, mgn_x]:
#     #     for dy in [-mgn_y, mgn_y]:
#     #         add_pt = Point(center_point.x_nm + dx, center_point.y_nm + dy)
#     #         print("add pt:", add_pt)
#     #         pts.append(add_pt)
#     # pts.append((cx, cy))
#     # print("Center:", cx, cy)
#     # for pad in fp.Pads():
#     #     pos = pad.GetPosition()
#     #     pts.append((pos.x, pos.y))


# # =======================================
# # 凸包取得 → CCW 補正
# # =======================================
# hull_mm = convex_hull(pts_mm)
# print("hull_mm:", hull_mm)
# # CW（時計回り）なら反転して CCW にする（重要！）
# if polygon_area(hull_mm) < 0:
#     hull_mm = list(reversed(hull_mm))
# print("hull_mm:", hull_mm)

# # =======================================
# # 既存の Edge.Cuts をクリア
# # =======================================
clear_edge_cuts(board)

# # =======================================
# # 新しい Edge.Cuts を描く
# # =======================================
# pts_mm = [(40-5, 40-5),
#        (40, 40-5),
#        (40, 40),
#        (40-5, 40),]

draw_outerline(pts_mm)

pcbnew.Refresh()
