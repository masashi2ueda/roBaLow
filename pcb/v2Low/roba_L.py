# exec(open(r"D:\develop\20251109robatest\20251109roBa-main\roBa-main\pcb\v2\roBa_L\roba_L.py").read())
import pcbnew

board = pcbnew.GetBoard()
pitch_x = 17.0  # 横ピッチ mm
pitch_y = 17.0  # 縦ピッチ mm
start_x, start_y = 50, 50  # 原点座標
cols, rows = 2, 4
# r = 1
# c = 0
# ref = f"SW{r * cols + c + 1}"
# module = board.FindFootprintByReference(ref)
# module.SetPosition(pcbnew.VECTOR2I_MM(start_x + c*pitch_x,start_y + r*pitch_y))
# sw1.SetPosition(pcbnew.VECTOR2I_MM(0,0))
# SW1～SW21 を自動整列（7列×3行の例）
# cols, rows = 2, 4
cols, rows = 1, 4
for r in range(rows):
    for c in range(cols):
        ref = f"SW{r * cols + c + 1}"
        module = board.FindFootprintByReference(ref)
        module.SetPosition(pcbnew.VECTOR2I_MM(start_x + c*pitch_x,start_y + r*pitch_y))
pcbnew.Refresh()