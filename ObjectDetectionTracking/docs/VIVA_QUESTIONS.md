# Viva Questions and Short Answers

1. **What is OpenCV?** A computer-vision library used here for video capture, drawing, display, and keyboard input.
2. **What is object detection?** Finding object locations and classes in an image.
3. **What is tracking?** Maintaining an object's identity across video frames.
4. **What is YOLO?** A one-stage neural detector that predicts boxes and classes in a single inference pass.
5. **Why use YOLOv8n?** Nano is small and generally faster for real-time beginner projects.
6. **What is a bounding box?** A rectangle, commonly `(x1,y1,x2,y2)`, enclosing an object.
7. **What is confidence?** The model's score that a predicted object/class is correct.
8. **What does a confidence threshold do?** It removes weak predictions below the selected score.
9. **What is NMS?** Non-maximum suppression removes duplicate overlapping detections; YOLO applies it during prediction.
10. **What is IoU?** Intersection over Union: overlap area divided by combined area of two boxes.
11. **Why is IoU used in SORT?** It measures whether a new detection likely belongs to a predicted track.
12. **What does SORT mean?** Simple Online and Realtime Tracking.
13. **What are SORT's two core methods?** Kalman filtering for motion prediction and Hungarian assignment for association.
14. **What is a Kalman filter?** A recursive estimator that predicts state and corrects it using noisy measurements.
15. **What state does this SORT filter use?** Box centre, area, aspect ratio, and velocities for centre/area.
16. **What is Hungarian assignment?** An algorithm that finds the best one-to-one assignment from a cost matrix.
17. **How is a tracking ID created?** An unmatched detection creates a tracker with the next incrementing integer.
18. **Does the ID equal the class ID?** No; tracking IDs identify instances, while class IDs identify categories.
19. **What is `max_age`?** Frames an unmatched track may survive before removal.
20. **What is `min_hits`?** Matches required before a new track is displayed as confirmed.
21. **What is Deep SORT?** SORT extended with appearance embeddings, helping preserve IDs through occlusions.
22. **Why can SORT switch IDs?** It has no appearance features and may confuse nearby/occluded boxes.
23. **What is FPS?** Frames processed or displayed per second.
24. **How is FPS measured here?** Reciprocal of elapsed time between loop iterations, then smoothed.
25. **What does `cv2.VideoCapture` do?** Opens a camera or video and reads frames sequentially.
26. **Why release a capture?** It frees the camera/file handle for other programs.
27. **Why call `destroyAllWindows`?** It closes OpenCV GUI windows cleanly.
28. **Why resize frames?** Smaller frames usually give faster inference but can reduce detection accuracy.
29. **What is CUDA acceleration?** Using an NVIDIA GPU to execute supported deep-learning operations faster.
30. **Why use NumPy?** It efficiently stores and computes boxes, matrices, and arrays.
31. **Why use classes in Python?** They keep model/tracker state and behavior organized and reusable.
32. **What happens on an empty video frame?** The application stops for a file or continues trying for a camera.
33. **How can person counting be added?** Keep a set of unique person track IDs or count line crossings.
34. **Why is line crossing better than raw IDs for traffic count?** It counts a defined event instead of all objects merely visible.
35. **What causes poor detection?** Low light, motion blur, occlusion, unusual viewpoints, low resolution, or classes absent from training data.
