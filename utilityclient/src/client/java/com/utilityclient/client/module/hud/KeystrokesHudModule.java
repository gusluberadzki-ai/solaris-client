package com.utilityclient.client.module.hud;

import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.ColorSetting;
import com.utilityclient.client.util.RenderUtil;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;

public final class KeystrokesHudModule extends HudModule {
    private final BooleanSetting showCps = addSetting(new BooleanSetting("showCPS", "Show click counters", true));
    private final ColorSetting activeColor = addSetting(new ColorSetting("activeColor", "Active key color", 16, 185, 129, 255));
    private final ColorSetting inactiveColor = addSetting(new ColorSetting("inactiveColor", "Inactive key color", 55, 65, 81, 255));

    private int leftClicks;
    private int rightClicks;
    private boolean lastAttackDown;
    private boolean lastUseDown;

    public KeystrokesHudModule(KeyMapping keybind) {
        super("Keystrokes HUD", "WASD and mouse-button overlay.", Category.HUD, keybind, 210, 250);
        width = 108;
        height = 80;
    }

    @Override
    public void onEnable() {
    }

    @Override
    public void onDisable() {
    }

    @Override
    public void onTick(Minecraft client) {
        boolean attackDown = client.options.keyAttack.isDown();
        boolean useDown = client.options.keyUse.isDown();
        if (attackDown && !lastAttackDown) {
            leftClicks++;
        }
        if (useDown && !lastUseDown) {
            rightClicks++;
        }
        lastAttackDown = attackDown;
        lastUseDown = useDown;
    }

    @Override
    public void onHudRender(GuiGraphics graphics, float tickDelta) {
        Minecraft client = Minecraft.getInstance();
        if (!isVisible()) {
            return;
        }
        RenderUtil.panel(graphics, getX(), getY(), width, height);
        drawKey(graphics, "W", getX() + 36, getY() + 6, client.options.keyUp.isDown());
        drawKey(graphics, "A", getX() + 8, getY() + 28, client.options.keyLeft.isDown());
        drawKey(graphics, "S", getX() + 36, getY() + 28, client.options.keyDown.isDown());
        drawKey(graphics, "D", getX() + 64, getY() + 28, client.options.keyRight.isDown());
        drawKey(graphics, "SP", getX() + 8, getY() + 50, client.options.keyJump.isDown());
        drawKey(graphics, "SH", getX() + 64, getY() + 50, client.options.keyShift.isDown());
        if (showCps.get()) {
            RenderUtil.text(graphics, "LMB " + leftClicks + " | RMB " + rightClicks, getX() + 6, getY() + height - 12, 0xFFFFFFFF);
        }
    }

    private void drawKey(GuiGraphics graphics, String label, int x, int y, boolean active) {
        int[] color = active ? activeColor.get() : inactiveColor.get();
        int argb = (color[3] << 24) | (color[0] << 16) | (color[1] << 8) | color[2];
        graphics.fill(x, y, x + 24, y + 16, argb);
        RenderUtil.text(graphics, label, x + 7, y + 4, 0xFFFFFFFF);
    }
}
