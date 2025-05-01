#!/bin/bash

python sa_suite/scripts/dataset_states_to_obs.py --dataset demos/1746127718_948951/demo.hdf5 --output_name image_dense.hdf5 --done_mode 2 --camera_names agentview robot0_eye_in_hand --camera_height 84 --camera_width 84
