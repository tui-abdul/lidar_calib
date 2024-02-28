import open3d as od3
a = od3.io.read_point_cloud("4459.263690480.pcd")
# Visualize cloud and edit
vis = od3.visualization.VisualizerWithEditing()
vis.create_window()
vis.add_geometry(a)
vis.run()
# Picked point #84 (-0.00, 0.01, 0.01) to add in queue.
# Picked point #119 (0.00, 0.00, -0.00) to add in queue.
# Picked point #69 (-0.01, 0.02, 0.01) to add in queue.
vis.destroy_window()
print(vis.get_picked_points()) #[84, 119, 69]