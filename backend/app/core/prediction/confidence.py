"""Prediction confidence helpers for Cognet."""

from __future__ import annotations


def prediction_confidence(pattern: list[str]) -> float:
	if len(pattern) >= 3:
		return 0.9
	if len(pattern) == 2:
		return 0.7
	return 0.5