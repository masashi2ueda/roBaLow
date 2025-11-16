# exec(open(r"D:\develop\roBaLow\pcb\v2Low\roba_L_position.py").read())
import pcbnew


board = pcbnew.GetBoard()

pitch_x = 17.0  # 横ピッチ mm
pitch_y = 17.0  # 縦ピッチ mm
start_x, start_y = 50, 50  # 原点座標
# ダイオードのオフセット
diode_offset_y = -5
diode_offset_x = -2


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
for c in range(4):
    set_swith_diode(1 + c, base_x, base_y + c * pitch_y)
base_x += pitch_x

# 2列目
offset_y = -1 * pitch_y / 2  # ずらし量 mm
for c in range(4):
    set_swith_diode(5 + c, base_x, base_y + c * pitch_y + offset_y)
base_x += pitch_x

# 3列目
offset_y = -2 * pitch_y / 2  # ずらし量 mm
for c in range(4):
    set_swith_diode(9 + c, base_x, base_y + c * pitch_y + offset_y)
base_x += pitch_x

# 4列目
offset_y = -1.5 * pitch_y / 2  # ずらし量 mm
for c in range(3):
    set_swith_diode(13 + c, base_x, base_y + c * pitch_y + offset_y)
base_x += pitch_x

# 5列目
offset_y = -1 * pitch_y / 2  # ずらし量 mm
for c in range(3):
    set_swith_diode(17 + c, base_x, base_y + c * pitch_y + offset_y)
base_x += pitch_x

# 6列目
offset_y = -1 * pitch_y / 2  + pitch_y # ずらし量 mm
for c in range(2):
    set_swith_diode(21 + c, base_x, base_y + c * pitch_y + offset_y)

# promicro
module = board.FindFootprintByReference("U1")
# print("U1:", module)
U1_y = 20 # ずらし量 mm
U1_x_offset = 3
module.SetPosition(pcbnew.VECTOR2I_MM(base_x + U1_x_offset, U1_y))

# バッテリー
module = board.FindFootprintByReference("B1")
bt_y = 40 # ずらし量 mm
bt_x_offset = 2
module.SetPosition(pcbnew.VECTOR2I_MM(base_x + bt_x_offset, bt_y))

# スイッチ
module = board.FindFootprintByReference("SW24")
U1_y = 80 # ずらし量 mm
U1_x_offset = 15
module.SetOrientationDegrees(-90)
module.SetPosition(pcbnew.VECTOR2I_MM(base_x + U1_x_offset, U1_y))

# 親指1
base_x = 105
base_y = 100
set_swith_diode(16, base_x, base_y)

# 親指2
base_x += 17
base_y += 2
set_swith_diode(20, base_x, base_y)

# 親指3
base_x += 17
base_y += 2
set_swith_diode(23, base_x, base_y)

pcbnew.Refresh()
