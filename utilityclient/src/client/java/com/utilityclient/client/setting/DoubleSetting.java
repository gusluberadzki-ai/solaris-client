package com.utilityclient.client.setting;

import com.google.gson.JsonElement;
import com.google.gson.JsonPrimitive;

public final class DoubleSetting extends Setting<Double> {
    private final double min;
    private final double max;

    public DoubleSetting(String name, String description, double defaultValue, double min, double max) {
        super(name, description, defaultValue);
        this.min = min;
        this.max = max;
    }

    @Override
    public void set(Double value) {
        super.set(Math.max(min, Math.min(max, value)));
    }

    @Override
    public JsonElement toJson() {
        return new JsonPrimitive(get());
    }

    @Override
    public void fromJson(JsonElement element) {
        if (element != null && element.isJsonPrimitive()) {
            set(element.getAsDouble());
        }
    }
}
