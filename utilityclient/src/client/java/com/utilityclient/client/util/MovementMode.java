package com.utilityclient.client.util;

public enum MovementMode {
    WALKING(0xFF93C5FD),
    SPRINTING(0xFF10B981),
    SWIMMING(0xFF06B6D4),
    HORSE(0xFFF59E0B),
    ZOMBIE_HORSE(0xFF84CC16),
    CAMEL(0xFFD97706),
    CAMEL_HUSK(0xFFEA580C),
    ELYTRA(0xFF8B5CF6),
    NAUTILUS(0xFF14B8A6),
    ZOMBIE_NAUTILUS(0xFF22C55E);

    private final int color;

    MovementMode(int color) {
        this.color = color;
    }

    public int getColor() {
        return color;
    }
}
