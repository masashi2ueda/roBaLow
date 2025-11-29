# exec(open(r"D:\develop\roBaLow\pcb\v2R-Low\roba_R_position.py").read())
import pcbnew


board = pcbnew.GetBoard()

pitch_x = 17.0  # 横ピッチ mm
pitch_y = 17.0  # 縦ピッチ mm
start_x, start_y = 250, 50  # 原点座標
# ダイオードのオフセット
diode_offset_y = -5
diode_offset_x = -2

def nm_to_mm(nm):
    return nm / 1_000_000.0

def mm_to_nm(mm):
    return int(round(mm * 1_000_000.0))


def get_ref_pos_mm(name):
    ref = board.FindFootprintByReference(name)
    pos = ref.GetPosition()
    return nm_to_mm(pos.x), nm_to_mm(pos.y)

def set_swith_diode(no, x, y, zrot_deg=0):
    ref = f"SW{no}"
    module = board.FindFootprintByReference(ref)
    module.SetPosition(pcbnew.VECTOR2I_MM(x, y))
    if zrot_deg != 0:
        module.SetOrientationDegrees(zrot_deg)

    ref = f"D{no}"
    module = board.FindFootprintByReference(ref)
    module.SetPosition(pcbnew.VECTOR2I_MM(x + diode_offset_x, y + diode_offset_y))


base_x = start_x
base_y = start_y
# 1列目
for c, sw_i in zip(range(4), [17, 18, 19, 20]):
    set_swith_diode(sw_i, base_x, base_y + c * pitch_y)
base_x -= pitch_x

# 2列目
offset_y = -1 * pitch_y / 2  # ずらし量 mm
for c, sw_i in zip(range(3), [13, 14, 15]):
    set_swith_diode(sw_i, base_x, base_y + c * pitch_y + offset_y)
base_x -= pitch_x

# 3列目
offset_y = -2 * pitch_y / 2  # ずらし量 mm
for c, sw_i in zip(range(3), [9, 10, 11]):
    set_swith_diode(sw_i, base_x, base_y + c * pitch_y + offset_y)
base_x -= pitch_x

# 4列目
offset_y = -1.5 * pitch_y / 2  # ずらし量 mm
for c, sw_i in zip(range(3), [5, 6, 7]):
    set_swith_diode(sw_i, base_x, base_y + c * pitch_y + offset_y)
base_x -= pitch_x

# 5列目
offset_y = -1 * pitch_y / 2  # ずらし量 mm
for c, sw_i in zip(range(3), [1, 2, 3]):
    set_swith_diode(sw_i, base_x, base_y + c * pitch_y + offset_y)
base_x -= pitch_x

# 6列目
offset_y = -1 * pitch_y / 2  + pitch_y # ずらし量 mm
for c, sw_i in zip(range(2), [4, 8]):
    set_swith_diode(sw_i, base_x, base_y + c * pitch_y + offset_y)

# promicro
module = board.FindFootprintByReference("U1")
# print("U1:", module)
U1_y = 20 # ずらし量 mm
U1_x_offset = -3
module.SetPosition(pcbnew.VECTOR2I_MM(base_x + U1_x_offset, U1_y))

# バッテリー
module = board.FindFootprintByReference("BT1")
bt_y = 40 # ずらし量 mm
bt_x_offset = -5
module.SetPosition(pcbnew.VECTOR2I_MM(base_x + bt_x_offset, bt_y))

# スイッチ
module = board.FindFootprintByReference("SW21")
U1_y = 80 # ずらし量 mm
U1_x_offset = -15
module.SetOrientationDegrees(90)
module.SetPosition(pcbnew.VECTOR2I_MM(base_x + U1_x_offset, U1_y))

# 親指1
xl1 = 50
xl2 = 50
base_xl = 102
base_yl = 95
dx = base_xl - xl1
dy = base_yl - xl2
base_x = start_x - dx
base_y = start_y + dy
# set_swith_diode(16, base_x, base_y)

# 親指2
base_x -= 17
base_y += 2
set_swith_diode(16, base_x, base_y)

# 親指3
base_x -= 17
base_y += 2
set_swith_diode(12, base_x, base_y)

# mouse
org_sw_x, org_sw_y = 205.53, 133.253749
org_ms_x, org_ms_y = 189.625, 131.35
org_dx = org_ms_x - org_sw_x
org_dy = org_ms_y - org_sw_y
sw20_x, sw20_y = get_ref_pos_mm("SW20")
ms_x = sw20_x + org_dx
ms_y = sw20_y + org_dy
module = board.FindFootprintByReference("J1")
module.SetPosition(pcbnew.VECTOR2I_MM(ms_x, ms_y))

pcbnew.Refresh()
