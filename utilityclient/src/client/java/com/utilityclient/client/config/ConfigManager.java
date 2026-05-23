package com.utilityclient.client.config;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.utilityclient.UtilityClient;
import com.utilityclient.client.UtilityClientClient;
import com.utilityclient.client.module.Module;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import net.minecraft.client.Minecraft;

public final class ConfigManager {
    private final Path configRoot = Minecraft.getInstance().gameDirectory.toPath().resolve("config").resolve("utilityclient");

    public void loadAll() {
        try {
            Files.createDirectories(configRoot);
            loadGlobal();
            for (Module module : UtilityClientClient.moduleManager.getModules()) {
                loadModule(module);
            }
            UtilityClientClient.waypointManager.load(configRoot.resolve("waypoints.json"));
        } catch (IOException exception) {
            UtilityClient.LOGGER.error("Failed to load Utility Client configs", exception);
        }
    }

    public void saveAll() {
        try {
            Files.createDirectories(configRoot);
            saveGlobal();
            for (Module module : UtilityClientClient.moduleManager.getModules()) {
                saveModule(module);
            }
            UtilityClientClient.waypointManager.save(configRoot.resolve("waypoints.json"));
        } catch (IOException exception) {
            UtilityClient.LOGGER.error("Failed to save Utility Client configs", exception);
        }
    }

    public void saveModule(Module module) {
        try {
            Files.createDirectories(configRoot);
            Files.writeString(
                configRoot.resolve(module.getName().toLowerCase().replace(' ', '_') + ".json"),
                UtilityClient.GSON.toJson(module.toJson()),
                StandardCharsets.UTF_8
            );
        } catch (IOException exception) {
            UtilityClient.LOGGER.error("Failed to save module {}", module.getName(), exception);
        }
    }

    private void loadModule(Module module) {
        Path path = configRoot.resolve(module.getName().toLowerCase().replace(' ', '_') + ".json");
        if (!Files.exists(path)) {
            return;
        }
        try {
            JsonObject object = JsonParser.parseString(Files.readString(path, StandardCharsets.UTF_8)).getAsJsonObject();
            module.fromJson(object);
            if (module.isEnabled()) {
                module.onEnable();
            }
        } catch (Exception exception) {
            UtilityClient.LOGGER.error("Failed to load module {}", module.getName(), exception);
        }
    }

    private void saveGlobal() throws IOException {
        JsonObject object = new JsonObject();
        Map<String, Integer> keybinds = new HashMap<>();
        UtilityClientClient.moduleManager.getModules().forEach(module ->
            keybinds.put(module.getName(), module.getKeybind().getDefaultKey().getValue())
        );
        object.add("keybinds", UtilityClient.GSON.toJsonTree(keybinds));
        Files.writeString(configRoot.resolve("global.json"), UtilityClient.GSON.toJson(object), StandardCharsets.UTF_8);
    }

    private void loadGlobal() throws IOException {
        Path path = configRoot.resolve("global.json");
        if (!Files.exists(path)) {
            return;
        }
        JsonParser.parseString(Files.readString(path, StandardCharsets.UTF_8)).getAsJsonObject();
    }
}
