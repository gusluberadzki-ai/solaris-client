package com.utilityclient.client.setting;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

public final class ColorSetting extends Setting<int[]> {
    public ColorSetting(String name, String description, int red, int green, int blue, int alpha) {
        super(name, description, new int[] {red, green, blue, alpha});
    }

    @Override
    public JsonElement toJson() {
        JsonObject object = new JsonObject();
        object.addProperty("r", get()[0]);
        object.addProperty("g", get()[1]);
        object.addProperty("b", get()[2]);
        object.addProperty("a", get()[3]);
        return object;
    }

    @Override
    public void fromJson(JsonElement element) {
        if (element != null && element.isJsonObject()) {
            JsonObject object = element.getAsJsonObject();
            set(new int[] {
                clamp(object, "r"),
                clamp(object, "g"),
                clamp(object, "b"),
                clamp(object, "a")
            });
        }
    }

    private int clamp(JsonObject object, String key) {
        return Math.max(0, Math.min(255, object.get(key).getAsInt()));
    }
}
