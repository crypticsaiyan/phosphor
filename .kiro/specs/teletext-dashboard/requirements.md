# Teletext Dashboard Feature

## Overview
A retro 1980s Ceefax/Oracle-style dashboard displaying live DevOps metrics with authentic teletext aesthetics.

## Acceptance Criteria

### AC1: Dashboard Toggle
- User can toggle dashboard with F1 key
- Dashboard overlays the main chat view
- Pressing F1 again returns to chat

### AC2: Visual Authenticity
- Strict 8-color palette (Black, White, Red, Green, Blue, Cyan, Magenta, Yellow)
- Block graphics characters (█ ▀ ▄ ░)
- Page number display (Page 100)
- Ticking clock with seconds

### AC3: System Metrics
- CPU usage bar graph using psutil
- Memory usage bar graph
- Real-time updates every second

### AC4: Container Status
- Docker container status matrix
- Color-coded health indicators
- Shows running/stopped/unhealthy states

### AC5: Git Integration
- Recent commits displayed as "Breaking News"
- Shows commit hash and message
- Updates on dashboard open

### AC6: Error Ticker
- Scrolling ticker tape at bottom
- Displays recent error logs
- Continuous horizontal scroll animation
