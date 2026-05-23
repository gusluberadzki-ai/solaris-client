package com.utilityclient.client.setting;

import com.google.gson.JsonElement;
import com.google.gson.JsonPrimitive;

public final class EnumSetting<E extends Enum<E>> extends Setting<E> {
    private final Class<E> enumType;

    public EnumSetting(String name, String description, E defaultValue, Class<E> enumType) {
        super(name, description, defaultValue);
        this.enumType = enumType;
    }

    @Override
    public JsonElement toJson() {
        return new JsonPrimitive(get().name());
    }

    @Override
    public void fromJson(JsonElement element) {
        if (element != null && element.isJsonPrimitive()) {
            try {
                set(Enum.valueOf(enumType, element.getAsString()));
            } catch (IllegalArgumentException ignored) {
            }
        }
    }
}
