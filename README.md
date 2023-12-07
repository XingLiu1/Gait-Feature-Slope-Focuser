# Gait-Feature-Slope-Focuser

A real-time gait events detector base on positive and negtive SSF algorithm. Four gait events (Heel strike, Toes off, Walking stop, Walking start) can be detected from real-time IMU signal using the algorithm.

The accuracy of pulse onset determination was established using a newly created, manually-edited reference IMU signal database. The algorithm detected 98.32% of the Heal Strike(HS) event, 99.10% of the Toes Off(TO) event annotated in the IMU signal. For 96.41% of the 1427 gaits in the reference database, the difference between the manually-edited and SSF algorithm determined pulse onset was less than or equal to 20 ms. 75.62% of Walking stop or Walking start events are detected within 5 frame comparing to the ground truth annotated by none real-time methods. 
