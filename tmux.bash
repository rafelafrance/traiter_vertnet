#!/bin/bash

SESSION="vertnet"
TRAIT="~/work/traiter"

tmux new -s $SESSION -d
tmux rename-window -t $SESSION vert
tmux send-keys -t $SESSION "cd $TRAIT/vertnet" C-m
tmux send-keys -t $SESSION "vrun .venv" C-m
tmux send-keys -t $SESSION "git status" C-m

tmux new-window -t $SESSION
tmux rename-window -t $SESSION traiter
tmux send-keys -t $SESSION "cd $TRAIT/traiter" C-m
tmux send-keys -t $SESSION "vrun .venv" C-m
tmux send-keys -t $SESSION "git status" C-m

tmux new-window -t $SESSION

tmux select-window -t vert:1
tmux attach -t $SESSION
