package com.utilityclient.client.manager;

import com.mojang.blaze3d.platform.InputConstants;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.module.Module;
import com.utilityclient.client.module.combat.AutoClickerModule;
import com.utilityclient.client.module.hud.ArmorDurabilityHudModule;
import com.utilityclient.client.module.hud.EffectTimersHudModule;
import com.utilityclient.client.module.hud.FpsPerformanceHudModule;
import com.utilityclient.client.module.hud.HungerSaturationHudModule;
import com.utilityclient.client.module.hud.KeystrokesHudModule;
import com.utilityclient.client.module.hud.PositionIndicatorHudModule;
import com.utilityclient.client.module.hud.SpeedIndicatorHudModule;
import com.utilityclient.client.module.misc.ScoreboardTweaksModule;
import com.utilityclient.client.module.misc.ToggleSprintSneakModule;
import com.utilityclient.client.module.misc.ZoomModule;
import com.utilityclient.client.module.mount.MountHudModule;
import com.utilityclient.client.module.render.CrosshairCustomizerModule;
import com.utilityclient.client.module.world.MinimapModule;
import com.utilityclient.client.module.world.WaypointsModule;
import com.utilityclient.client.module.world.WorldMapModule;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Optional;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.KeyMapping;
import org.lwjgl.glfw.GLFW;
import com.utilityclient.client.UtilityClientClient;

public final class ModuleManager {
    private final List<Module> modules = new ArrayList<>();

    public void registerDefaults() {
        register(new AutoClickerModule(key("autoclicker", GLFW.GLFW_KEY_UNKNOWN)));
        register(new HungerSaturationHudModule(key("hunger_saturation_hud", GLFW.GLFW_KEY_UNKNOWN)));
        register(new MinimapModule(key("minimap", GLFW.GLFW_KEY_UNKNOWN)));
        register(new WorldMapModule(key("world_map_module", GLFW.GLFW_KEY_UNKNOWN)));
        register(new WaypointsModule(key("waypoints", GLFW.GLFW_KEY_UNKNOWN)));
        register(new ArmorDurabilityHudModule(key("armor_durability_hud", GLFW.GLFW_KEY_UNKNOWN)));
        register(new EffectTimersHudModule(key("effect_timers_hud", GLFW.GLFW_KEY_UNKNOWN)));
        register(new PositionIndicatorHudModule(key("position_indicator_hud", GLFW.GLFW_KEY_UNKNOWN)));
        register(new SpeedIndicatorHudModule(key("speed_indicator_hud", GLFW.GLFW_KEY_UNKNOWN)));
        register(new FpsPerformanceHudModule(key("fps_performance_hud", GLFW.GLFW_KEY_UNKNOWN)));
        register(new CrosshairCustomizerModule(key("crosshair_customizer", GLFW.GLFW_KEY_UNKNOWN)));
        register(new KeystrokesHudModule(key("keystrokes_hud", GLFW.GLFW_KEY_UNKNOWN)));
        register(new ToggleSprintSneakModule(key("toggle_sprint_sneak", GLFW.GLFW_KEY_G)));
        register(new ZoomModule(key("zoom_module", GLFW.GLFW_KEY_V)));
        register(new ScoreboardTweaksModule(key("scoreboard_tweaks", GLFW.GLFW_KEY_UNKNOWN)));
        register(new MountHudModule(key("mount_hud", GLFW.GLFW_KEY_UNKNOWN)));
    }

    private KeyMapping key(String name, int keyCode) {
        return KeyBindingHelper.registerKeyBinding(new KeyMapping(
            "key.utilityclient." + name,
            InputConstants.Type.KEYSYM,
            keyCode,
            UtilityClientClient.KEY_CATEGORY
        ));
    }

    public void register(Module module) {
        modules.add(module);
    }

    public List<Module> getModules() {
        return modules.stream()
            .sorted(Comparator.comparing((Module module) -> module.getCategory().ordinal()).thenComparing(Module::getName))
            .toList();
    }

    public List<Module> getByCategory(Category category) {
        return modules.stream().filter(module -> module.getCategory() == category).toList();
    }

    public Optional<Module> getModuleByName(String name) {
        return modules.stream()
            .filter(module -> module.getName().toLowerCase(Locale.ROOT).equals(name.toLowerCase(Locale.ROOT)))
            .findFirst();
    }

    public <T extends Module> T getModuleByClass(Class<T> moduleClass) {
        return moduleClass.cast(modules.stream()
            .filter(moduleClass::isInstance)
            .findFirst()
            .orElseThrow(() -> new IllegalArgumentException("Module not registered: " + moduleClass.getSimpleName())));
    }
}
