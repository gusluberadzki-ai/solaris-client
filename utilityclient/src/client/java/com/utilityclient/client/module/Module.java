package com.utilityclient.client.module;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.utilityclient.client.UtilityClientClient;
import com.utilityclient.client.setting.Setting;
import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.client.rendering.v1.world.WorldRenderContext;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;

public abstract class Module {
    private final String name;
    private final String description;
    private final Category category;
    private boolean enabled;
    private final KeyMapping keybind;
    private final List<Setting<?>> settings = new ArrayList<>();

    protected Module(String name, String description, Category category, KeyMapping keybind) {
        this.name = name;
        this.description = description;
        this.category = category;
        this.keybind = keybind;
    }

    public abstract void onEnable();

    public abstract void onDisable();

    public void onTick(Minecraft client) {
    }

    public void onHudRender(GuiGraphics graphics, float tickDelta) {
    }

    public void onWorldRender(WorldRenderContext context) {
    }

    public final void toggle() {
        setEnabled(!enabled);
    }

    public final void setEnabled(boolean enabled) {
        if (this.enabled == enabled) {
            return;
        }
        this.enabled = enabled;
        if (enabled) {
            onEnable();
        } else {
            onDisable();
        }
        UtilityClientClient.configManager.saveModule(this);
    }

    public final void setEnabledSilently(boolean enabled) {
        this.enabled = enabled;
    }

    protected final <T extends Setting<?>> T addSetting(T setting) {
        settings.add(setting);
        return setting;
    }

    public JsonObject toJson() {
        JsonObject object = new JsonObject();
        object.addProperty("enabled", enabled);
        object.addProperty("key", keybind.getDefaultKey().getValue());
        JsonArray array = new JsonArray();
        for (Setting<?> setting : settings) {
            JsonObject entry = new JsonObject();
            entry.addProperty("name", setting.getName());
            entry.add("value", setting.toJson());
            array.add(entry);
        }
        object.add("settings", array);
        return object;
    }

    public void fromJson(JsonObject object) {
        if (object.has("enabled")) {
            enabled = object.get("enabled").getAsBoolean();
        }
        if (object.has("settings")) {
            object.getAsJsonArray("settings").forEach(element -> {
                JsonObject entry = element.getAsJsonObject();
                String settingName = entry.get("name").getAsString();
                settings.stream()
                    .filter(setting -> setting.getName().equals(settingName))
                    .findFirst()
                    .ifPresent(setting -> setting.fromJson(entry.get("value")));
            });
        }
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public Category getCategory() {
        return category;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public KeyMapping getKeybind() {
        return keybind;
    }

    public List<Setting<?>> getSettings() {
        return settings;
    }
}
