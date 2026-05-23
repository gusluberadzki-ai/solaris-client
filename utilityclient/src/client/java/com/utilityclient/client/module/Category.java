package com.utilityclient.client.module;

public enum Category {
    COMBAT("Combat"),
    HUD("HUD"),
    WORLD("World"),
    RENDER("Render"),
    MOVEMENT("Movement"),
    MOUNT("Mount"),
    MISC("Misc");

    private final String displayName;

    Category(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }
}
