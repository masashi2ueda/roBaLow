import pcbnew

# === 設定 ===
input_file = "roba_L.kicad_pcb"  # 開いているPCBを対象にする場合はこのままでOK
output_file = "roba_L_17mm.kicad_pcb"
scale = 17.0 / 19.05  # 縮小率 ≒ 0.892

# === 現在開いているボードを取得 ===
board = pcbnew.GetBoard()

# 中心座標を取得（重心付近）
bbox = board.ComputeBoundingBox()
center_x = bbox.Centre().x
center_y = bbox.Centre().y
center = pcbnew.wxPoint(center_x, center_y)

print(f"Center: {center_x/1e6:.2f}mm, {center_y/1e6:.2f}mm")

# === 各フットプリントをスケーリング ===
for module in board.GetModules():
    pos = module.GetPosition()
    new_x = center.x + (pos.x - center.x) * scale
    new_y = center.y + (pos.y - center.y) * scale
    module.SetPosition(pcbnew.wxPoint(int(new_x), int(new_y)))

# === Edge.Cutsや描画ラインもスケーリング ===
for draw_segment in board.GetDrawings():
    if hasattr(draw_segment, "GetStart") and hasattr(draw_segment, "GetEnd"):
        start = draw_segment.GetStart()
        end = draw_segment.GetEnd()
        new_start = pcbnew.wxPoint(center.x + (start.x - center.x) * scale, center.y + (start.y - center.y) * scale)
        new_end = pcbnew.wxPoint(center.x + (end.x - center.x) * scale, center.y + (end.y - center.y) * scale)
        draw_segment.SetStart(new_start)
        draw_segment.SetEnd(new_end)

# === 保存 ===
pcbnew.SaveBoard(output_file, board)
print(f"Saved scaled board as: {output_file}")
