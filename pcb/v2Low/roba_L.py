# exec(open(r"D:\develop\roBaLow\pcb\v2Low\roba_L.py").read())
import pcbnew

board = pcbnew.GetBoard()
module = board.FindFootprintByReference("U1")
print("U1:", module)

pitch_x = 17.0  # 横ピッチ mm
pitch_y = 17.0  # 縦ピッチ mm
start_x, start_y = 50, 50  # 原点座標

base_x = start_x
base_y = start_y
# 1列目
for c in range(4):
    ref = f"SW{1+c}"
    module = board.FindFootprintByReference(ref)
    module.SetPosition(pcbnew.VECTOR2I_MM(base_x, base_y + c * pitch_y))
base_x += pitch_x

# 2列目
offset_y = -1 * pitch_y / 2  # ずらし量 mm
for c in range(4):
    ref = f"SW{5+c}"
    module = board.FindFootprintByReference(ref)
    module.SetPosition(pcbnew.VECTOR2I_MM(base_x, base_y + c * pitch_y + offset_y))
base_x += pitch_x

# 3列目
offset_y = -2 * pitch_y / 2  # ずらし量 mm
for c in range(4):
    ref = f"SW{9+c}"
    module = board.FindFootprintByReference(ref)
    module.SetPosition(pcbnew.VECTOR2I_MM(base_x, base_y + c * pitch_y + offset_y))
base_x += pitch_x

# 4列目
offset_y = -1.5 * pitch_y / 2  # ずらし量 mm
for c in range(3):
    ref = f"SW{13+c}"
    module = board.FindFootprintByReference(ref)
    module.SetPosition(pcbnew.VECTOR2I_MM(base_x, base_y + c * pitch_y + offset_y))
base_x += pitch_x

# 5列目
offset_y = -1 * pitch_y / 2  # ずらし量 mm
for c in range(3):
    ref = f"SW{17+c}"
    module = board.FindFootprintByReference(ref)
    module.SetPosition(pcbnew.VECTOR2I_MM(base_x, base_y + c * pitch_y + offset_y))

# 6列目
base_x += pitch_x
offset_y = -1 * pitch_y / 2  + pitch_y # ずらし量 mm
for c in range(2):
    ref = f"SW{21+c}"
    module = board.FindFootprintByReference(ref)
    module.SetPosition(pcbnew.VECTOR2I_MM(base_x, base_y + c * pitch_y + offset_y))

# promicro
module = board.FindFootprintByReference("U1")
# print("U1:", module)
U1_y = 25 # ずらし量 mm
U1_x_offset = 5
module.SetPosition(pcbnew.VECTOR2I_MM(base_x + U1_x_offset, U1_y))


# 親指1
base_x = 105
base_y = 100
module = board.FindFootprintByReference("SW16")
module.SetPosition(pcbnew.VECTOR2I_MM(base_x, base_y))

# 親指2
base_x += 17
base_y += 2
zrot_deg = 0
module = board.FindFootprintByReference("SW20")
module.SetPosition(pcbnew.VECTOR2I_MM(base_x, base_y))
module.SetOrientationDegrees(zrot_deg)

# 親指3
base_x += 17
base_y += 2
module = board.FindFootprintByReference("SW23")
module.SetPosition(pcbnew.VECTOR2I_MM(base_x, base_y))


# cols, rows = 2, 4
# r = 1
# c = 0
# ref = f"SW{r * cols + c + 1}"
# module = board.FindFootprintByReference(ref)
# module.SetPosition(pcbnew.VECTOR2I_MM(start_x + c*pitch_x,start_y + r*pitch_y))
# sw1.SetPosition(pcbnew.VECTOR2I_MM(0,0))
# SW1～SW21 を自動整列（7列×3行の例）
# cols, rows = 2, 4
# cols, rows = 1, 4
# for r in range(rows):
#     for c in range(cols):
#         ref = f"SW{r * cols + c + 1}"
#         module = board.FindFootprintByReference(ref)
#         module.SetPosition(pcbnew.VECTOR2I_MM(start_x + c*pitch_x,start_y + r*pitch_y))
pcbnew.Refresh()
