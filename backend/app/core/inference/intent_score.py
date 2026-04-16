"""Intent Priority for Cognet."""

from __future__ import annotations


INTENT_PRIORITY = {
	"ask_next_step": 1.0,
	"ask_status": 0.8,
	"update_progress": 0.7,
	"new_goal": 0.6,
	"general": 0.5,
}