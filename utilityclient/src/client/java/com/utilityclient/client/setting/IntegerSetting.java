package com.utilityclient.client.setting;

import com.google.gson.JsonElement;
import com.google.gson.JsonPrimitive;

public final class IntegerSetting extends Setting<Integer> {
    private final int min;
    private final int max;

    public IntegerSetting(String name, String description, int defaultValue, int min, int max) {
        super(name, description, defaultValue);
        this.min = min;
        this.max = max;
    }

    @Override
    public void set(Integer value) {
        super.set(Math.max(min, Math.min(max, value)));
    }

    @Override
    public JsonElement toJson() {
        return new JsonPrimitive(get());
    }

    @Override
    public void fromJson(JsonElement element) {
        if (element != null && element.isJsonPrimitive()) {
            set(element.getAsInt());
        }
    }
}
