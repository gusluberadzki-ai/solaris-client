package com.utilityclient.client.module.world;

import com.utilityclient.client.module.Category;
import com.utilityclient.client.module.Module;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.DoubleSetting;
import net.minecraft.client.KeyMapping;

public final class WorldMapModule extends Module {
    private final DoubleSetting defaultZoom = addSetting(new DoubleSetting("defaultZoom", "Default full map zoom", 1.0D, 0.25D, 4.0D));
    private final BooleanSetting autoOpen = addSetting(new BooleanSetting("autoOpen", "Open automatically on join", false));

    public WorldMapModule(KeyMapping keybind) {
        super("World Map", "Full-screen world map GUI scaffolding.", Category.WORLD, keybind);
    }

    @Override
    public void onEnable() {
    }

    @Override
    public void onDisable() {
    }

    public double getDefaultZoom() {
        return defaultZoom.get();
    }

    public boolean shouldAutoOpen() {
        return autoOpen.get();
    }
}
