package com.utilityclient.client.module.misc;

import com.utilityclient.client.module.Category;
import com.utilityclient.client.module.Module;
import com.utilityclient.client.setting.BooleanSetting;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;

public final class ToggleSprintSneakModule extends Module {
    private final BooleanSetting toggleSprint = addSetting(new BooleanSetting("toggleSprint", "Enable sprint toggle", true));
    private final BooleanSetting toggleSneak = addSetting(new BooleanSetting("toggleSneak", "Enable sneak toggle", true));
    private final BooleanSetting showIndicator = addSetting(new BooleanSetting("showIndicator", "Show HUD indicator", true));
    private boolean sprintState;
    private boolean sneakState;
    private boolean lastSprintKey;
    private boolean lastSneakKey;

    public ToggleSprintSneakModule(KeyMapping keybind) {
        super("ToggleSprint / ToggleSneak", "One-press sprint and sneak toggles.", Category.MOVEMENT, keybind);
    }

    @Override
    public void onEnable() {
    }

    @Override
    public void onDisable() {
        sprintState = false;
        sneakState = false;
    }

    @Override
    public void onTick(Minecraft client) {
        boolean sprintKey = client.options.keySprint.isDown();
        boolean sneakKey = client.options.keyShift.isDown();
        if (toggleSprint.get() && sprintKey && !lastSprintKey) {
            sprintState = !sprintState;
        }
        if (toggleSneak.get() && sneakKey && !lastSneakKey) {
            sneakState = !sneakState;
        }
        lastSprintKey = sprintKey;
        lastSneakKey = sneakKey;
        if (client.player != null) {
            client.player.setSprinting(sprintState);
            client.options.keyShift.setDown(sneakState);
        }
    }

    @Override
    public void onHudRender(GuiGraphics graphics, float tickDelta) {
        if (!showIndicator.get()) {
            return;
        }
        int y = Minecraft.getInstance().getWindow().getGuiScaledHeight() - 30;
        graphics.drawString(Minecraft.getInstance().font, "Sprint: " + (sprintState ? "ON" : "OFF") + " Sneak: " + (sneakState ? "ON" : "OFF"), 8, y, 0xFFFFFFFF);
    }
}
