package com.utilityclient.client;

import com.mojang.blaze3d.platform.InputConstants;
import com.utilityclient.UtilityClient;
import com.utilityclient.client.config.ConfigManager;
import com.utilityclient.client.event.ClientEventBus;
import com.utilityclient.client.gui.ClickGuiScreen;
import com.utilityclient.client.gui.HudEditorScreen;
import com.utilityclient.client.gui.WorldMapScreen;
import com.utilityclient.client.manager.HudManager;
import com.utilityclient.client.manager.ModuleManager;
import com.utilityclient.client.util.TpsTracker;
import com.utilityclient.client.waypoint.WaypointManager;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientLifecycleEvents;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.KeyMapping;
import net.minecraft.resources.Identifier;
import org.lwjgl.glfw.GLFW;

public final class UtilityClientClient implements ClientModInitializer {
    public static ModuleManager moduleManager;
    public static ConfigManager configManager;
    public static HudManager hudManager;
    public static WaypointManager waypointManager;

    public static final KeyMapping.Category KEY_CATEGORY = KeyMapping.Category.register(
        Identifier.fromNamespaceAndPath(UtilityClient.MOD_ID, "controls")
    );

    // Right Ctrl opens the Click GUI per spec; Right Shift opens HUD Editor.
    public static final KeyMapping CLICK_GUI_KEY = new KeyMapping(
        "key.utilityclient.click_gui",
        InputConstants.Type.KEYSYM,
        GLFW.GLFW_KEY_RIGHT_CONTROL,
        KEY_CATEGORY
    );

    public static final KeyMapping HUD_EDITOR_KEY = new KeyMapping(
        "key.utilityclient.hud_editor",
        InputConstants.Type.KEYSYM,
        GLFW.GLFW_KEY_RIGHT_SHIFT,
        KEY_CATEGORY
    );

    public static final KeyMapping WORLD_MAP_KEY = new KeyMapping(
        "key.utilityclient.world_map",
        InputConstants.Type.KEYSYM,
        GLFW.GLFW_KEY_M,
        KEY_CATEGORY
    );

    public static final KeyMapping ZOOM_KEY = new KeyMapping(
        "key.utilityclient.zoom",
        InputConstants.Type.KEYSYM,
        GLFW.GLFW_KEY_V,
        KEY_CATEGORY
    );

    @Override
    public void onInitializeClient() {
        KeyBindingHelper.registerKeyBinding(CLICK_GUI_KEY);
        KeyBindingHelper.registerKeyBinding(HUD_EDITOR_KEY);
        KeyBindingHelper.registerKeyBinding(WORLD_MAP_KEY);
        KeyBindingHelper.registerKeyBinding(ZOOM_KEY);

        waypointManager = new WaypointManager();
        hudManager = new HudManager();
        configManager = new ConfigManager();
        moduleManager = new ModuleManager();

        moduleManager.registerDefaults();
        configManager.loadAll();
        TpsTracker.register();
        ClientEventBus.register();

        ClientLifecycleEvents.CLIENT_STOPPING.register(client -> configManager.saveAll());
        UtilityClient.LOGGER.info("Utility Client client initialized.");
    }

    public static void handleGlobalKeys() {
        var client = net.minecraft.client.Minecraft.getInstance();

        while (CLICK_GUI_KEY.consumeClick()) {
            client.setScreen(new ClickGuiScreen());
        }

        while (HUD_EDITOR_KEY.consumeClick()) {
            client.setScreen(new HudEditorScreen());
        }

        while (WORLD_MAP_KEY.consumeClick()) {
            client.setScreen(new WorldMapScreen());
        }
    }
}
