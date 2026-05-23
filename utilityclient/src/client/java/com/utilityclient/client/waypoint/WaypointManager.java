package com.utilityclient.client.waypoint;

import com.google.gson.reflect.TypeToken;
import com.utilityclient.UtilityClient;
import java.io.IOException;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class WaypointManager {
    private static final Type WAYPOINT_LIST = new TypeToken<List<Waypoint>>() {}.getType();
    private final List<Waypoint> waypoints = new ArrayList<>();

    public List<Waypoint> getWaypoints() {
        return waypoints;
    }

    public void add(Waypoint waypoint) {
        waypoints.add(waypoint);
    }

    public void remove(Waypoint waypoint) {
        waypoints.remove(waypoint);
    }

    public void save(Path path) throws IOException {
        Files.writeString(path, UtilityClient.GSON.toJson(waypoints, WAYPOINT_LIST), StandardCharsets.UTF_8);
    }

    public void load(Path path) throws IOException {
        waypoints.clear();
        if (!Files.exists(path)) {
            return;
        }
        List<Waypoint> loaded = UtilityClient.GSON.fromJson(Files.readString(path, StandardCharsets.UTF_8), WAYPOINT_LIST);
        if (loaded != null) {
            waypoints.addAll(loaded);
        }
    }
}
