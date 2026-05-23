package com.utilityclient.client.module.misc;

import com.utilityclient.client.module.Category;
import com.utilityclient.client.module.Module;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.DoubleSetting;
import net.minecraft.client.KeyMapping;

public final class ScoreboardTweaksModule extends Module {
    private final BooleanSetting hideNumbers = addSetting(new BooleanSetting("hideNumbers", "Hide scoreboard scores", false));
    private final BooleanSetting hideEntirely = addSetting(new BooleanSetting("hideEntirely", "Hide scoreboard", false));
    private final DoubleSetting opacity = addSetting(new DoubleSetting("opacity", "Background opacity", 0.75D, 0.0D, 1.0D));

    public ScoreboardTweaksModule(KeyMapping keybind) {
        super("Scoreboard Tweaks", "Visibility tweaks for the sidebar scoreboard.", Category.MISC, keybind);
    }

    @Override
    public void onEnable() {
    }

    @Override
    public void onDisable() {
    }

    public boolean shouldHideEntirely() {
        return isEnabled() && hideEntirely.get();
    }

    public boolean shouldHideNumbers() {
        return isEnabled() && hideNumbers.get();
    }

    public float getOpacity() {
        return opacity.get().floatValue();
    }
}
