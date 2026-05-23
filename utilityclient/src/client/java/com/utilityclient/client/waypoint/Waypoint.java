package com.utilityclient.client.waypoint;

public record Waypoint(
    String name,
    int x,
    int y,
    int z,
    int color,
    String dimension,
    boolean enabled
) {
}
