#!/bin/bash

# Check if the CT folder exists
ct_folder='../data/all_data/CT'

if [ ! -d "$ct_folder" ]; then
    echo "CT folder '$ct_folder' does not exist."
    exit 1
fi

# Get the list of all image files
ct_files=($(ls "$ct_folder"))

tmux new-session -d -s image_processing

for ct_file in "${ct_files[@]}"
do
    tmux send-keys "python image_metrics.py $ct_file" C-m
    sleep 1 # Add a small delay if needed to manage resource usage
done

# Attach to the tmux session
tmux attach-session -t image_processing

# After detaching, kill the tmux session
tmux send-keys -t image_processing "exit" C-m
tmux kill-session -t image_processing